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
   (?P<log_tag>%s):\s+(?P<json>.*)$"""
  
  def __init__(self, match, line):
    self.device = match.group('hashed_ID')
    self.datetime = datetime.datetime.strptime(match.group('datetime'), '%Y-%m-%d %H:%M:%S.%f')
    self.log_tag = match.group('log_tag').strip()
    self.line = line.strip()
    self.log_message = match.group('json').strip()
    try:
      self.json = json.loads(match.group('json').strip())
    except:
      self.json = None
    self.label = None
    
  def __str__(self):
    return self.line
  
class LogFilter(object):
  
  DEFAULT_FILTER_PROCESSES = 4
  
  @classmethod
  def load(cls, **kwargs):
    if os.path.exists(cls.get_pickle_path()):
      p = cPickle.load(open(cls.get_pickle_path(), 'rb'))
    else:
      p = cls(**kwargs)

    if not p.filtered:
      p.filter()
      
    if not p.processed:
      p.process()
      p.store()

    return p
  
  def store(self):
    cPickle.dump(self, open(self.get_pickle_path(), 'wb'), cPickle.HIGHEST_PROTOCOL)
  
  @classmethod
  def remove(cls):
    try:
      os.remove(cls.get_pickle_path())
    except OSError:
      pass
    
  @classmethod
  def get_log_directory(cls):
    return os.environ['MOBISYS13_DATA']
  
  @classmethod
  def get_data_directory(cls):
    return os.path.join(cls.get_log_directory(), cls.__name__.lower())
  
  @classmethod
  def get_pickle_path(cls):
    return os.path.join(cls.get_data_directory(), 'processed.pickle')
  
  @classmethod
  def get_log_files(cls):
    return sorted([os.path.join(cls.get_log_directory(), f) for f in dircache.listdir(cls.get_log_directory()) if os.path.splitext(f)[1] == '.out'],
            key=lambda k: int(os.path.splitext(os.path.basename(k))[0]))
  
  @classmethod
  def get_data_files(cls):
    return sorted([os.path.join(cls.get_data_directory(), f) for f in dircache.listdir(cls.get_data_directory()) if os.path.splitext(f)[1] == '.dat'],
            key=lambda k: int(os.path.splitext(os.path.basename(k))[0]))
    
  @classmethod
  def log_file_to_data_file(cls, path):
    return os.path.join(cls.get_data_directory(), os.path.splitext(os.path.basename(path))[0] + '.dat')
    
  def __init__(self, tags, duplicates=False, verbose=False):
    
    if os.environ.has_key('MOBISYS13_FILTER_PROCESSES'):
      self.filter_processes = int(os.environ['MOBISYS13_FILTER_PROCESSES'])
    else:
      self.filter_processes = self.DEFAULT_FILTER_PROCESSES
      
    self.tags = tags
    
    self.pattern = re.compile(Logline.LOGLINE_PATTERN_STRING % ("|".join([r"""%s\s*""" % (tag,) for tag in self.TAGS]),), re.VERBOSE)
    
    self.devices = set([])
    self.start_time = None
    self.end_time = None
    
    self.verbose = verbose
    self.duplicates = duplicates
    
    self.filtered = False
    self.processed = False
    try:
      os.mkdir(self.get_data_directory())
    except OSError:
      pass
  
  def test_labels(self, line_count=10000):
    line_set = set([])
    labels = set([])
    for line in open(self.get_log_files()[0], 'rb'):
      m = self.pattern.match(line)
      if m == None:
        continue
      if line in line_set:
        continue
      l = Logline(m, line)
      label = self.label_line(l)
      if label == None:
        continue
      print label, line.strip()
      line_set.add(line)
      labels.add(label)
      if len(line_set) >= line_count:
        break
    print labels
          
  def filter(self, refilter=False):
    if self.filtered and not refilter:
      return
    
    pool = Pool(processes=self.filter_processes)
    log_files = self.get_log_files()
    data_files = [self.log_file_to_data_file(f) for f in log_files]
    pool.map(do_filter_star, zip(log_files, data_files,
                                 itertools.repeat(self.pattern),
                                 itertools.repeat(self.label_line),
                                 itertools.repeat(self.verbose),
                                 itertools.repeat(self.duplicates),
                                 itertools.repeat(self.__class__.__name__)))
    pool.close()
    pool.join()
    
    self.filtered = True
    self.processed = False
    self.store()
    
  def process_loop(self):
    if self.processed:
      return
    
    for data_file in self.get_data_files():
      if self.verbose:
        print >>sys.stderr, "Processing %s" % (data_file,)
      
      lines = cPickle.load(open(data_file, 'rb'))
      for line in lines:
        self.devices.add(line.device)
        if self.start_time == None:
          self.start_time = line.datetime
        self.end_time = line.datetime
        self.process_line(line)
    
    self.processed = True
      
def do_filter_star(l_d_p_l_v):
  return do_filter(*l_d_p_l_v)

def do_filter(log_file, data_file, pattern, label_line, verbose, duplicates, name):
    if verbose:
      print >>sys.stderr, "%s: filtering %s" % (name, log_file,)
    lines = []
    device_lines = {}
    
    count = 0
    duplicate_count = 0
    
    log_f = open(log_file, 'rb')
    for line in log_f:
      m = pattern.match(line)
      if m == None:
        continue
      l = Logline(m, line)
      
      if not duplicates and device_lines.has_key(l.device):
        if device_lines[l.device].datetime == l.datetime and \
           device_lines[l.device].log_message == l.log_message:
          duplicate_count += 1
          continue
      device_lines[l.device] = l
      
      label = label_line(l)
      if label == None:
        continue
      count += 1
      l.label = label
      lines.append(l)
    log_f.close()
    
    if not duplicates and verbose:
      print >>sys.stderr, "%s: %d duplicates, %d labeled." % (name, duplicate_count, count)
      
    data_f = open(data_file, 'wb')
    cPickle.dump(lines, data_f, cPickle.HIGHEST_PROTOCOL)
    data_f.close()
    del(data_f)
    del(lines)
