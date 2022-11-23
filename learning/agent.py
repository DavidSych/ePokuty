import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np


class Network():
	def __init__(self, args, group):
		self.epsilon = args.epsilon
		self.c_ent = args.entropy_weight
		self.baseline_weight = args.baseline_weight
		self.c_l2 = args.l2_weight
		self.g = group
		self.get_model(args)

	def get_model(self, args):
		inputs = tf.keras.Input(
			shape=(3,))  # My position (0, 1), what I payed so far (0, 1) and how much time I spent in queue (0, 1)

		y = tf.keras.layers.Dense(args.hidden_layer_actor, activation='relu')(inputs)
		# y = tf.keras.layers.Dense(args.hidden_layer_size, activation='relu')(y)
		actions = tf.keras.layers.Dense(args.F + 1, activation='softmax')(y)

		z = tf.keras.layers.Dense(args.hidden_layer_critic, activation='relu')(inputs)
		z = tf.keras.layers.Dense(args.hidden_layer_critic, activation='relu')(z)
		value = tf.keras.layers.Dense(1, activation='linear')(z)[:, 0]

		self.model = tf.keras.Model(inputs=inputs, outputs={'policy': actions, 'value': value})
		self.model.compile(loss=tf.keras.losses.MeanSquaredError(),
						   optimizer=tf.keras.optimizers.Adam(args.learning_rate, global_clipnorm=args.clip_norm))

	def train(self, buffer):
		buffer = tf.cast(buffer, dtype=tf.float32)
		observations = buffer[:, :3]
		actions = buffer[:, 3]
		old_probs = buffer[:, 4]
		advantages = buffer[:, 5]
		returns = buffer[:, 6]

		with tf.GradientTape() as tape:
			prediction = self.model(observations)
			dist = tfp.distributions.Categorical(probs=prediction['policy'])
			new_probs = dist.prob(actions)

			ratio = new_probs / old_probs

			clipped_advantage = tf.where(
				advantages > 0,
				(1 + self.epsilon) * advantages,
				(1 - self.epsilon) * advantages
			)

			policy_loss = - tf.reduce_mean(tf.minimum(ratio * advantages, clipped_advantage))

			entropy_loss = - self.c_ent * tf.reduce_mean(dist.entropy())

			value_loss = self.baseline_weight * self.model.compiled_loss(y_true=returns, y_pred=prediction['value'])

			l2_loss = 0
			for var in self.model.trainable_variables:
				l2_loss += self.c_l2 * tf.nn.l2_loss(var)

			loss = policy_loss + entropy_loss + value_loss + l2_loss

		self.model.optimizer.minimize(loss, self.model.trainable_variables, tape=tape)

	def predict(self, observation):
		preds = self.model(observation)
		dist = tfp.distributions.Categorical(probs=preds['policy'])
		actions = dist.sample()
		p = dist.prob(actions)
		return {'policy': actions, 'value': preds['value'], 'probability': p}

	def save(self):
		self.model.save_weights(f'model_{self.g}.h5')

	def load(self):
		self.model.load_weights(f'model_{self.g}.h5')


class Agent():
	def __init__(self, args, group, use_to_train=True):
		self.t = 0
		self.payment = 0  # What I paid so far
		self.g = group
		if args.ignorance_distribution == 'fixed':
			self.p = args.p
		elif args.ignorance_distribution == 'uniform':
			self.p = np.random.uniform(args.p_min, 1)
		elif args.ignorance_distribution == 'beta':
			self.p = np.random.beta(args.alpha, args.beta)
		else:
			raise NotImplementedError(f'Unknown ignorance distribution {args.ignorance_distribution}.')

		self.my_buffer = np.zeros((args.T, 8))
		self.use_to_train = use_to_train

	@property
	def average_payment(self):
		return self.payment / self.t

	def compute_return_and_advantage(self, args, position):
		t_steps = np.arange(self.t)

		if args.reward_shaping:
			states = np.empty(shape=(self.t + 1, 3))
			states[:self.t, :] = self.my_buffer[:self.t, :3]
			states[self.t, :] = np.array([position, self.payment / args.F, self.t / args.T])
			phi = np.sum(states[:, :1], axis=1)
			self.my_buffer[:self.t, 6] += args.gamma * phi[1:] - phi[:-1]

		self.my_buffer = self.my_buffer[:self.t]
		values = np.append(self.my_buffer[:, 5].copy(), 0)
		rewards = self.my_buffer[:, 6].copy()

		td_error = rewards + args.gamma * values[1:] - values[:-1]
		decay_factor = args.gamma * args._lambda
		a = td_error * (decay_factor ** t_steps)
		a = np.cumsum(a[::-1])[::-1] / (decay_factor ** t_steps)
		self.my_buffer[:, 5] = a

		r = rewards * (args.gamma ** t_steps)
		r = np.cumsum(r[::-1])[::-1] / (args.gamma ** t_steps)
		self.my_buffer[:, 6] = r

	def compute_return(self):
		return np.sum(self.my_buffer[:self.t, 6])
