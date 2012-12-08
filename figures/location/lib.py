import re, math

class Location(object):
  RADIUS = 6371.0
  
  def __init__(self, lat, lon):
    self.lat = float(lat)
    self.lon = float(lon)
  
  def dist(self, other):
    dlat = math.radians(other.lat - self.lat)
    dlon = math.radians(other.lon - self.lon)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(self.lat)) \
        * math.cos(math.radians(other.lat)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = Location.RADIUS * c
    return d

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
    self.datetime = logline.datetime
    super(DeviceLocation, self).__init__(match.group('lat'), match.group('lon'))