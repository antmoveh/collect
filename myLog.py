import logging
from logging.handlers import RotatingFileHandler
import os


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='f:/test.log',
#                     filemode='w')

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     )
#
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)


# Rthandler = RotatingFileHandler('f:/myapp.log', maxBytes=10*1024*1024, backupCount=5)
# Rthandler.setLevel(logging.WARNING)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# Rthandler.setFormatter(formatter)
# logging.getLogger('').addHandler(Rthandler)


def get_handler(filename=''):
    print(filename)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(threadName)s %(levelname)s: %(message)s')
    handler = RotatingFileHandler(filename=filename, mode='a', maxBytes=100*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    return handler


handler = get_handler(filename=os.getcwd()+'\log.log')
handler.setLevel(logging.INFO)
logging.getLogger('').addHandler(handler)


logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')