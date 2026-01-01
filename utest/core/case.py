from .base import Base


class TestCase(Base):
  """用例基类"""

  @classmethod
  def setUpClass(cls):
    """初始化用例"""

    # 实例化Base类，日志输出测试用例标题
    Base()._case(cls.__name__)


  @classmethod
  def tearDownClass(cls):
    """析构测试用例"""
    pass


  def setUp(self):
    """初始化测试单元"""

    # 日志输出——测试单元标题
    self._unit(self.id().split('.')[-1])

    # 将测试单元默认置为通过
    self._unit_passed = True


  def tearDown(self):
    """析构测试单元"""

    # 日志输出——测试单元是否通过
    if self._unit_passed:
      self._pass(f'{self._testMethodName} pass!')
    else:
      self._fail(f'{self._testMethodName} fail!')


  def _formatMessage(self, msg, standard_msg):
    """断言失败后将用例置为失败"""

    super()._formatMessage(msg, standard_msg)

    # 将测试单元置为失败
    self._unit_passed = False

