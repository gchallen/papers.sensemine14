import os, hashlib, cPickle, re, json, argparse
from dateutil.parser import parse

ARCHIVE_MD5SUM_PICKLE_FILENAME = 'md5sums.pickle'

class AutoDict(dict):
  def __getitem__(self, item):
    try:
      return dict.__getitem__(self, item)
    except KeyError:
      value = self[item] = type(self)()
      return value
          
class LibraryException(Exception):
  def __init__(self, value):
    self.value = value
  
  def __str__(self):
    return repr(self.value)

def check_directory(directory):
  if directory == None:
    if not os.environ.has_key('MOBISYS13_DATA'):
      raise LibraryException("MOBISYS13_DATA environment variable not set.")
    else:
      directory = os.environ['MOBISYS13_DATA'] 
  if not os.path.isdir(directory):
    raise LibraryException("Path that should be a directory is not.")
  return directory

def load_hash(directory=None):
  directory = check_directory(directory)
  path = os.path.join(directory, ARCHIVE_MD5SUM_PICKLE_FILENAME)
  if not os.path.exists(path):
    add_md5sum(directory)
  return cPickle.load(open(path, 'rb'))
  
def hash_logs(directory=None):
  directory = check_directory(directory)
  md5sums = {}
  for dirname, unused, filenames in os.walk(directory):
    for filename in filenames:
      if os.path.splitext(filename)[1] != '.out':
        continue
      md5 = hashlib.md5()
      with open(os.path.join(dirname, filename), 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
          md5.update(chunk)
      md5sums[filename] = md5.hexdigest()
  return md5sums

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

class LogFilter:
  def __init__(self, tags, directory=None):
    self.tags = tags
    self.directory = check_directory(directory)
    self.logs_md5sums = load_hash(directory)
    
  def sorted_keys(self):
    return sorted(self.logs_md5sums.keys(), key=lambda k: int(os.path.splitext(k)[0]))
  
  def generate_loglines(self):
    
    log_tag_string = "|".join([r"""%s\s*""" % (tag,) for tag in self.tags])
    logline_pattern_string = Logline.LOGLINE_PATTERN_STRING % (log_tag_string,)
    logline_pattern = re.compile(logline_pattern_string, re.VERBOSE)
    
    for filename in self.sorted_keys():
      for line in open(os.path.join(self.directory, filename), 'rb'):
        m = logline_pattern.match(line)
        if m != None:
          yield Logline(m, line)

def add_md5sum(archive_directory):
  cPickle.dump(hash_logs(archive_directory),
              open(os.path.join(archive_directory, ARCHIVE_MD5SUM_PICKLE_FILENAME), 'wb'),
              cPickle.HIGHEST_PROTOCOL)

if __name__=='__main__':          
  parser = argparse.ArgumentParser(description="util package for MobiSys'13 graphs")
  parser.add_argument('--md5sum', dest='md5sum', action='store', default=None, help='Add md5sum pickle to existing archive.')
  args = parser.parse_args()
      
  if args.md5sum != None:
    add_md5sum(args.md5sum)