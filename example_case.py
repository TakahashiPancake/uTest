from utest import TestCase, HTMLTestExecutor
from example_action import TestAction

class TC_001_Framework(TestCase):
  def unit_001(self):
    self.step('1. 单元测试，导入uTest包')
    self.assertTrue(True, '123')

  def unit_002(self):
    self.step('2. 单元测试，测试用例断言失败')
    self.assertTrue(False, '123')

  def unit_003(self):
    self.step('3. 单元测试，创建Action实例')
    TestAction().action()


class TC_002_Framework(TestCase):
  def unit_001(self):
    self.step('1. 单元测试，导入uTest包')
    self.assertTrue(True, '123')

  def unit_002(self):
    self.step('2. 单元测试，测试用例断言失败')
    self.assertTrue(False, '123')

  def unit_003(self):
    self.step('3. 单元测试，创建Action实例')
    TestAction().action()


if __name__ == '__main__':
  executor = HTMLTestExecutor()
  executor.load_case(TC_001_Framework)
  executor.load_case(TC_002_Framework)
  executor.run()

