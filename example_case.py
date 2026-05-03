###############################
##### 示例: 测试用例编写方法
###############################


# 1. 测试用例的基本编写方法

# 1.1. 导入测试用例类
from utest import TestCase

# 1.2. 编写测试用例
# - 类: 继承自utest.TestCase
class TEST_CASE_EXAMPLE_001(TestCase):

  # 1.2.1. 前置条件
  # - precondition()方法: 测试用例（测试单元）的前置条件
  def precondition(self):
    self.info('这里是一些前置步骤')
    ...

  # 1.2.2. 测试步骤
  # - testcase()方法: 测试用例（测试单元）的操作步骤
  def testcase(self):
    self.info('这里是一些测试步骤')
    ...

  # 1.2.3. 后置条件
  # - postcondition()方法: 测试用例（测试单元）的后置条件
  def postcondition(self):
    self.info('这里是一些后置步骤')
    ...

  # 1.2.4. 此外若需要给整个测试类添加前置条件和后置条件:
  # - 可使用 precondition_class()方法 和 postcondition_class()方法，
  #   但比较难用，不推荐使用
  @classmethod
  def precondition_class(cls) -> None:
    ...

  @classmethod
  def postcondition_class(cls) -> None:
    ...


# 2. 输出测试日志

class TEST_CASE_EXAMPLE_002(TestCase):

  def testcase(self):

    # 2.1. 日志

    # 2.1.1. 输出测试步骤
    self.step(1, '测试步骤 1')
    self.step(2, '测试步骤 2')
    self.step(3, '测试步骤 3')

    # 2.2. 输出日志

    # 2.2.1. 输出提示信息
    self.info('这是一行提示信息。')

    # 2.2.2. 输出警告信息
    self.warn('这是一行警告信息。')

    # 2.2.3. 输出错误信息
    self.error('这是一行错误信息。')

    # 2.2.4. 输出调试信息
    # - 由于debug方法被占用，所以输出调试信息方法更名为 trace()
    self.trace('这是一行调试信息。')

    # 2.2.5. 输出致命错误信息
    # - 致命错误发生时，测试用例（测试单元）置为失败
    self.fatal('这是一行致命错误信息。【致命错误发生时，测试用例（测试单元）置为失败】')

    ...

# 3. 一个测试用例含有多个测试单元的编写方式

class TEST_CASE_EXAMPLE_003(TestCase):

  # - 一个测试用例有多个测试单元时，
  #   每个测试单元用 'unit_' 打头命名

  # 例:

  # 测试单元 1
  def unit_001(self):
    self.info('这是第 1 个测试单元')
    ...

  # 测试单元 2
  def unit_002(self):
    self.info('这是第 2 个测试单元')
    ...

  # 测试单元 3
  def unit_003(self):
    self.info('这是第 3 个测试单元')
    ...

  # 注意！
  # - 每个测试单元执行之前都会执行 同一个precondition()方法 和 同一个postcondition()方法，
  #   若需要在所有测试单元执行之前执行一次前置条件，并在所有测试单元执行之后执行一次后置条件，
  #   则需要编写 precondition_class()方法 和 postcondition_class()方法

# 4. 断言
# utest.TestCase继承自 unittest.TestCase，
# 所以 utest.TestCase内 可使用所有的 unittest的断言方法

class TEST_CASE_EXAMPLE_004(TestCase):

  # 例:

  def unit_001(self):
    # 编写第 1 个断言
    self.info('第 1 个断言')
    self.assertTrue(True, '断言 1')
    ...

  def unit_002(self):
    # 编写第 2 个断言
    self.info('第 2 个断言')
    self.assertTrue(False, '断言 2')
    ...

# 5. 编写动作 (Action)
# - Action类内，可使用 utest.TestCase 的日志方法、断言方法

# 5.1. 导入 Action类
from utest import Action

# 5.2. 编写一个动作类
class Test_Action(Action):
  def action_001(self):
    # 5.2.1. 编写一些日志
    self.info('这是一个Action类内日志')

    # 5.2.2. 编写一些断言
    self.fail('这是一个Action类内的断言')

  ...

# 5.3. 实例化 Action类
test_action = Test_Action()

# 5.4. 在测试用例内使用 Action实例 的方法
class TEST_CASE_EXAMPLE_005(TestCase):
  def testcase(self):
    # 例:
    # - 在测试用例内使用 Action实例 的方法
    test_action.action_001()

    ...

