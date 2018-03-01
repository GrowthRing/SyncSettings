# -*- coding: utf-8 -*-

import logging
import os
from sync_settings.libs import path

logger_path = path.join(os.path.expanduser('~'), '.sync_settings.log')
logging.basicConfig(
    filename=logger_path,
    level=logging.DEBUG,
    format='[%(asctime)-15s] [%(filename)s:%(lineno)d] (%(levelname)s) %(message)s'
)
logger = logging.getLogger(__name__)
