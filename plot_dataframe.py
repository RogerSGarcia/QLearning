#convert -delay 20 -loop 0 table_*.png qtable.gif
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_Qtable(Qtable, iteration):
	#Ensure directory exist to save plots 
	path_to_save = os.path.join(os.getcwd(), "temp_plots")
	if not os.path.exists(path_to_save): os.makedirs(path_to_save)

	fig, ax = plt.subplots()

	# hide axes
	fig.patch.set_visible(False)
	ax.axis('off')
	ax.axis('tight')

	# df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
	#get states
	np_Qtable = np.zeros((len(Qtable.keys()), 4))
	all_states = sorted(list(Qtable.keys()))

	for i in range(len(all_states)):
		np_Qtable[i,0] = round(Qtable[all_states[i]]['up'], 5)
		np_Qtable[i,1] = round(Qtable[all_states[i]]['down'], 5)
		np_Qtable[i,2] = round(Qtable[all_states[i]]['left'], 5)
		np_Qtable[i,3] = round(Qtable[all_states[i]]['right'], 5)

	df = pd.DataFrame({'up': np_Qtable[:,0], 'down': np_Qtable[:,1], 'left': np_Qtable[:,2], 'right': np_Qtable[:,3]})

	# df = pd.DataFrame(list(Qtable.items()),columns = ['up','down', 'left', 'right'])
	# df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))

	table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
	table.auto_set_font_size(False)
	table.set_fontsize(20)
	# table.set_text_props(weight = 'bold')

	# fig.tight_layout()
	# fig.figsize = (4,4)
	fig.set_size_inches(20, 20)

	# plt.show()
	if iteration < 10:
		iteration = '0' + str(iteration)
	plt.savefig(os.path.join(path_to_save, "table_" + str(iteration)))
