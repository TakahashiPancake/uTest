from .base import Base as _Base


class TestCase(_Base):
  """测试用例类"""

  @classmethod
  def setUpClass(cls) -> None:
    """
    初始化测试用例

    Returns:
      return: 无

    """
    # 实例化Base类，日志输出测试用例标题
    _Base()._case(cls.__name__)


  @classmethod
  def tearDownClass(cls) -> None:
    """
    析构测试用例

    Returns:
      return: 无

    """
    pass


  def setUp(self) -> None:
    """
    初始化测试单元

    Returns:
      return: 无

    """
    # 日志输出——测试单元标题
    self._unit(self.id().split('.')[-1])

    # 将测试单元默认置为通过
    self._unit_passed = True


  def tearDown(self) -> None:
    """
    析构测试单元

    Returns:
      return: 无

    """
    # 日志输出——测试单元是否通过
    if self._unit_passed:
      self._pass(f'{self._testMethodName} pass!')
    else:
      self._fail(f'{self._testMethodName} fail!')


  def _formatMessage(self,
    msg:         str | None,
    standardMsg: str
  ) -> str:
    """
    格式化错误信息

    - 将断言失败的原始消息与自定义消息合并，生成最终的错误信息

    Args:
      msg:         用户提供的自定义错误信息
      standardMsg: 框架生成的默认错误信息

    Returns:
      return:      最终的错误信息

    """
    # 将测试单元置为失败
    self._unit_passed = False

    return super()._formatMessage(msg, standardMsg)

