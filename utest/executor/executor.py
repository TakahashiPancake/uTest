import os as _os
import copy as _copy
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Any as _Any
import xml.etree.ElementTree as _ElementTree
import unittest as _unittest
from unittest import TestSuite as _TestSuite
from unittest.runner import TextTestResult as _TextTestResult
import HtmlTestRunner as _HtmlTestRunner
from HtmlTestRunner import HTMLTestRunner as _HTMLTestRunner
import utest.util.path as _path
from utest.util.stream import StringIO as _StringIO
from utest.util.date import DateTime as _DateTime
from utest.common.stream import sync_stream as _sync_stream
from utest.core.case import TestCase as _TestCase



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

  def load(self, case: type[_TestCase], /, *cases: type[_TestCase]) -> _TestSuite:
    """
    读取测试用例

    Args:
      case:   测试用例
      cases:  测试用例（复数）

    Returns:
      return: 全部测试套件

    """
    # 添加到套件
    self._suite.addTest(self._load_case(case))

    # 逐个添加剩余的
    for case_ in cases:
      self._suite.addTest(self._load_case(case_))

    return self._suite

  def _load_case(self, case) -> _TestSuite:
    """
    加载测试用例

    Args:
      case:   测试用例

    Returns:
      return: 无

    """
    return self._loader.loadTestsFromTestCase(case)

  @_abstractmethod
  def _run_suite(self, suite, dir_name) -> _TextTestResult:
    """执行测试套件"""
    ...

  def run(self,
    output: str      = './reports/',
    report_name: str = '测试报告'
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

    # 定义日志名称
    log_name = report_name + '_' + current_datetime

    # 定义日志保存路径
    log_saving_dir: str = _path.join(output, log_name)

    # 创建日志保存路径
    _os.makedirs(log_saving_dir, exist_ok=True)

    # 执行测试套件
    result = self._run_suite(self._suite, dir_name = log_name)

    # 保存缓存区
    self._sync_buffer_saved = _copy.copy(self._sync_buffer)

    # 保存所有日志
    xml_log_str: str = self._sync_buffer_saved.getvalue()
    xml_log_root = _ElementTree.fromstring(xml_log_str)
    xml_log_root_main = xml_log_root.find('MAIN')
    test_logs: list = xml_log_root_main.findall('TEST_LOG')
    for element in test_logs:
      with open(_path.join(
        log_saving_dir,
        (element.tag + '_' + element.attrib['TEST_CASE'] + '_' + element.attrib['DATETIME']) \
          .replace(':', '_').replace('.', '_') + '.log'
      ), 'w') as f:
        print(element.text, file=f)

    # 保存XML格式的日志
    with open(_path.join(
      log_saving_dir,
      log_name + '.xml'
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
    _ = dir_name
    return self._runner.run(suite)


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

