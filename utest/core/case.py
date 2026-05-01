from unittest import TextTestResult as _TextTestResult
from utest.core.base import Base as _Base
from utest.public.proto import proto as _proto
from utest.public.stream import sync_output_stream as _sync_output_stream


class TestCase(_Base):
  """测试用例类"""

  @classmethod
  def pre_case(cls) -> None:
    """每个测试用例之前执行的方法"""
    ...

  def pre_unit(self) -> None:
    """每个测试单元之前执行的方法"""
    ...

  def post_unit(self) -> None:
    """每个测试单元之后执行的方法"""
    ...

  @classmethod
  def post_case(cls) -> None:
    """每个测试用例之后执行的方法"""
    ...

  @classmethod
  def setUpClass(cls) -> None:
    """
    初始化测试用例

    Returns:
      return: 无

    """
    # 日志输出测试用例标题
    _proto.case_(cls.__name__)
    # 执行测试用例前置步骤
    cls.pre_case()


  @classmethod
  def tearDownClass(cls) -> None:
    """
    析构测试用例

    Returns:
      return: 无

    """
    # 执行测试用例后置步骤
    cls.post_case()


  def setUp(self) -> None:
    """
    初始化测试单元

    Returns:
      return: 无

    """
    # 日志输出: 测试单元标题
    self._unit(self.id().split('.')[-1])
    print(_TextTestResult.separator2, file = _sync_output_stream)
    # 执行测试单元前置步骤
    self.info('测试单元前置步骤:')
    self.pre_unit()
    print(_TextTestResult.separator2, file=_sync_output_stream)


  def tearDown(self) -> None:
    """
    析构测试单元

    Returns:
      return: 无

    """
    # 执行测试单元后置步骤
    print(_TextTestResult.separator2, file=_sync_output_stream)
    self.info('测试单元后置步骤:')
    print(_TextTestResult.separator2, file=_sync_output_stream)
    self.post_unit()


