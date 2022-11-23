import argparse
from fine_queue import FineQueue
import numpy as np
import tensorflow as tf
import datetime
import shutil
import pickle
from produce_output import draw_leaving_counts

import cProfile
import os

parser = argparse.ArgumentParser()
# TF params
parser.add_argument("--seed", default=42, type=int, help="Random seed for reproducibility.")
parser.add_argument("--threads", default=15, type=int, help="Number of CPU threads to use.")
parser.add_argument("--hidden_layer_actor", default=4, type=int, help="Size of the hidden layer of the network.")
parser.add_argument("--hidden_layer_critic", default=32, type=int, help="Size of the hidden layer of the network.")
parser.add_argument("--learning_rate", default=3e-4, type=float, help="Learning rate.")
parser.add_argument("--entropy_weight", default=1e-2, type=float, help="Entropy regularization constant.")
parser.add_argument("--baseline_weight", default=3., type=float, help="Value loss scaling, i.e. critic learning rate scaling.")
parser.add_argument("--l2_weight", default=1e-2, type=float, help="L2 regularization constant.")
parser.add_argument("--clip_norm", default=0.1, type=float, help="Gradient clip norm.")

parser.add_argument("--buffer_len", default=20_000, type=int, help="Number of time steps to train on.")
parser.add_argument("--epsilon", default=0.05, type=float, help="Clipping constant.")
parser.add_argument("--gamma", default=1, type=float, help="Return discounting.")
parser.add_argument("--_lambda", default=0.97, type=float, help="Advantage discounting.")
parser.add_argument("--train_cycles", default=2, type=int, help="Number of PPO passes.")
parser.add_argument("--train_sims", default=4, type=int, help="How many simulations to train from.")
parser.add_argument("--evaluate", default=False, type=bool, help="If NashConv should be computed as well.")

# Queue parameters
parser.add_argument("--F", default=4, type=int, help="End fine to pay.")
parser.add_argument("--fined_penalty", default=0, type=int, help="Additional penalty for leaving due to a fine.")
parser.add_argument("--T", default=4, type=int, help="Time to survive in queue.")
parser.add_argument("--k", default=5, type=int, help="How many people have to pay in each step.")
parser.add_argument("--g", default=1, type=int, help="How many groups to use.")
parser.add_argument("--tau", default=1, type=int, help="Don't use agents added to queue before tau * T steps.")
parser.add_argument("--x_mean", default=100, type=float, help="Mean number of agents to add each step.")
parser.add_argument("--x_std", default=5, type=float, help="Standard deviation of the number of agents to add each step.")
parser.add_argument("--N_init", default=100, type=int, help="Initial number of agents.")
parser.add_argument("--ignorance_distribution", default='uniform', type=str, help="What distribuin to use to sample probability of ignorance. Supported: fixed, uniform, beta.")
parser.add_argument("--p", default=0.7, type=float, help="Probability of ignorance, if fixed.")
parser.add_argument("--p_min", default=0.7, type=float, help="Minimum probability of ignorance, if uniform.")
parser.add_argument("--alpha", default=2, type=float, help="Parameter of Beta distribution of ignorance.")
parser.add_argument("--beta", default=4, type=float, help="Parameter of Beta distribution of ignorance.")
parser.add_argument("--reward_shaping", default=False, type=bool, help="If rewards shaping should be used.")

args = parser.parse_args([] if "__file__" not in globals() else None)

np.random.seed(args.seed)
tf.random.set_seed(args.seed)
tf.config.threading.set_inter_op_parallelism_threads(args.threads)
tf.config.threading.set_intra_op_parallelism_threads(args.threads)

path = os.getcwd()
if not os.path.isdir('Results'):
	os.mkdir('Results')
os.chdir('Results')
dir_name = f'{str(datetime.datetime.now().date())}_{str(datetime.datetime.now().time())[:5].replace(":", "-")}'
os.mkdir(dir_name)
os.chdir(dir_name)
pickle.dump(args, open("args.pickle", "wb"))

shutil.copy(path + '/main.py', path + '/Results/' + dir_name)
shutil.copy(path + '/fine_queue.py', path + '/Results/' + dir_name)
shutil.copy(path + '/agent.py', path + '/Results/' + dir_name)

queue = FineQueue(args, dir_name)
queue.save(0)

eval_queue = FineQueue(args, dir_name)


def simulate_queue():
	# queue.load_from_single()
	nashconv = np.zeros(shape=(args.train_sims, args.g))
	for sim in range(args.train_sims):
		# Run a training cycle
		queue.load(sim)
		while any(pointer < args.buffer_len for pointer in queue.pointers):
			queue.step()

		prev_returns = queue.average_return()
		queue.train()
		queue.save(sim + 1)
		queue.reset_simulation()

		if args.evaluate:
			# Compute "NashConv"
			next_returns = np.zeros(shape=(args.g,))
			for g in range(args.g):
				eval_queue.load_single(g, sim)
				while any(pointer < args.buffer_len for pointer in eval_queue.pointers):
					eval_queue.step(eval=True)

				print()
				next_returns[g] = eval_queue.average_return()[g]
				eval_queue.reset_simulation(eval=True)

			eval_queue.reset_simulation()

			nashconv[sim, :] = next_returns - prev_returns
		np.save('nashconv.npy', nashconv[:sim + 1, :])

		print(f'Simulation {sim + 1} of {args.train_sims} done.\n')


simulate_queue()
draw_leaving_counts()

