import inspect as _inspect
from utest.util.date import DateTime as _DateTime
import functools as _func_tools
from fnmatch import fnmatchcase as _fnmatchcase
from unittest import TestLoader as _TestLoader
from unittest import TestSuite as _TestSuite
from unittest import TestResult as _TestResult
from unittest import TestCase as _TestCase
from unittest import TextTestResult as _TextTestResult
import unittest as _unittest
import utest.util.framework as framework_util
from utest.patch.base import PatcherBase as _PatcherBase
from utest.public.stream import sync_output_stream as _sync_output_stream


class LoaderPatch(_PatcherBase):

  _class_to_patch = _TestLoader

  @staticmethod
  def getTestCaseNames(self, testCaseClass):
    """ Return a sorted sequence of method names found within testCaseClass """

    def shouldIncludeMethod(attr_name):
      # 添加测试方法名称
      if not (attr_name.startswith(self.testMethodPrefix) or attr_name == 'testcase'):
        return False
      test_func = getattr(testCaseClass, attr_name)
      if not callable(test_func):
        return False
      full_name = f'%s.%s.%s' % (
        testCaseClass.__module__, testCaseClass.__qualname__, attr_name
      )
      return self.testNamePatterns is None or \
        any(_fnmatchcase(full_name, pattern) for pattern in self.testNamePatterns)

    test_fn_names = list(filter(shouldIncludeMethod, dir(testCaseClass)))
    if self.sortTestMethodsUsing:
      test_fn_names.sort(key=_func_tools.cmp_to_key(self.sortTestMethodsUsing))
    return test_fn_names


class SuitePatch(_PatcherBase):

  _class_to_patch = _TestSuite

  @staticmethod
  def run(self, result, debug = False):
    """
    补丁

    模块: TestSuite

    方法: TestSuite.run()

    """

    def _isnotsuite(t):
      try:
        iter(t)
      except TypeError:
        return True
      return False

    top_level = False
    if getattr(result, '_testRunEntered', False) is False:
      result._testRunEntered = top_level = True

    for index, test in enumerate(self):
      if result.shouldStop:
        break

      if _isnotsuite(test):
        self._tearDownPreviousClass(test, result)
        self._handleModuleFixture(test, result)
        self._handleClassSetUp(test, result)
        result._previousTestClass = test.__class__

        if (getattr(test.__class__, '_classSetupFailed', False) or
          getattr(result, '_moduleSetUpFailed', False)):
          continue

      if not debug:
        if isinstance(test, _TestSuite):
          # 使用XML标签将测试用例结果封装
          # 测试套件不为空
          if test._tests:
            print(
              r'<TEST_LOG TEST_CASE="{}" DATETIME="{}">'.format(
                # 测试用例标题
                _inspect.getmodule(test._tests[0]).__name__ + '.' + type(test._tests[0]).__name__,
                # 测试日期&测试时间
                _DateTime.get_formatted_datetime('%Y-%m-%d_%H:%M:%S.%f')
              ),
              sep='', file=_sync_output_stream
            )
            # 执行测试套件
            test(result)
            # XML结束标签
            print(
              '</TEST_LOG>',
              sep='', file=_sync_output_stream
            )

          # 测试套件为空
          else:
            # 执行测试套件
            test(result)
        elif isinstance(test, _TestCase):
          # 输出分隔符
          result.stream.write(_TextTestResult.separator1)
          result.stream.writeln()
          result.stream.flush()
          # 执行测试用例
          test(result)
          # 输出自定义错误&自定义失败
          result.print_errors_custom()
          # 清除自定义错误&自定义失败
          result.clear_errors_custom()

        else:
          pass
      else:
        test.debug()

      if self._cleanup:
        self._removeTestAtIndex(index)

    if top_level:
      self._tearDownPreviousClass(None, result)
      self._handleModuleTearDown(result)
      result._testRunEntered = False
    return result


class ResultPatch(_PatcherBase):

  _class_to_patch = _TestResult

  # 自定义错误列表
  errors_custom   = []

  # 自定义失败列表
  failures_custom = []

  @staticmethod
  def clear_errors_custom(self) -> int:
    """
    补丁

    模块: TestResult

    方法（新增）: TestResult.clear_errors_custom()

    """
    # 框架内
    self.errors_custom.clear()
    self.failures_custom.clear()
    return 0

  @staticmethod
  def print_errors_custom(self):
    """
    补丁

    模块: TextTestResult

    方法（新增）: TextTestResult.print_errors_custom()

    """
    if self.dots or self.showAll:
      # self.stream.writeln()
      self.stream.flush()
    self.printErrorList('ERROR', self.errors_custom)
    self.printErrorList('FAIL', self.failures_custom)
    unexpected_successes = getattr(self, 'unexpectedSuccesses', ())
    if unexpected_successes:
      self.stream.writeln(self.separator1)
      for test in unexpected_successes:
        self.stream.writeln(f"UNEXPECTED SUCCESS: {self.getDescription(test)}")
      self.stream.flush()


def patch_unittest_by_config_file(
  config_path: str,
  encoding: str = 'utf-8'
):
  """
  修补unittest模块

  Args:
    config_path: 配置文件路径
    encoding:    配置文件编码

  Returns:
    return:      无

  """

  test_loader = 'test_loader'
  test_method_prefix = 'test_method_prefix'

  if not hasattr(_unittest, '_patched'):

    # 读取配置文件
    config = framework_util.read_yaml_config(
      config_path=config_path,
      encoding=encoding
    )

    # 更多日志级别
    if test_loader in config:
      _unittest.TestLoader.testMethodPrefix = \
        config[test_loader][test_method_prefix]

    # 标记unittest为patched
    setattr(_unittest, '_patched', True)

    # 设置unittest配置文件目录
    setattr(_unittest, '_config_path', config_path)

  elif getattr(_unittest, '_config_path') != config_path:
    raise ValueError(
      'Module unittest has already been patched by another config!'
    )

