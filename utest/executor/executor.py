import sys
import time
import traceback
from abc import ABC, abstractmethod
from typing import LiteralString, Any
import unittest
from unittest import TestSuite
from unittest.runner import TextTestResult
import HtmlTestRunner
from HtmlTestRunner.result import TestResult
from utest.util.path import framework
from utest.util.stream import redirect_stream
from utest.core.case import TestCase


class _PatchHTMLTestRunner(object):
  """
  html-testrunner 补丁

  - 适配版本：

    -  python          version 3.11.13
    -  html-testrunner version 1.2.1

  """
  def __call__(self) -> None:
    """打补丁"""
    from HtmlTestRunner.result import HtmlTestResult

    # 修改 HtmlTestRunner.result.HtmlTestResult 使之能在 python 3.11.13 中运行
    HtmlTestResult._exc_info_to_string = self._exc_info_to_string

    # 额外修改，使测试日志更加美观
    HtmlTestResult.startTest = self.start_test


  @staticmethod
  def start_test(self, test):
    """ Called before execute each method. """
    self.start_time = time.time()
    TestResult.startTest(self, test)

    if self.showAll:
      self.stream.write(self.getDescription(test))
      self.stream.write(" ...\n")

  @staticmethod
  def _exc_info_to_string(self, err, test) -> LiteralString:
    """ Converts a sys.exc_info()-style tuple of values into a string."""
    # if six.PY3:
    # # It works fine in python 3
    # try:
    #   return super(
    #     _HTMLTestResult,
    #     self
    #   )._exc_info_to_string(err, test)
    # except AttributeError:
    #   # We keep going using the legacy python <= 2 way
    #   pass

    # This comes directly from python2 unittest
    exc_type, value, tb = err
    # Skip test executor traceback levels
    while tb and self._is_relevant_tb_level(tb):
      tb = tb.tb_next

    msg_lines = []

    if exc_type is test.failureException:
      # Skip assert*() traceback levels
      msg_lines = traceback.format_exception(exc_type, value, tb)

    if self.buffer:
      # Only try to get sys.stderr as it might not be
      # StringIO yet, e.g. when test fails during __call__
      try:
        error = sys.stderr.getvalue()
      except AttributeError:
        error = None
      if error:
        if not error.endswith('\n'):
          error += '\n'
        msg_lines.append(error)
    # This is the extra magic to make sure all lines are str
    encoding = getattr(sys.stdout, 'encoding', 'utf-8')
    lines = []
    for line in msg_lines:
      if not isinstance(line, str):
        # utf8 shouldn't be hard-coded, but not sure f
        line = line.encode(encoding)
      lines.append(line)

    return ''.join(lines)


# 给 html-testrunner 打补丁
_PatchHTMLTestRunner()()


class _TestExecutorBase(ABC):
  """测试执行器基类"""

  # 初始化测试套件
  _suite = unittest.TestSuite()

  # 初始化测试加载器
  _loader = unittest.TestLoader()

  @abstractmethod
  def __init__(self):
    """
    初始化对象

    1. 定义测试套件执行器
    2. ...

    """
    ...

  def load_case(self, case: TestCase | Any) -> TestSuite:
    """
    读取测试用例

    Args:
      case:   测试用例

    Returns:
      return: 读取到的测试套件

    """
    suite = self._load_case(case)

    # 添加到套件
    self._suite.addTest(suite)

    return suite

  def _load_case(self, case) -> TestSuite:
    """
    加载测试用例

    Args:
      case:   测试用例

    Returns:
      return: 无

    """
    return self._loader.loadTestsFromTestCase(case)

  @abstractmethod
  def _run_suite(self, suite) -> TextTestResult:
    """执行测试套件"""
    ...

  def run(self) -> TextTestResult:
    """
    执行测试用例

    - 默认执行所有测试用例

    """
    return self._run_suite(self._suite)


class TextTestExecutor(_TestExecutorBase):
  """文本测试执行器"""

  def __init__(self) -> None:
    self._runner = unittest.TextTestRunner()

  def _run_suite(self, suite) -> TextTestResult:
    return self._runner.run(suite)


class HTMLTestExecutor(_TestExecutorBase):
  """HTML测试执行器"""

  def __init__(self,
    output: str           = './reports/',
    verbosity: int        = 2,
    descriptions: bool    = True,
    failfast: bool        = False,
    buffer: bool          = False,
    report_title: str     = '测试报告',
    report_name: str      = '测试报告',
    template: str         = None,
    resultclass           = None,
    add_timestamp: bool   = True,
    open_in_browser: bool = False,
    combine_reports: bool = True,
    template_args         = None
  ) -> None:
    """
    初始化测试执行器

    Args:
      ...

    Returns:
      return: 无

    """
    # 清空重定向缓存
    redirect_stream.clear()

    if template is None:
      template = framework.abs_path('./external/report_template.html')

    self._runner = HtmlTestRunner.HTMLTestRunner(
      output          = output,
      verbosity       = verbosity,
      stream          = redirect_stream.buffer,
      descriptions    = descriptions,
      failfast        = failfast,
      buffer          = buffer,
      report_title    = report_title,
      report_name     = report_name,
      template        = template,
      resultclass     = resultclass,
      add_timestamp   = add_timestamp,
      open_in_browser = open_in_browser,
      combine_reports = combine_reports,
      template_args   = template_args
    )

  def __del__(self):
    redirect_stream.clear()

  def _run_suite(self, suite) -> TextTestResult:
    redirect_stream.clear()
    result = self._runner.run(suite)

    return result

