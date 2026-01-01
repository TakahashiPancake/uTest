from .case import TestCase
from .base import Base
import inspect


class Action(object):
  """动作基类"""


  # 测试用例实例
  _case_instance = None


  def __init__(self):
    """
    构造函数

    1. 目的是获取测试用例实例

    2. 从测试用例实例导入日志方法和断言方法

    Returns:
      return: None

    """
    self._case_instance = self._get_case_instance()

    # 导入日志方法
    self._get_logging_methods_from_a_case(self._case_instance)

    # 导入断言方法
    self._get_assertion_methods_from_a_case(self._case_instance)


  @staticmethod
  def _get_case_instance() -> TestCase:
    """
    获取测试用例实例

    Returns:
      return: 测试用例实例

    """
    curr_frame = inspect.currentframe()

    # 遍历调用栈寻找测试用例实例
    while curr_frame.f_back.f_locals.get('self') is not None:

      # 获取上一帧
      prev_frame = curr_frame.f_back

      # 获取调用者实例
      caller_instance = prev_frame.f_locals.get('self')

      # 截止条件：
      # - 调用者实例是一个测试用例（框架定义的测试用例有get_logger方法）
      if hasattr(caller_instance, 'get_logger'):
        case_instance = caller_instance
        break

      curr_frame = prev_frame

    # 如果没有找到测试用例实例，则创建一个Base实例当作测试用例实例
    else:
      case_instance = Base()

    return case_instance


  def _get_logging_methods_from_a_case(
      self,
      case: TestCase
  ) -> None:
    """
    导入日志方法

    Args:
      case:   测试用例

    Returns:
      return: 无

    """
    self.trace   = case.trace
    self.info    = case.info
    self.warning = case.warning
    self.error   = case.error
    self.fatal   = case.fatal
    self.step    = case.step


  def _get_assertion_methods_from_a_case(
    self,
    case: TestCase
  ) -> None:
    """
    导入断言方法

    Args:
      case:   测试用例

    Returns:
      return: 无

    """
    self.assertTrue           = case.assertTrue
    self.assertFalse          = case.assertFalse
    self.assertEqual          = case.assertEqual
    self.assertNotEqual       = case.assertNotEqual
    self.assertAlmostEqual    = case.assertAlmostEqual
    self.assertNotAlmostEqual = case.assertNotAlmostEqual
    self.assertLess           = case.assertLess
    self.assertLessEqual      = case.assertLessEqual
    self.assertGreater        = case.assertGreater
    self.assertGreaterEqual   = case.assertGreaterEqual
    self.assertIsNone         = case.assertIsNone
    self.assertSequenceEqual  = case.assertSequenceEqual
    self.assertDictEqual      = case.assertDictEqual
    self.assertListEqual      = case.assertListEqual
    self.assertTupleEqual     = case.assertTupleEqual
    self.assertSetEqual       = case.assertSetEqual
    self.assertCountEqual     = case.assertCountEqual
    self.assertMultiLineEqual = case.assertMultiLineEqual
    self.assertIn             = case.assertIn
    self.assertNotIn          = case.assertNotIn
    self.assertIs             = case.assertIs
    self.assertIsNot          = case.assertIsNot
    self.assertRegex          = case.assertRegex
    self.assertNotRegex       = case.assertNotRegex
    self.assertRaises         = case.assertRaises
    self.assertWarns          = case.assertWarns
    self.assertWarnsRegex     = case.assertWarnsRegex
    self.assertLogs           = case.assertLogs
    self.assertIsInstance     = case.assertIsInstance
    self.assertNotIsInstance  = case.assertNotIsInstance

    # 弃用的方法
    try:
      self.failUnlessEqual        = case.failUnlessEqual
      self.assertEquals           = case.assertEquals
      self.failIfEqual            = case.failIfEqual
      self.assertNotEquals        = case.assertNotEquals
      self.failUnlessAlmostEqual  = case.failUnlessAlmostEqual
      self.assertAlmostEquals     = case.assertAlmostEquals
      self.failIfAlmostEqual      = case.failIfAlmostEqual
      self.assertNotAlmostEquals  = case.assertNotAlmostEquals
      self.failUnless             = case.failUnless
      self.assert_                = case.assert_
      self.failUnlessRaises       = case.failUnlessRaises
      self.failIf                 = case.failIf
      self.assertRaisesRegexp     = case.assertRaisesRegexp
      self.assertRegexpMatches    = case.assertRegexpMatches
      self.assertNotRegexpMatches = case.assertNotRegexpMatches

    except AttributeError:
      pass

