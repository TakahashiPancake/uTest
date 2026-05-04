__all__ = ['TestCase', 'Action', 'saving_path', 'TextTestExecutor', 'HTMLTestExecutor']


import utest.meta as _meta
import utest.util.path as _path

# 安装模块
from utest.feature.autopip import autopip as _autopip
_autopip.main(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.AUTOPIP
  ))
)

# 修补软件包
from utest.patch.internal import patch as _internal_patch
_internal_patch()

# 修补logging
from utest.patch.internal import \
  patch_logging_by_config_file as _patch_logging_by_config_file
_patch_logging_by_config_file(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.LOGGING
  ))
)

# 修补unittest
from utest.patch.internal import \
  patch_unittest_by_config_file as _patch_unittest_by_config_file
_patch_unittest_by_config_file(
  config_path = _path.framework.abs_path(_path.join(
    _meta.CONFIG_DIR, _meta.CONFIGs.UNITTEST
  ))
)

# 修补外部库
from utest.patch.external import patch as _external_patch
_external_patch()

# 设定命令行编码为UTF-8
from utest.util.system import system as _system
_system.set_cmd_encoding('utf-8')

# 导入模块
from utest.core.case import TestCase
from utest.core.action import Action
from utest.executor.executor import TextTestExecutor, HTMLTestExecutor
import utest.public.variable.path as _active_paths

def saving_path() -> str | None:
  """保存路径"""
  return _active_paths.saving_path

