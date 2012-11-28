import os, hashlib, pickle

ARCHIVE_MD5SUM_PICKLE_FILENAME = 'md5sums.pickle'

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
    return None
  else:
    return pickle.load(open(path, 'rb'))
  
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