import sys as _sys
import inspect as _inspect
from typing import         \
  Any as _Any,             \
  AnyStr as _AnyStr,       \
  Callable as _Callable,   \
  Container as _Container, \
  Iterable as _Iterable,   \
  Mapping as _Mapping,     \
  NoReturn as _NoReturn,   \
  overload as _overload,   \
  ParamSpec as _ParamSpec, \
  Sequence as _Sequence,   \
  Set as _AbstractSet,     \
  TypeVar as _TypeVar
from re import Pattern as _Pattern
import warnings as _warnings
from unittest.case import _AssertRaisesContext, _AssertWarnsContext
import logging as _logging
from utest.core.case import TestCase as _TestCase
from utest.public.proto import proto as _proto


_E = _TypeVar('_E', bound=BaseException)
_P = _ParamSpec('_P')


class Action(object):
  """
  动作类

  - 在动作类中可以调用测试用例类中的日志方法以及断言方法

  """
  @staticmethod
  def _get_case_instance() -> _TestCase:
    """
    获取测试用例实例

    Returns:
      return: 测试用例实例

    """
    curr_frame = _inspect.currentframe()

    # 遍历调用栈寻找测试用例实例
    while curr_frame.f_back.f_locals.get('self') is not None:

      # 获取上一帧
      prev_frame = curr_frame.f_back

      # 获取调用者实例
      caller_instance = prev_frame.f_locals.get('self')

      # 截止条件：
      # - 调用者实例是一个测试用例
      if isinstance(caller_instance, _TestCase):
        case_instance = caller_instance
        break

      curr_frame = prev_frame

    # 如果没有找到测试用例实例，则使用公用测试用例实例
    else:
      case_instance = _proto

    return case_instance

  ####################
  ###   日志方法
  ####################

  def step(self, step: int, msg: str) -> None:
    """在日志中输出测试步骤"""
    self._get_case_instance().step(step = step, msg = msg)

  def trace(self, msg: str) -> None:
    """在日志中输出调试信息"""
    self._get_case_instance().trace(msg = msg)

  def info(self, msg: str) -> None:
    """在日志中输出一般信息"""
    self._get_case_instance().info(msg = msg)

  def warn(self, msg: str) -> None:
    """在日志中输出警告信息"""
    self._get_case_instance().warn(msg=msg)

  def warning(self, msg: str) -> None:
    """在日志中输出警告信息"""
    _warnings.warn(
      'warning()方法已弃用，请使用warn()方法',
      DeprecationWarning
    )
    self._get_case_instance().warning(msg = msg)

  def error(self, msg: str) -> None:
    """在日志中输出错误信息"""
    self._get_case_instance().error(msg = msg)

  def fatal(self, msg: str) -> None:
    """在日志中输出致命错误信息"""
    self._get_case_instance().fatal(msg = msg)


  ####################
  ###  测试用例方法
  ####################

  def id(self) -> str:
    return self._get_case_instance().id()


  ####################
  ###   断言方法
  ####################

  def fail(self, msg: _Any = None) -> _NoReturn:
    """将测试用例置为失败，并输出信息"""
    self._get_case_instance().fail(msg=msg)

  def assertEqual(self, first: _Any, second: _Any, msg: _Any = None) -> None:
    """若两个对象不相等，则测试用例失败"""
    self._get_case_instance().assertEqual(first, second, msg = msg)

  def assertNotEqual(self, first: _Any, second: _Any, msg: _Any = None) -> None:
    """若两个对象相等，则测试用例失败"""
    self._get_case_instance().assertNotEqual(first, second, msg = msg)

  def assertTrue(self, expr: _Any, msg: _Any = None) -> None:
    """若表达式为假，则测试用例失败"""
    self._get_case_instance().assertTrue(expr, msg = msg)

  def assertFalse(self, expr: _Any, msg: _Any = None) -> None:
    """若表达式为真，则测试用例失败"""
    self._get_case_instance().assertFalse(expr, msg = msg)

  def assertIs(self, expr1: object, expr2: object, msg: _Any = None) -> None:
    """若表达式1不是表达式2，则测试用例失败"""
    self._get_case_instance().assertIs(expr1, expr2, msg = msg)

  def assertIsNot(self, expr1: object, expr2: object, msg: _Any = None) -> None:
    """若表达式1是表达式2，则测试用例失败"""
    self._get_case_instance().assertIsNot(expr1, expr2, msg = msg)

  def assertIsNone(self, obj: object, msg: _Any = None) -> None:
    """若传入对象不是None，则测试用例失败"""
    self._get_case_instance().assertIsNone(obj, msg = msg)

  def assertIsNotNone(self, obj: object, msg: _Any = None) -> None:
    """若传入对象是None，则测试用例失败"""
    self._get_case_instance().assertIsNotNone(obj, msg = msg)

  def assertIn(self, member: _Any, container: _Iterable[_Any] | _Container[_Any], msg: _Any = None) -> None:
    """若元素不在容器内，则测试用例失败"""
    self._get_case_instance().assertIn(member, container, msg = msg)

  def assertNotIn(self, member: _Any, container: _Iterable[_Any] | _Container[_Any], msg: _Any = None) -> None:
    """若元素在容器内，则测试用例失败"""
    self._get_case_instance().assertNotIn(member, container, msg = msg)

  def assertIsInstance(self, obj: object, cls: type[object], msg: _Any = None) -> None:
    """若传入对象不是传入类的实例，则测试用例失败"""
    self._get_case_instance().assertIsInstance(obj, cls, msg = msg)

  def assertNotIsInstance(self, obj: object, cls: type[object], msg: _Any = None) -> None:
    """若传入对象是传入类的实例，则测试用例失败"""
    self._get_case_instance().assertNotIsInstance(obj, cls, msg = msg)

  def assertGreater(self, a, b, msg: _Any = None) -> None:
    """若a不大于b，则测试用例失败"""
    self._get_case_instance().assertGreater(a, b, msg = msg)

  def assertGreaterEqual(self, a, b, msg: _Any = None) -> None:
    """若a小于b，则测试用例失败"""
    self._get_case_instance().assertGreaterEqual(a, b, msg = msg)

  def assertLess(self, a, b, msg: _Any = None) -> None:
    """若a不小于b，则测试用例失败"""
    self._get_case_instance().assertLess(a, b, msg = msg)

  def assertLessEqual(self, a, b, msg: _Any = None) -> None:
    """若a大于b，则测试用例失败"""
    self._get_case_instance().assertLessEqual(a, b, msg = msg)

  @_overload
  def assertRaises(
    self,
    expected_exception: type[BaseException] | tuple[type[BaseException], ...],
    callable_: _Callable[..., object],
    *args: _Any,
    **kwargs: _Any,
  ) -> None:
    ...

  @_overload
  def assertRaises(
    self, expected_exception: type[_E] | tuple[type[_E], ...], *, msg: _Any = ...
  ) -> _AssertRaisesContext[_E]:
    ...

  def assertRaises(self, expected_exception, *args, **kwargs) -> _AssertRaisesContext[_E] | None:
    if 'callable_' not in kwargs:
      return self._get_case_instance().assertRaises(expected_exception, *args, **kwargs)
    else:
      return self._get_case_instance().assertRaises(
        expected_exception, callable = kwargs['callable_'], *args, **kwargs
      )

  @_overload
  def assertRaisesRegex(
    self,
    expected_exception: type[BaseException] | tuple[type[BaseException], ...],
    expected_regex: str | _Pattern[str],
    callable_: _Callable[..., object],
    *args: _Any,
    **kwargs: _Any,
  ) -> None:
    ...

  @_overload
  def assertRaisesRegex(
    self, expected_exception: type[_E] | tuple[type[_E], ...], expected_regex: str | _Pattern[str], *, msg: _Any = ...
  ) -> _AssertRaisesContext[_E]:
    ...

  def assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs) -> _AssertRaisesContext[_E] | None:
    if 'callable_' not in kwargs:
      return self._get_case_instance().assertRaisesRegex(
        expected_exception, expected_regex, *args, **kwargs
      )
    else:
      return self._get_case_instance().assertRaisesRegex(
        expected_exception, expected_regex, callable = kwargs['callable_'], *args, **kwargs
      )

  @_overload
  def assertWarns(
    self,
    expected_warning: type[Warning] | tuple[type[Warning], ...],
    callable_: _Callable[_P, object],
    *args: _P.args,
    **kwargs: _P.kwargs,
  ) -> None:
    ...

  @_overload
  def assertWarns(
    self,
    expected_warning: type[Warning] | tuple[type[Warning], ...], *, msg: _Any = ...
  ) -> _AssertWarnsContext:
    ...

  def assertWarns(self, expected_warning, *args, **kwargs) -> _AssertWarnsContext | None:
    if 'callable_' not in kwargs:
      return self._get_case_instance().assertWarns(expected_warning, *args, **kwargs)
    else:
      return self._get_case_instance().assertWarns(
        expected_warning, callable = kwargs['callable_'], *args, **kwargs
      )

  @_overload
  def assertWarnsRegex(
    self,
    expected_warning: type[Warning] | tuple[type[Warning], ...],
    expected_regex: str | _Pattern[str],
    callable_: _Callable[_P, object],
    *args: _P.args,
    **kwargs: _P.kwargs,
  ) -> None:
    ...

  @_overload
  def assertWarnsRegex(
    self, expected_warning: type[Warning] | tuple[type[Warning], ...], expected_regex: str | _Pattern[str], *,
    msg: _Any = ...
  ) -> _AssertWarnsContext:
    ...

  def assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs) -> _AssertWarnsContext | None:
    if 'callable_' not in kwargs:
      return self._get_case_instance().assertWarnsRegex(expected_warning, expected_regex, *args, **kwargs)
    else:
      return self._get_case_instance().assertWarnsRegex(
        expected_warning, callable_ = kwargs['callable_'], *args, **kwargs
      )

  def assertLogs(self, logger: str | _logging.Logger | None = None, level: int | str | None = None
  ):
    return self._get_case_instance().assertLogs(logger=logger, level=level)

  if _sys.version_info >= (3, 10):
    def assertNoLogs(
      self, logger: str | _logging.Logger | None = None, level: int | str | None = None
    ):
      return self._get_case_instance().assertNoLogs(logger=logger, level=level)

  @_overload
  def assertAlmostEqual(
    self, first, second, places: None, msg: _Any, delta
  ) -> None:
    ...

  @_overload
  def assertAlmostEqual(
    self, first, second, places: None = None, msg: _Any = None, *, delta
  ) -> None:
    ...

  @_overload
  def assertAlmostEqual(
    self,
    first,
    second,
    places: int | None = None,
    msg: _Any = None,
    delta: None = None,
  ) -> None:
    ...

  def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None) -> None:
    """若对象1约等于对象2，则通过"""
    self._get_case_instance().assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

  @_overload
  def assertNotAlmostEqual(self, first, second, places: None, msg: _Any, delta) -> None:
    ...

  @_overload
  def assertNotAlmostEqual(
    self, first, second, places: None = None, msg: _Any = None, *, delta
  ) -> None:
    ...

  @_overload
  def assertNotAlmostEqual(
    self, first,
    second,
    places: int | None = None,
    msg: _Any = None,
    delta: None = None,
  ) -> None:
    ...

  def assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None) -> None:
    """若对象1约等于对象2，则失败"""
    self._get_case_instance().assertNotAlmostEqual(first, second, places=places, msg=msg, delta=delta)

  def assertRegex(self, text: _AnyStr, expected_regex: _AnyStr | _Pattern[_AnyStr], msg: _Any = None) -> None:
    self._get_case_instance().assertRegex(text, expected_regex, msg = msg)

  def assertNotRegex(self, text: _AnyStr, unexpected_regex: _AnyStr | _Pattern[_AnyStr], msg: _Any = None) -> None:
    self._get_case_instance().assertNotRegex(text, unexpected_regex, msg = msg)

  def assertCountEqual(self, first: _Iterable[_Any], second: _Iterable[_Any], msg: _Any = None) -> None:
    self._get_case_instance().assertCountEqual(first, second, msg = msg)

  def assertMultiLineEqual(self, first: str, second: str, msg: _Any = None) -> None:
    self._get_case_instance().assertMultiLineEqual(first, second, msg = msg)

  def assertSequenceEqual(
    self, seq1: _Sequence[_Any], seq2: _Sequence[_Any], msg: _Any = None, seq_type: type[_Sequence[_Any]] | None = None
  ) -> None:
    self._get_case_instance().assertSequenceEqual(seq1, seq2, msg = msg, seq_type = seq_type)

  def assertListEqual(self, list1: list[_Any], list2: list[_Any], msg: _Any = None) -> None:
    self._get_case_instance().assertListEqual(list1, list2, msg = msg)

  def assertTupleEqual(self, tuple1: tuple[_Any, ...], tuple2: tuple[_Any, ...], msg: _Any = None) -> None:
    self._get_case_instance().assertTupleEqual(tuple1, tuple2, msg = msg)

  def assertSetEqual(self, set1: _AbstractSet[object], set2: _AbstractSet[object], msg: _Any = None) -> None:
    self._get_case_instance().assertSetEqual(set1, set2, msg = msg)

  # assertDictEqual accepts only true dict instances. We can't use that here, since that would make
  # assertDictEqual incompatible with TypedDict.
  def assertDictEqual(self, d1: _Mapping[_Any, object], d2: _Mapping[_Any, object], msg: _Any = None) -> None:
    self._get_case_instance().assertDictEqual(d1, d2, msg = msg)

  if _sys.version_info < (3, 12):
    failUnlessEqual        = assertEqual
    assertEquals           = assertEqual
    failIfEqual            = assertNotEqual
    assertNotEquals        = assertNotEqual
    failUnless             = assertTrue
    assert_                = assertTrue
    failIf                 = assertFalse
    failUnlessRaises       = assertRaises
    failUnlessAlmostEqual  = assertAlmostEqual
    assertAlmostEquals     = assertAlmostEqual
    failIfAlmostEqual      = assertNotAlmostEqual
    assertNotAlmostEquals  = assertNotAlmostEqual
    assertRegexpMatches    = assertRegex
    assertNotRegexpMatches = assertNotRegex
    assertRaisesRegexp     = assertRaisesRegex
    def assertDictContainsSubset(
      self, subset: _Mapping[_Any, _Any], dictionary: _Mapping[_Any, _Any], msg: object = None
    ) -> None:
      self._get_case_instance().assertDictContainsSubset(subset, dictionary, msg = msg)

