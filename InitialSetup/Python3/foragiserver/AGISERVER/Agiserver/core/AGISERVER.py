
import re
import threading
import pystrix
from typing import List


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
        print(f'Server set to listen on {port} and  interface {host}')


    def kill(self):

        self._fagi_server.shutdown()

    def register_handles(self,handlers: List[tuple]):
        for handler in handlers:
            endpoint,method = handler
            self._fagi_server.register_script_handler(re.compile(endpoint),method.Agihandler)


    def run(self):

        self._fagi_server.serve_forever()