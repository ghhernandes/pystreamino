import logging

import os
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

log = logging
log.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s'
                #,filename="\\{0}\\app.log".format(CURRENT_PATH),
                #filemode='w'
                )

log.debug("Iniciado.")
log.debug("CURRENT_PATH: {0}".format(CURRENT_PATH))
