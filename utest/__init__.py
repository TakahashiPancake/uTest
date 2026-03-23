__all__ = ['TestCase', 'Action', 'TextTestExecutor', 'HTMLTestExecutor']


import utest.meta as _meta
import utest.util.path as _path


# 安装模块
from .feature.autopip import autopip as _autopip
_autopip.main(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.AUTOPIP
  ))
)


# 修补模块
from .core.patch import patcher as _patcher
_patcher.patch_logging_by_config_file(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.LOGGING
  ))
)
_patcher.patch_unittest_by_config_file(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.UNITTEST
  ))
)


# 导入模块
from .core.case import TestCase
from .core.action import Action
from .executor.executor import TextTestExecutor, HTMLTestExecutor

