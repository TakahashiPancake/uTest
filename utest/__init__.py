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

# 修补软件包
from utest.patch.internal import patcher as _patcher_internal

# 修补框架
_patcher_internal.patch_framework()

# 修补logging
_patcher_internal.patch_logging_by_config_file(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.LOGGING
  ))
)

# 修补unittest
_patcher_internal.patch_unittest()
_patcher_internal.patch_unittest_by_config_file(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.UNITTEST
  ))
)

from utest.patch.external import PatchHTMLTestRunner as _PatchHTMLTestRunner

# 修补html-testrunner
_PatchHTMLTestRunner()()

# 设定命令行编码为UTF-8
from utest.util.system import system as _system
_system.set_cmd_encoding('utf-8')

# 导入模块
from .core.case import TestCase
from .core.action import Action
from .executor.executor import TextTestExecutor, HTMLTestExecutor

