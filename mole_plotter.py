import matplotlib.pylab as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


def mole_pop_plot():
	cells = np.loadtxt('population_history.txt')
	with PdfPages('mole_pop_history.pdf') as pdf:
		fig,ax = plt.subplots()
		# create discrete colormap
		cmap = plt.cm.get_cmap('viridis', 4) 

		cax = ax.imshow(cells,aspect='auto',cmap=cmap)
		cbar = fig.colorbar(cax,ticks=[-1,0,1,2],cmap=cmap)
		cbar.ax.set_yticklabels(['Empty', 'Queen', 'Worker', 'Juvenile'])
		plt.ylabel('Cell Index')
		plt.xlabel('Time (Quarter)')
		pdf.savefig(bbox_inches='tight')

mole_pop_plot()