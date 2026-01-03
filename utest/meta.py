"""
定义元数据

"""
class RootMeta:
  CONFIG_DIR = 'config'
  LOG_DIR    = 'log'

  class CONFIGs:
    AUTOPIP  = 'autopip.json'
    LOGGING  = 'logging.yaml'
    UNITTEST = 'unittest.yaml'

  class LOGs:
    AUTOPIP = 'autopip.log'

