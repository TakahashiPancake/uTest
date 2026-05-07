"""
Copyright (c) 2026 Yidong Zhu

Repository: https://github.com/TakahashiPancake/uTest

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

"""
from utest.core.base import Base as _Base

class Proto(_Base):
  def __init__(self):
    super().__init__()
    self.case_ = self._case
    self.pass_ = self._pass
    self.fail_ = self._fail

