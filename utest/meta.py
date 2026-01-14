"""
元数据

"""
from enum import StrEnum as _StrEnum


CONFIG_DIR = 'config'
LOG_DIR    = 'log'

class CONFIGs(_StrEnum):
  AUTOPIP  = 'autopip.json'
  LOGGING  = 'logging.yaml'
  UNITTEST = 'unittest.yaml'

class LOGs(_StrEnum):
  AUTOPIP = 'autopip.log'

