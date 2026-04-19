from utest import TestCase
from example_action import test_action

class TC_001_Framework(TestCase):
  def unit_001(self):
    self.step('1. 单元测试，导入uTest包')
    self.assertTrue(True, 'test_01')

  def unit_002(self):
    self.step('2. 单元测试，测试用例断言失败')
    self.assertTrue(False, 'test_02')

  def unit_003(self):
    self.step('3. 单元测试，创建Action实例')
    test_action.action_03()


class TC_002_Framework(TestCase):
  def unit_001(self):
    self.step('1. 单元测试，导入uTest包')
    self.assertTrue(True, 'test_01')

  def unit_002(self):
    self.step('2. 单元测试，测试用例断言失败')
    self.assertTrue(False, 'test_02')

  def unit_003(self):
    self.step('3. 单元测试，创建Action实例')
    test_action.action_03()

