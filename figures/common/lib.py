import os, cPickle, re, json, dircache, threading, Queue, datetime

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
  DATETIME_PATTERN_STRING = r"""%Y-%m-%d %H:%M:%S.%f"""
  
  def __init__(self, match, line):
    self.device = match.group('hashed_ID')
    self.datetime = datetime.datetime.strptime(match.group('datetime'), self.DATETIME_PATTERN_STRING)
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
  FILTERS = []
  NUM_QUEUES = 1
  THREADS_PER_QUEUE = 1
  
  def __init__(self, verbose=False):
    self.directory = self._directory()
    self.path = self._path()
    
    self.sorted_files = sorted([os.path.join(self.directory, f) for f in dircache.listdir(self.directory) if os.path.splitext(f)[1] == '.out'],
                               key=lambda k: int(os.path.splitext(os.path.basename(k))[0]))
    
    self.devices = set([])
    self.start_time = None
    self.end_time = None
    self.verbose = verbose
    
    self.filtered = False
    self.processed = False
  
  @classmethod
  def _directory(cls):
    return os.environ['MOBISYS13_DATA']
  
  @classmethod
  def _path(cls):
    return os.path.join(cls._directory(), cls.__name__.lower() + '.dat')
  
  @classmethod
  def load(cls, **kwargs):
    if os.path.exists(cls._path()):
      return cPickle.load(open(cls._path(), 'rb'))
    else:
      return cls(**kwargs)
    
  def store(self):
    cPickle.dump(self, open(self._path(), 'wb'), cPickle.HIGHEST_PROTOCOL)
  
  def process(self):
    self.process_loop()
  
  @classmethod
  def reset(cls):
    try:
      os.remove(cls._path())
    except OSError:
      pass
  
  def filter(self):
    pass
  
  def process_loop(self):
    
    log_tag_string = "|".join([r"""%s\s*""" % (tag,) for tag in self.TAGS])
    logline_pattern_string = Logline.LOGLINE_PATTERN_STRING % (log_tag_string,)
    logline_pattern = re.compile(logline_pattern_string, re.VERBOSE)
    
    if self.NUM_QUEUES > 1:
      queues = [Queue.Queue()] * self.NUM_QUEUES
      current_queue = 0
      device_queues = {}
    
      for queue in queues:
        for unused in range(self.THREADS_PER_QUEUE):
          t = LogProcessor(queue, self)
          t.setDaemon(True)
          t.start()
    
    for filename in self.sorted_files:
      if self.verbose:
        print filename
      for line in open(filename, 'rb'):
        m = logline_pattern.match(line)
        if m == None:
          continue    
        l = Logline(m, line)
        self.devices.add(l.device)
        if self.start_time == None:
          self.start_time = l.datetime
        self.end_time = l.datetime
        
        if self.NUM_QUEUES > 1:
          if not device_queues.has_key(l.device):
            device_queues[l.device] = queues[current_queue]
            current_queue = (current_queue + 1) % self.NUM_QUEUES
          device_queues[l.device].put(l)
        else:
          self.process_line(l)
    
    if self.NUM_QUEUES > 1:
      for queue in queues:
        queue.join()  
        
class LogProcessor(threading.Thread):
  def __init__(self, queue, logfilter):
    threading.Thread.__init__(self)
    self.queue = queue
    self.logfilter = logfilter
    
  def run(self):
    while True:
      l = self.queue.get()
      self.logfilter.process_line(l)
      self.queue.task_done()