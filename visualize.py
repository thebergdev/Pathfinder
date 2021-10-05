import matplotlib as mpl
from matplotlib import pyplot
import numpy as np

class MapViz:
    def __init__(self, map, colors, bounds):
        self.map = map
        self.colors = colors
        self.bounds = bounds

    def viz(self):
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(self.colors)
        norm = mpl.colors.BoundaryNorm(self.bounds, cmap.N)

        # tell imshow about color map so that only set colors are used
        img = pyplot.imshow(self.map,interpolation='nearest',
                            cmap = cmap,norm=norm)
        pyplot.show()
    

