from utest.core.base import Base as _Base


class TestCase(_Base):
  """测试用例类"""

  @classmethod
  def setUpClass(cls) -> None:
    """
    初始化测试用例

    Returns:
      return: 无

    """
    # 日志输出测试用例标题
    from utest.public.proto import proto
    proto.case_(cls.__name__)


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


  def tearDown(self) -> None:
    """
    析构测试单元

    Returns:
      return: 无

    """
    ...


