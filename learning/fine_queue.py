import numpy as np
import tensorflow as tf
from agent import Agent, Network
import os


class FineQueue():
	def __init__(self, args, dir_name):
		self.F = args.F
		self.T = args.T
		self.k = args.k
		self.g = args.g
		self.tau = args.tau
		self.x_mean = args.x_mean
		self.x_std = args.x_std
		self.N_equal = self.T * (self.x_mean - args.k)
		self.args = args
		self.dir_name = dir_name
		self.return_mean, self.return_std = None, None

		# These are dictionaries where the keys denote the group
		groups = np.random.randint(0, self.g, size=args.N_init)
		self.agents = [Agent(args, group=groups[i], use_to_train=False) for i in range(args.N_init)]
		self.networks = [Network(args, group=g) for g in range(self.g)]
		# Where I am (0), what I paid so far (1) and how much time I spent in the queue (2)
		# action (3) and its probability (4) advantage (5), return (6) and acting flag (7)
		self.buffer = np.zeros(shape=(args.train_sims, self.g, args.buffer_len, 8), dtype=np.float32)

		self.pointers = np.zeros(self.g, dtype=np.int)

		self.step_num = 0
		self.sim_num = 0

		max_payment = 2 * args.F + args.fined_penalty
		self.log = {'leaving_time': np.zeros(shape=(args.train_sims, args.g, args.T), dtype=np.int),
					'leaving_payment': np.zeros(shape=(args.train_sims, args.g, max_payment), dtype=np.int)}
		self.group_returns = [[] for _ in range(args.g)]

	def add_agents(self):
		to_add = int(np.random.normal(loc=self.x_mean, scale=self.x_std))
		if self.step_num > self.tau * self.T:
			for _ in range(to_add):
				group = np.random.randint(self.g)
				new_agent = Agent(self.args, group=group)
				self.agents.append(new_agent)
		else:
			for _ in range(to_add):
				group = np.random.randint(self.g)
				new_agent = Agent(self.args, group=group, use_to_train=False)
				self.agents.append(new_agent)

	def add_to_buffer(self, agent, fined=False):
		to_pay = int(np.sum(agent.my_buffer[:, 3])) + (self.args.F + self.args.fined_penalty) * fined
		self.log['leaving_payment'][self.sim_num, agent.g, to_pay] += 1
		self.log['leaving_time'][self.sim_num, agent.g, agent.t - 1] += 1

		if agent.use_to_train and self.pointers[agent.g] < self.args.buffer_len:
			self.group_returns[agent.g].append(agent.my_buffer[0, 6])

			is_acting = np.where(agent.my_buffer[:, 7] == 1)
			data = agent.my_buffer[is_acting]
			samples = data.shape[0]

			start = self.pointers[agent.g]
			length = min(samples, self.args.buffer_len - start)
			to_add = data[:length, :]
			self.buffer[self.sim_num, agent.g, start:start + length, :] = to_add
			self.pointers[agent.g] += samples

	def remove_agents(self):
		for i in reversed(range(len(self.agents))):
			if self.agents[i].t >= self.T or self.agents[i].payment >= self.F:
				self.agents[i].compute_return_and_advantage(self.args, i / self.N_equal)
				self.add_to_buffer(self.agents[i])
				self.agents.pop(i)

		for i in reversed(range(min(self.k, len(self.agents)))):
			self.agents[i].my_buffer[self.agents[i].t - 1, 6] -= self.F + self.args.fined_penalty
			self.agents[i].compute_return_and_advantage(self.args, i / self.N_equal)
			self.add_to_buffer(self.agents[i], fined=True)
			self.agents.pop(i)

	def get_observations(self):
		observations = np.zeros(shape=(len(self.agents), 3), dtype=np.float32)
		groups = np.zeros(shape=(len(self.agents, )), dtype=np.float32)
		for i, agent in enumerate(self.agents):
			observations[i, :] = [i / self.N_equal, agent.payment / self.F, agent.t / self.T]
			groups[i] = agent.g

		return observations, groups

	@tf.function
	def _train(self, observations):
		for i, network in enumerate(self.networks):
			network.train(observations[i])

	def preprocess(self):
		if self.return_mean is None:
			self.return_mean = np.mean(self.buffer[self.sim_num, :, :, 6])
			self.return_std = np.std(self.buffer[self.sim_num, :, :, 6])

		self.buffer[self.sim_num, :, :, 6] -= self.return_mean
		self.buffer[self.sim_num, :, :, 6] /= self.return_std

	def train(self):
		self.preprocess()
		print()
		for i in range(self.args.train_cycles):
			self._train(self.buffer[self.sim_num, ...])
			print(f'\rTraining {np.round(100 * (i + 1) / self.args.train_cycles, 1)}% done.', end='')
		print()

	def reset_simulation(self, eval=False):
		for g in range(self.g):
			self.pointers[g] = 0

		self.step_num = 0
		groups = np.random.randint(0, self.g, size=self.args.N_init)
		self.agents = [Agent(self.args, group=groups[i], use_to_train=False) for i in range(self.args.N_init)]
		if not eval:
			self.sim_num += 1
		else:
			self.buffer[self.sim_num, ...] = 0

	def save(self, sim_num):
		home_path = os.getcwd()
		for group_num, network in enumerate(self.networks):
			if sim_num == 0:
				os.mkdir(f'strategy_{group_num}')
			os.chdir(f'strategy_{group_num}')
			os.mkdir(str(sim_num))
			os.chdir(str(sim_num))
			network.save()
			os.chdir(home_path)
		np.save('buffer.npy', self.buffer[:self.sim_num, ...])
		np.save('leaving_time.npy', self.log['leaving_time'])
		np.save('leaving_payment.npy', self.log['leaving_payment'])

	def load(self, sim_num):
		home_path = os.getcwd()
		for group_num, network in enumerate(self.networks):
			os.chdir(f'strategy_{group_num}/{str(sim_num)}')
			network.load()
			os.chdir(home_path)

	def load_last(self):
		home_path = os.getcwd()
		for group_num, network in enumerate(self.networks):
			os.chdir(f'strategy_{group_num + 1}')
			sim_num = len(os.listdir())
			os.chdir(str(sim_num))
			network.load()
			os.chdir(home_path)

	def load_single(self, load_g, sim):
		self.step_num = 0

		for g in range(self.g):
			self.pointers[g] = 0

			home_path = os.getcwd()
			s = sim + 1 if g == load_g else sim
			os.chdir(f'strategy_{g}/{s}')

			self.networks[g].load()

			os.chdir(home_path)

	def average_return(self):
		return np.array([np.mean(self.group_returns[g]) for g in range(self.g)])

	@tf.function(experimental_relax_shapes=True)
	def group_predict(self, observations):
		actions = tf.TensorArray(tf.int32, size=self.args.g)
		probabilities = tf.TensorArray(tf.float32, size=self.args.g)
		values = tf.TensorArray(tf.float32, size=self.args.g)
		for i, network in enumerate(self.networks):
			preds = network.predict(observations)

			actions = actions.write(i, preds['policy'])
			probabilities = probabilities.write(i, preds['probability'])
			values = values.write(i, preds['value'])

		actions = actions.stack()
		probabilities = probabilities.stack()
		values = values.stack()
		return actions, probabilities, values

	def step(self, eval=False):
		# Obtain actions of all agents
		observations, groups = self.get_observations()
		acting = np.random.uniform(0, 1, size=(len(self.agents, ))) > np.array([a.p for a in self.agents])
		group_actions, group_probabilities, group_values = self.group_predict(observations)
		for g in range(self.g):
			group_ids = np.where(groups == g)[0]
			actions = group_actions.numpy()[g, group_ids]
			probabilities = group_probabilities.numpy()[g, group_ids]
			values = group_values.numpy()[g, group_ids]
			if actions.shape[0] == 0:
				continue  # There is nobody in this group now

			for k, id in enumerate(group_ids):
				agent = self.agents[id]
				action = actions[k] if acting[id] else 0
				agent.my_buffer[agent.t, :3] = observations[id]
				agent.my_buffer[agent.t, 3] = action
				agent.my_buffer[agent.t, 4] = probabilities[k]
				agent.my_buffer[agent.t, 5] = values[k]
				agent.my_buffer[agent.t, 6] = - action
				agent.my_buffer[agent.t, 7] = acting[id]
				agent.t += 1
				agent.payment += action

		# Sort according to average payment
		self.agents.sort(key=lambda agent: agent.average_payment, reverse=False)

		# Remove agents
		self.remove_agents()

		# Add new agents
		self.add_agents()

		if not eval:
			print(
				f'\r{self.step_num, len(self.agents)}: Buffer {np.round(100 * np.min(self.pointers) / self.args.buffer_len, 1)}% full.',
				end='')
		else:
			print(
				f'\r{self.step_num, len(self.agents)}: Eval buffer {np.round(100 * np.min(self.pointers) / self.args.buffer_len, 1)}% full.',
				end='')

		self.step_num += 1








