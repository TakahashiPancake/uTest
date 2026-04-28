__all__ = ['patch']

from utest.patch.framework.framework_patch import TestCasePatch

def patch():
  TestCasePatch()()

