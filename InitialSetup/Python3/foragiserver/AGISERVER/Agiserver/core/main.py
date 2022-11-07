import sys
import time
from Agiserver.core import (
    Logger,AGISERVER,AgiModels)


Agiregister = [
                ('complaintAgi' , AgiModels.ComplaintAgi()),
                ('appealAgiGet' , AgiModels.AppealDocketAgi()),
                ('AppealAgi' , AgiModels.AppealAgi()),
                ('Bill',AgiModels.BillStatusAgi()),
                ('vip',AgiModels.VipCheckingAgi()),
                ('newnumber',AgiModels.ChdNoAgi()),
                ('OtpValidate',AgiModels.OtpVerification()),
                ('RMNCaptureMenu',AgiModels.RMNCaptureMenu())
              ]

def collect_args():
    args =[i.split('=') for i in sys.argv[1:]]
    return {a:b for a,b in args if a in ['host','port']}


if __name__ == '__main__':
    
    args = collect_args()

    fastagi_core = AGISERVER.FastAGIServer(**args,daemon_threads=False)
    Logger.LogQ.start()
    print('Logger started')

    ## register Agi services to the Server
    fastagi_core.register_handles(Agiregister)
    
    fastagi_core.start()

    print('Server started')

    while fastagi_core.is_alive():

        time.sleep(1)

    fastagi_core.kill()

    Logger.LogQ.stop_gracefully()