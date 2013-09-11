
class Logger():
    def log(self, msg, verbosity = 1):
        print msg
        
    def warn(self, msg, priority = 0):
        pass
        
logger = Logger()    