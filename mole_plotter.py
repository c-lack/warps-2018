import matplotlib.pylab as plt
import numpy as np
import sys
from matplotlib.backends.backend_pdf import PdfPages

ptype = sys.argv[1]

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

def mole_resource_plot():
	resource = np.loadtxt('resource_history.txt')
	with PdfPages('mole_resource_history.pdf') as pdf:
		plt.plot(resource)
		plt.ylabel('Resources (au)')
		plt.xlabel('Time (Quarter)')
		pdf.savefig(bbox_inches='tight')

namespace = __import__(__name__)
fname = 'mole_%s_plot'%(ptype)
getattr(namespace, fname)()