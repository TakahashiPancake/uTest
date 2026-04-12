import sys as _sys
import time as _time
import traceback as _traceback
import copy as _copy
from abc import ABC as _ABC, abstractmethod  # 导入装饰器
from typing import LiteralString, Any        # 导入类型
import unittest as _unittest
from unittest import TestSuite               # 导入类型
from unittest.runner import TextTestResult   # 导入类型
import HtmlTestRunner as _HtmlTestRunner
from HtmlTestRunner.result import TestResult # 导入类型
import utest.util.path as _path
from utest.util.stream import StreamBuffer   # 导入类型
from utest.util.date import DateTime as _DateTime
from utest.common.stream import stream_buffer as _stream_buffer_
from utest.core.case import TestCase         # 导入类型


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
    self.start_time = _time.time()
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
      msg_lines = _traceback.format_exception(exc_type, value, tb)

    if self.buffer:
      # Only try to get sys.stderr as it might not be
      # StringIO yet, e.g. when test fails during __call__
      try:
        error = _sys.stderr.getvalue()
      except AttributeError:
        error = None
      if error:
        if not error.endswith('\n'):
          error += '\n'
        msg_lines.append(error)
    # This is the extra magic to make sure all lines are str
    encoding = getattr(_sys.stdout, 'encoding', 'utf-8')
    lines = []
    for line in msg_lines:
      if not isinstance(line, str):
        # utf8 shouldn't be hard-coded, but not sure f
        line = line.encode(encoding)
      lines.append(line)

    return ''.join(lines)


# 给 html-testrunner 打补丁
_PatchHTMLTestRunner()()

class _TestExecutorBase(_ABC):
  """测试执行器基类"""

  # 初始化测试套件
  _suite = _unittest.TestSuite()

  # 初始化测试加载器
  _loader = _unittest.TestLoader()

  # 引用文本流缓存区
  _stream_buffer = _stream_buffer_

  # 保存的文本流缓存区
  _stream_buffer_saved: StreamBuffer | None = None

  def __init__(self):
    """
    初始化对象

    1. 定义测试套件执行器
    2. ...

    """
    self._stream_buffer.clear()

  def __del__(self):
    self._stream_buffer.clear()

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

  def run(self,
    output: str      = './reports/',
    report_name: str = '测试报告'
  ) -> TextTestResult:
    """
    执行测试用例

    1. 默认执行所有测试用例

    2. 保存缓冲区

    3. 返回测试结果

    Args:
      ...

    Returns:
      return: 测试结果

    """
    # 清除缓存区
    self._stream_buffer.clear()

    # 执行测试套件
    result = self._run_suite(self._suite)

    # 保存缓存区
    self._stream_buffer_saved = _copy.deepcopy(self._stream_buffer)

    # 输出缓存区到文件
    with open(_path.join(
      output,
      report_name + '_' + _DateTime.get_formatted_datetime('%Y-%m-%d_%H-%M-%S') + '.log'
    ), 'w') as f:
      self._stream_buffer_saved.output(file=f)

    # 返回测试结果
    return result


class TextTestExecutor(_TestExecutorBase):
  """文本测试执行器"""

  def __init__(self) -> None:
    super().__init__()
    self._runner = _unittest.TextTestRunner()

  def _run_suite(self, suite) -> TextTestResult:
    self._stream_buffer.clear()
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
    template: str | None  = None,
    resultclass           = None,
    add_timestamp: bool   = True,
    open_in_browser: bool = False,
    combine_reports: bool = True,
    template_args         = None
  ) -> None:
    """
    初始化测试执行器

    1. 定义测试套件执行器
    2. ...

    Args:
      ...

    Returns:
      return: 无

    """
    super().__init__()

    if template is None:
      template = _path.framework.abs_path('./external/report_template.html')

    self._runner = _HtmlTestRunner.HTMLTestRunner(
      output          = output,
      verbosity       = verbosity,
      stream          = self._stream_buffer(),
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

  def _run_suite(self, suite) -> TextTestResult:
    result = self._runner.run(suite)

    # Debug
    #print(result.stream.getvalue())

    return result

