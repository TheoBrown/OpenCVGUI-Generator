import os
import socket
import sys



rdir = os.getcwd()
# sys.stderr = sys.stdout

        
hostname = socket.gethostname()
rootpath = os.getcwd()


logLevel = 'debug'
consoledbg = 'debug'

datapath = rootpath + '/Data/'
resultpath = datapath + 'Results/'

logpath = rootpath + '/Logs/'
templatepath = datapath+'templates/'
tempimg = templatepath+'img/'
tempinfo = templatepath+'info/'
recordDB = True
#Note = rootlog only goes to stream above warning
datadir = {'dante-EX58-UD4P':{'db':'iReport',
                     'picklepath':'/var/www/iReport/data/',
                     'debug':True
                     },
        'li614-103':{'db':'Diagnostics', 
                     'picklepath' : '/var/www/remoteProcessor/data/',
                    'debug':False

                     }
        }


from PyUtils.Files import ensure_dir

database = datadir[hostname]['db']
picklepath = datadir[hostname]['picklepath']
isDebug = datadir[hostname]['debug']
ensure_dir(logpath)
