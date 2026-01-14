__all__ = ['TestCase', 'Action']


import utest.meta as _meta
import utest.util.path as _path


# 安装模块
from .feature.autopip import autopip
autopip.main(
  config_path = _path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.AUTOPIP
  )
)


# 修补模块
from .core.patch import patcher
patcher.patch_logging(
  config_path = _path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.LOGGING
  )
)
patcher.patch_unittest(
  config_path = _path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.UNITTEST
  )
)


# 导入模块
from .core.case import TestCase
from .core.action import Action

