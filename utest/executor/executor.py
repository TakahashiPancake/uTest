import copy as _copy
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from types import ModuleType as _ModuleType
from typing import Any as _Any
import xml.etree.ElementTree as _ElementTree
from xml.etree.ElementTree import Element as _Element
import unittest as _unittest
from unittest import TestCase as _TestCase
from unittest import TestSuite as _TestSuite
from unittest.runner import TextTestResult as _TextTestResult
import HtmlTestRunner as _HtmlTestRunner
from HtmlTestRunner import HTMLTestRunner as _HTMLTestRunner
import utest.util.path as _path
from utest.util.stream import StringIO as _StringIO
from utest.util.date import DateTime as _DateTime
from utest.public.stream import sync_output_stream as _sync_stream



class _TestExecutorBase(_ABC):
  """测试执行器基类"""

  # 初始化测试套件
  _suite = _unittest.TestSuite()

  # 初始化测试加载器
  _loader = _unittest.TestLoader()

  # 引用文本流缓存区
  _sync_buffer = _sync_stream

  # 保存的文本流缓存区
  _sync_buffer_saved: _StringIO | None = None

  def __init__(self):
    """
    初始化对象

    1. 定义测试套件执行器
    2. ...

    """
    self._sync_buffer.clear_buffer()

  def __del__(self):
    self._sync_buffer.clear_buffer()

  def load(self, *tests: type[_TestCase] | _ModuleType, pattern: str | None = None) -> _TestSuite:
    """
    读取测试用例

    Args:
      tests:   测试（模块或类）（复数）
      pattern: load_tests协议片段

    Returns:
      return: 全部测试套件

    """
    # 加载测试
    for test in tests:
      if isinstance(test, _ModuleType):
        self._suite.addTest(self._load_module(test, pattern = pattern))
      elif issubclass(test, _TestCase):
        self._suite.addTest(self._load_case(test))

    return self._suite

  def _load_case(self, case: type[_TestCase]) -> _TestSuite:
    """
    加载测试用例

    Args:
      case:   测试用例

    Returns:
      return: 无

    """
    return self._loader.loadTestsFromTestCase(case)

  def _load_module(self,
    module: _ModuleType,
    *args,
    pattern: str | None = None
  ) -> _TestSuite:
    """
    加载测试用例

    Args:
      module:  包含测试用例的模块
      pattern: 片段，用于load_tests协议

    Returns:
      return: 无

    """
    return self._loader.loadTestsFromModule(module, *args, pattern = pattern)

  @_abstractmethod
  def _run_suite(self, suite, dir_name) -> _TextTestResult:
    """执行测试套件"""
    ...

  def run(self,
    output: str      = './reports/',
    report_name: str = '测试报告',
    result_name: str = '测试结果'
  ) -> _TextTestResult:
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
    self._sync_buffer.clear_buffer()

    # 记录当前时间
    current_datetime: str = _DateTime.get_formatted_datetime('%Y-%m-%d_%H-%M-%S')

    # 定义报告名称
    report_name = report_name + '_' + current_datetime

    # 定义日志名称
    result_name = result_name + '_' + current_datetime

    # 定义报告保存路径
    reports_saving_dir: str = _path.join(output, report_name)

    # 创建报告保存路径
    _path.create_dirs(reports_saving_dir)

    # 执行测试套件
    result = self._run_suite(self._suite, dir_name = report_name)

    # 保存缓存区
    self._sync_buffer_saved = _copy.copy(self._sync_buffer)

    # 定义保存日志方法
    def save_logs(xml_element: _Element, path: str):
      """递归保存日志"""

      test_logs: list = xml_element.findall(path)

      for element in test_logs:

        if 'unittest.suite.TestSuite' not in element.attrib['TEST_CASE']:

          # 定义日志名称
          #log_name = (element.attrib['TEST_CASE'] + '_' + element.attrib['DATETIME']) \
          #  .replace(':', '_').replace('.', '_')
          log_name = element.attrib['TEST_CASE'] \
            .replace(':', '_').replace('.', '_')

          # 定义日志保存路径
          logs_saving_dir: str = _path.join(reports_saving_dir, log_name)

          # 创建日志保存路径
          _path.create_dirs(logs_saving_dir)

          with open(_path.join(
            logs_saving_dir,
            log_name + '.log'
          ), 'w') as file:
            print(element.text, file=file)

        elif element.find(path) is not None:
          save_logs(element, path)

        else:
          pass

    # 保存文本格式日志

    # 读取XML测试结果
    xml_log_str: str = self._sync_buffer_saved.getvalue()
    xml_log_root: _Element[str] = _ElementTree.fromstring(xml_log_str)
    xml_log_root_main: _Element[str] = xml_log_root.find('MAIN')

    # 保存日志
    save_logs(xml_log_root_main, 'TEST_LOG')

    # 保存XML格式的测试结果
    with open(_path.join(
      reports_saving_dir,
      result_name + '.xml'
    ), 'w') as f:
      self._sync_buffer_saved.print_buffer(file=f)

    # 返回测试结果
    return result


class TextTestExecutor(_TestExecutorBase):
  """文本测试执行器"""

  def __init__(self) -> None:
    super().__init__()
    self._runner = _unittest.TextTestRunner()

  def _run_suite(self, suite, dir_name) -> _TextTestResult:
    ...

class HTMLTestExecutor(_TestExecutorBase):
  """HTML测试执行器"""

  class _Params(object):
    """
    参数

    """
    output: str | None                  = None
    verbosity: int | None               = None
    stream: _StringIO | None            = None
    descriptions: bool | None           = None
    failfast: bool | None               = None
    buffer: bool | None                 = None
    report_title: str | None            = None
    report_name: str | None             = None
    template: str | None                = None
    resultclass: _TextTestResult | None = None
    add_timestamp: bool | None          = None
    open_in_browser: bool | None        = None
    combine_reports: bool | None        = None
    template_args: _Any                 = None

  _params = _Params()

  _runner: _HTMLTestRunner | None = None

  def __init__(self,
    output: str                         = './reports/',
    verbosity: int                      = 2,
    descriptions: bool                  = True,
    failfast: bool                      = False,
    buffer: bool                        = False,
    report_title: str                   = '测试报告',
    report_name: str                    = '测试报告',
    template: str | None                = None,
    resultclass: _TextTestResult | None = None,
    add_timestamp: bool                 = True,
    open_in_browser: bool               = False,
    combine_reports: bool               = True, #default False
    template_args: _Any                 = None
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

    try:
      self._params.output          = output
      self._params.verbosity       = verbosity
      self._params.stream          = self._sync_buffer
      self._params.descriptions    = descriptions
      self._params.failfast        = failfast
      self._params.buffer          = buffer
      self._params.report_title    = report_title
      self._params.report_name     = report_name
      self._params.template        = template
      self._params.resultclass     = resultclass
      self._params.add_timestamp   = add_timestamp
      self._params.open_in_browser = open_in_browser
      self._params.combine_reports = combine_reports
      self._params.template_args   = template_args
    finally:
      ...

  def _run_suite(self, suite, dir_name) -> _TextTestResult:
    self._params.output = _path.join(self._params.output, dir_name)
    self._runner = _HtmlTestRunner.HTMLTestRunner(**vars(self._params))
    result = self._runner.run(suite)
    return result

