
class Appnames:
    def __init__(self):
        self.names = {}
        f = open('appnames.txt', 'r')
        for line in f:
            s = line.split('=')
            self.names[s[0].strip()] = s[1].strip()
        f.close()
            
            
            
    def getname(self,n):
        if self.names.has_key(n):
            return self.names[n]
        else:
            return None

