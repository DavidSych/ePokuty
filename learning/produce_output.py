import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pickle, os


def draw_leaving_counts():
	root = os.getcwd()
	args = pickle.load(open('args.pickle', 'rb'))
	leaving_time = np.load(f'leaving_time.npy')
	leaving_payment = np.load(f'leaving_payment.npy')
	Q = args.fined_penalty + args.F
	avr_payment = np.empty(args.train_sims)
	for num in range(args.train_sims):
		fig, axs = plt.subplots(2, 1)
		for g in range(args.g):
			fig.tight_layout(pad=1.5)
			axs[0].bar(np.arange(args.T) + 1, leaving_time[num, g] / np.sum(leaving_time[num, g]), align='center')
			axs[1].bar(np.arange(Q + args.F), leaving_payment[num, g] / np.sum(leaving_payment[num, g]), align='center')

		axs[0].xaxis.set_major_locator(MaxNLocator(integer=True))
		axs[0].set_xlabel('Time')
		axs[0].set_ylabel('Percentage')
		axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
		axs[1].set_xlabel('Payment')
		axs[1].set_ylabel('Percentage')
		plt.savefig(f'counts_{num}.pdf')
		plt.clf()

		average_payment = np.sum(np.arange(Q + args.F) * leaving_payment[num] / np.sum(leaving_payment[num]))
		min_payment = Q * args.k / args.x_mean
		payment = average_payment - min_payment
		avr_payment[num] = payment
		print(f'Average payment above minimum: {np.round(payment, 2):.2f}, {np.round(100 * payment / args.F, 1):.1f}% of F.')

	episodes = np.arange(1, args.train_sims + 1)
	plt.plot(episodes, avr_payment)
	plt.xlabel('Training Episode')
	plt.ylabel('Payment above Minimum')
	plt.savefig('minimum_payment.pdf')

	os.chdir(root)


#folder = '2022-10-19_21-32'
#draw_final_policy(folder)
#draw_leaving_counts(folder)