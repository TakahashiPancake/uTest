"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

"""
from enum import StrEnum as _StrEnum

# 配置文件夹
CONFIG_DIR = 'config'

# 日志文件夹
LOG_DIR    = 'log'

# 配置文件
class CONFIGs(_StrEnum):
  AUTOPIP  = 'autopip.json'
  LOGGING  = 'logging.yaml'
  UNITTEST = 'unittest.yaml'

# 日志文件
class LOGs(_StrEnum):
  AUTOPIP = 'autopip.log'

