from utest.patch.base import PatcherBase as _PatcherBase
from utest.core.case import TestCase as _TestCase


class FrameworkPatch(_PatcherBase):

  _class_to_patch = _TestCase

  @staticmethod
  def tear_down(self) -> None:
    _ = self
    ...

