import os
from PIL import Image

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from location.lib import Location

os.path.dirname(os.path.abspath(__file__))

class Map(object):
  def __init__(self):
    self.m = Basemap(**self.BASEMAP_PARAMS)
    self.width, self.height = Image.open(self.BACKGROUND_PATH).size
    self.background = plt.imread(self.BACKGROUND_PATH)
    
class SUNYNorth(Map):
  BASEMAP_PARAMS = {'llcrnrlon': -78.79794,
                    'llcrnrlat': 42.99445,
                    'urcrnrlon': -78.7785,
                    'urcrnrlat': 43.01063,
                    'resolution': 'l',
                    'fix_aspect': False}
  BACKGROUND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps/SUNYNorth.png')
  
  

class SUNYNorthSpine(Map):
  BASEMAP_PARAMS = {'llcrnrlon': -78.79596,
                    'llcrnrlat': 42.99904,
                    'urcrnrlon': -78.78013,
                    'urcrnrlat': 43.00309,
                    'resolution': 'l',
                    'fix_aspect': False}
  BACKGROUND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps/SUNYNorthSpine.png')
  
DAVIS_HALL = Location(43.00276406362166, -78.7873363494873)