from utest import TestCase
from unit_test_action import TestAction

class TC_Framework(TestCase):
  def unit_001(self):
    self.step('1. 单元测试，导入uTest包')
    self.assertTrue(True, '123')

  def unit_002(self):
    self.step('1. 单元测试，创建Action实例')
    TestAction().action()


