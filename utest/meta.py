"""
定义元数据

"""
class RootMeta(object):
  CONFIG_DIR = 'config'
  LOG_DIR    = 'log'

  class CONFIGs(object):
    AUTOPIP = 'autopip.json'
    LOGGING = 'logging.yaml'
    UNITTEST = 'unittest.yaml'

  class LOGs(object):
    AUTOPIP = 'autopip.log'

