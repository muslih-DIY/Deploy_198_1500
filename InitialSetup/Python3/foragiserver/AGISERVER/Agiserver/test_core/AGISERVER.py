#!/usr/bin/python3
import re
import threading
import time
import sys
import pystrix

from Agiserver.test_core.AgiModels import ComplaintAgi
from Agiserver.test_core.Modules import LogQ

Agiregister={'complaintAgi' : ComplaintAgi()}

class FastAGIServer(threading.Thread):

    """

    A simple thread that runs a FastAGI server forever.

    """

    _fagi_server = None #The FastAGI server controlled by this thread



    def __init__(self,host='127.0.0.1', port=4573, daemon_threads=True, debug=False):

        threading.Thread.__init__(self)
        self.daemon = daemon_threads
        self._fagi_server = pystrix.agi.FastAGIServer(
                                        interface=host,
                                        port=int(port),
                                        daemon_threads=daemon_threads,
                                        debug=debug)
        print(f'server listen on {port} and  interface {host}')

        for name,handler in Agiregister.items():
            self._fagi_server.register_script_handler(re.compile(name),handler.Agihandler)


    def kill(self):

        self._fagi_server.shutdown()



    def run(self):

        self._fagi_server.serve_forever()







if __name__ == '__main__':
    import  sys
    args =[i.split('=') for i in sys.argv[1:]]
    args = {a:b for a,b in args if a in ['host','port']}

    fastagi_core = FastAGIServer(**args,daemon_threads=False)

    fastagi_core.start()
    print('agiserver  ready')
    LogQ.start()
    print('logger  ready')

    while fastagi_core.is_alive():
    
        

        #In a larger application, you'd probably do something useful in another non-daemon

        #thread or maybe run a parallel AMI server

        time.sleep(1)


    fastagi_core.kill()
    print('killed grace shutdown')
    LogQ.stop_gracefully()