__all__ = ['patch', 'patch_logging_by_config_file', 'patch_unittest_by_config_file']

# 通过配置文件修补
from utest.patch.internal.logging_patch import patch_logging_by_config_file
from utest.patch.internal.unittest_patch import patch_unittest_by_config_file

from utest.patch.internal.unittest_patch import \
  LoaderPatch as UnitTestLoaderPatch,           \
  SuitePatch as UnitTestSuitePatch,             \
  ResultPatch as UnitTestResultPatch

def patch():
  UnitTestLoaderPatch()()
  UnitTestSuitePatch()()
  UnitTestResultPatch()()
