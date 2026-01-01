__all__ = ['TestCase', 'Action']

# 安装模块
from .feature.autopip import autopip
autopip.main(
  config_path = 'config/autopip.json',
  upgrade     = False
)

# 修补模块
from .core.patch import patcher
patcher.patch_logging(
  config_path = 'config/logging.yaml'
)
patcher.patch_unittest(
  config_path = 'config/unittest.yaml'
)

# 导入模块
from .core.case import TestCase
from .core.action import Action

