import os, cPickle, re, json, dircache
from dateutil.parser import parse

class AutoDict(dict):
  def __getitem__(self, item):
    try:
      return dict.__getitem__(self, item)
    except KeyError:
      value = self[item] = type(self)()
      return value
          
class Logline:
  LOGLINE_PATTERN_STRING = r"""^
   (?P<hashed_ID>\w{40})\s+
   (?P<datetime>\d+-\d+-\d+\s+\d+:\d+:\d+\.\d+)\s+
   (?P<process_id>\d+)\s+(?P<thread_id>\d+)\s+(?P<log_level>\w)\s+
   (?P<log_tag>%s):\s+(?P<json>.*?)$"""
   
  def __init__(self, match, line):
    self.device = match.group('hashed_ID')
    self.datetime = parse(match.group('datetime'))
    self.log_tag = match.group('log_tag').strip()
    self.line = line.strip()
    self.log_message = match.group('json').strip()
      
    try:
      self.json = json.loads(match.group('json').strip())
    except ValueError:
      self.json = None
  
  def __str__(self):
    return self.line
  
class LogFilter(object):
  
  def __init__(self):
    self.sorted_files = sorted([os.path.join(os.environ['MOBISYS13_DATA'], f) for f in dircache.listdir(os.environ['MOBISYS13_DATA']) if os.path.splitext(f)[1] == '.out'],
                               key=lambda k: int(os.path.splitext(os.path.basename(k))[0]))
    
    self.devices = set([])
    
    self.processed = False
    self.__process()
    
  @classmethod
  def path(cls):
    return os.path.join(os.environ['MOBISYS13_DATA'], cls.__name__.lower() + '.dat')
  
  @classmethod
  def load(cls):
    if os.path.exists(cls.path()):
      return cPickle.load(open(cls.path(), 'rb'))
    else:
      return cls()
  
  def __process(self, reprocess=False):
    if self.processed and not reprocess:
      return
    self.process()
    self.processed = True
    self.store()
    
  def store(self):
    cPickle.dump(self, open(self.path(), 'wb'), cPickle.HIGHEST_PROTOCOL)
      
  def generate_loglines(self):
    
    log_tag_string = "|".join([r"""%s\s*""" % (tag,) for tag in self.TAGS])
    logline_pattern_string = Logline.LOGLINE_PATTERN_STRING % (log_tag_string,)
    logline_pattern = re.compile(logline_pattern_string, re.VERBOSE)
    
    for filename in self.sorted_files:
      for line in open(filename, 'rb'):
        m = logline_pattern.match(line)
        if m == None:
          continue
        try:
          l = Logline(m, line)
          self.devices.add(l.device)
          yield l
        except StopIteration:
          return
        except Exception, e:
          raise(e)