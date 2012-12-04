import sys, os, cPickle, re, json, dircache, datetime, itertools
from multiprocessing import Pool

class AutoDict(dict):
  def __getitem__(self, item):
    try:
      return dict.__getitem__(self, item)
    except KeyError:
      value = self[item] = type(self)()
      return value
          
class Logline(object):
  LOGLINE_PATTERN_STRING = r"""^
   (?P<hashed_ID>\w{40})\s+
   (?P<datetime>\d+-\d+-\d+\s+\d+:\d+:\d+\.\d+)\s+
   (?P<process_id>\d+)\s+(?P<thread_id>\d+)\s+(?P<log_level>\w)\s+
   (?P<log_tag>%s):\s+(?P<json>.*?)$"""
  
  def __init__(self, match, line):
    self.device = match.group('hashed_ID')
    self.datetime = datetime.datetime.strptime(match.group('datetime'), '%Y-%m-%d %H:%M:%S.%f')
    self.log_tag = match.group('log_tag').strip()
    self.line = line.strip()
    self.log_message = match.group('json').strip()
    self._json = match.group('json').strip()
    self.json = None
    
  def get_json(self):
    try:
      self.json = json.loads(self._json)
    except ValueError:
      pass    
    return self.json
  
  def __str__(self):
    return self.line
  
class LogFilter(object):
  
  NUM_FILTER_PROCESSES = 8
  
  @classmethod
  def load(cls, **kwargs):
    if os.path.exists(cls._path()):
      return cPickle.load(open(cls._path(), 'rb'))
    else:
      return cls(**kwargs)
  
  def store(self):
    cPickle.dump(self, open(self._path(), 'wb'), cPickle.HIGHEST_PROTOCOL)
  
  @classmethod
  def _directory(cls):
    return os.environ['MOBISYS13_DATA']
  
  @classmethod
  def _path(cls):
    return os.path.join(cls._directory(), cls.__name__.lower() + '.dat')
    
  def __init__(self, tags, verbose=False):
    
    self.tags = tags
    self.pattern = re.compile(Logline.LOGLINE_PATTERN_STRING % ("|".join([r"""%s\s*""" % (tag,) for tag in self.TAGS]),), re.VERBOSE)
    
    self.directory = self._directory()
    self.sorted_files = sorted([os.path.join(self.directory, f) for f in dircache.listdir(self.directory) if os.path.splitext(f)[1] == '.out'],
                               key=lambda k: int(os.path.splitext(os.path.basename(k))[0]))
    
    self.devices = set([])
    self.start_time = None
    self.end_time = None
    self.verbose = verbose
    
    self.filtered = False
    self.filter()
    self.processed = False
    self.process()
 
  
  def process(self):
    if self.processed:
      return
    
    self.process_loop()
  
  def filter(self):
    if self.filtered:
      return
    pool = Pool(processes=self.NUM_FILTER_PROCESSES)
    f_lines = pool.map(do_filter_star, itertools.izip(self.sorted_files, itertools.repeat(self.pattern), itertools.repeat(self.verbose)))
    print len(f_lines)
      
  def process_loop(self): 
    for line in self.lines:
      self.process_line(line)
      
  @classmethod
  def reset(self):
    self.filtered = False
    self.processed = False

def do_filter_star(f_pattern_verbose):
  return do_filter(*f_pattern_verbose)

def do_filter(f, pattern, verbose=False):
  if verbose:
    print >>sys.stderr, f
  lines = []
  for line in open(f, 'rb'):
    m = pattern.match(line)
    if m == None:
      continue
    l = Logline(m, line)
    lines.append(l)
  return lines