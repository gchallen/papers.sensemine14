import os

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from location.lib import Location

os.path.dirname(os.path.abspath(__file__))

class SUNYNorth:
  BASEMAP_PARAMS = {'llcrnrlon': -78.79794,
                    'llcrnrlat': 42.99445,
                    'urcrnrlon': -78.7785,
                    'urcrnrlat': 43.01063,
                    'resolution': 'l'}
  BACKGROUND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps/SUNYNorth.png')
  
  def __init__(self):
    self.m = Basemap(**SUNYNorth.BASEMAP_PARAMS)
    self.background = plt.imread(SUNYNorth.BACKGROUND_PATH)
    
DAVIS_HALL = Location(43.00276406362166, -78.7873363494873)