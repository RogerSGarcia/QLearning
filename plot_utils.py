import matplotlib.pyplot as plt
import numpy as np
import os

def results_to_plots(episodes, scores, avg_rewards, discount, alphas, walk_reward):
	#Ensure directory exist to save plots 
	path_to_save = os.path.join(os.getcwd(), "q_plots")
	if not os.path.exists(path_to_save): os.makedirs(path_to_save)

	######                    ######
	###### Episodes vs Scores ######
	######                    ######
	fig, ax = plt.subplots()
	plot_path = os.path.join(path_to_save, "episode_score.png")
	plot_path_svg = os.path.join(path_to_save, "episode_score.svg")
	plt.plot(episodes,scores, color='g')
	plt.title("Episodes vs Score")
	plt.xlabel("Episodes")
	plt.xticks(np.arange(min(episodes), max(episodes)+1, 1.0))
	plt.ylabel("Score (Walk Reward)")
	plt.grid(True)
	# plt.savefig(plot_path_svg, format = 'svg', dpi = 1200)
	plt.text(max(episodes)*0.70, min(scores), 'Discount Factor: ' + str(discount) + '\n' + 'Walk Reward: '+ str(walk_reward))
	# plt.text(max(episodes), min(scores), r'$\mu=100,\ \sigma=15$')
	plt.savefig(plot_path)
	# plt.show()
	
	######                            ######
	###### Episodes vs average reward ######
	######                            ######
	plot_path = os.path.join(path_to_save, "episode_reward.png")
	plt.clf()
	plt.plot(episodes, avg_rewards,color='k')
	plt.title("Avg. Reward Over Time")
	plt.xlabel("Episodes")
	plt.xticks(np.arange(min(episodes), max(episodes)+1, 1.0))
	plt.ylabel("Reward")
	plt.grid(True)
	plt.savefig(plot_path)
	# plt.savefig('Result01.svg', format = 'svg', dpi=1200)
	# plt.savefig('Result01.eps', format='eps', dpi=1000)
	
	######                                      ######
	###### Episodes vs average alpha (decaying) ######
	######                                      ######

	plot_path = os.path.join(path_to_save, "episode_alphas.png")

	plt.clf()
	plt.plot(episodes, alphas,color='m')
	plt.title(r'$\alpha$' + " Over Time")
	plt.xlabel("Episodes")
	plt.xticks(np.arange(min(episodes), max(episodes)+1, 1.0))
	plt.ylabel(r'$\alpha$')
	plt.grid(True)
	plt.savefig(plot_path)
	# # plt.savefig('Result02.svg', format = 'svg', dpi=1200)


##################################################################################################################
# Print World info
##################################################################################################################
def print_info(alpha, discount, walk_reward, iteration, number_of_iterations):
	print('*********************')
	print('Learning Rate: ', alpha)
	print('Discount Factor (gamma): ', discount)
	print('Walk Reward: ', walk_reward)
	print('World Iter: ', iteration)
	print('Number of Moves (actions): ', int(number_of_iterations))
	print('*********************')
	
# if save:
#     #save screenshot of world
#     im = ImageGrab.grab(bbox=(0,0,500,500))
#     im.save('WORLDscreenshot.png')
