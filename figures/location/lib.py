import re

class Location(object):
  def __init__(self, lat, lon):
    self.lat = float(lat)
    self.lon = float(lon)
    
class DeviceLocation(Location):
  LOGLINE_PATTERN = \
    re.compile(r"""mProvider=(?P<provider>\w+),.*?mLatitude=(?P<lat>[0-9\-\.]+),.*?mLongitude=(?P<lon>[0-9\-\.]+),.*?mAccuracy=(?P<accuracy>[0-9\.]+)""",
               re.VERBOSE)
    
  def __init__(self, logline):
    match = DeviceLocation.LOGLINE_PATTERN.search(logline.log_message)
    if match == None:
      raise Exception("Unable to create location object: %s" % (logline.log_message,))
    self.provider = match.group('provider')
    self.accuracy = float(match.group('accuracy'))
    super(DeviceLocation, self).__init__(match.group('lat'), match.group('lon'))