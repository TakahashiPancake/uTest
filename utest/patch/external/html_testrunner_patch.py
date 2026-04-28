import sys as _sys
import time as _time
from datetime import datetime as _datetime
import traceback as _traceback
from typing import LiteralString as _LiteralString
from HtmlTestRunner.result import TestResult as _TestResult
from HtmlTestRunner.result import HtmlTestResult as _HtmlTestResult
from HtmlTestRunner.runner import HTMLTestRunner as _HTMLTestRunner
from utest.common.stream import sync_output_stream as _sync_stream
from utest.common.proto import proto as _proto
from utest.patch.base import PatcherBase as _PatcherBase

class ResultPatch(_PatcherBase):

  _class_to_patch = _HtmlTestResult

  @staticmethod
  def addFailure(self, test, err):
    """ Called when a test method fails. """
    self._save_output_data()
    test_info = self.infoclass(self, test, self.infoclass.FAILURE, err)
    self._prepare_callback(test_info, self.failures, 'FAIL', 'F')
    # 自定义failures列表
    self._prepare_callback(test_info, self.failures_custom, 'FAIL', 'F')

  @staticmethod
  def addError(self, test, err):
    """" Called when a test method raises an error. """
    self._save_output_data()
    test_info = self.infoclass(self, test, self.infoclass.ERROR, err)
    self._prepare_callback(test_info, self.errors, 'ERROR', 'E')
    # 自定义errors列表
    self._prepare_callback(test_info, self.errors_custom, 'ERROR', 'E')

  @staticmethod
  def startTest(self, test):
    """ Called before execute each method. """
    self.start_time = _time.time()
    _TestResult.startTest(self, test)

    # 注释掉以下不显示标题
    #if self.showAll:
    #  self.stream.write(f'{self.getDescription(test)}\n')
    #  self.stream.write(' ...\n')

  @staticmethod
  def _prepare_callback(
    self, test_info, target_list, verbose_str, short_str
  ):
    """ Appends an 'info class' to the given target list and sets a
        callback method to be called by stopTest method."""

    target_list.append(test_info)

    def callback():
      """ Print test method outcome to the stream and elapsed time too."""
      test_info.test_finished()

      if self.showAll:
        # 使用测试用例实例输出callback
        #self.stream.writeln(
        #  "{} ({:3f})s".format(verbose_str, test_info.elapsed_time)
        #)
        formated_string = '{} {} ({:3f})s'.format(test_info.test_id.rsplit('.', 1)[-1], verbose_str, test_info.elapsed_time)
        if test_info.outcome == 0:
          _proto.pass_(formated_string)
        else:
          _proto.fail_(formated_string)

      elif self.dots:
        self.stream.write(short_str)

    self.callback = callback

  @staticmethod
  def printErrorList(self, flavour, errors):
    """
    Writes information about the FAIL or ERROR to the stream.
    """
    for test_info in errors:
      # 空行
      self.stream.writeln()

      self.stream.writeln(self.separator1)
      self.stream.writeln(
        '{} [{:3f}s]: {}'.format(flavour, test_info.elapsed_time,
                                 test_info.test_id)
      )
      self.stream.writeln(self.separator2)
      self.stream.writeln('%s' % test_info.get_error_info())

  @staticmethod
  def _exc_info_to_string(self, err, test) -> _LiteralString:
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


class RunnerPatch(_PatcherBase):

  # 被打补丁的类
  _class_to_patch = _HTMLTestRunner

  @staticmethod
  def run(self, test):
    """ Runs the given testcase or testsuite. """
    try:
      result = self._make_result()
      result.failfast = self.failfast
      if hasattr(test, 'properties'):
        # junit testsuite properties
        result.properties = test.properties

      # 输出XML格式

      # XML根
      print('<TEST_RESULT>', file=_sync_stream)

      # 将XML头部输出到XML根内
      # XML标签开始
      print('<HEADER>', file=_sync_stream)
      self.stream.writeln("Running tests... ")
      self.stream.writeln(result.separator2)
      print('</HEADER>', file=_sync_stream)

      print('<MAIN>', file=_sync_stream)
      self.start_time = _datetime.now()
      test(result)
      stop_time = _datetime.now()
      self.time_taken = stop_time - self.start_time

      # 注释掉以下行关闭错误自动输出
      # result.printErrors()
      # self.stream.writeln(result.separator2)
      print('</MAIN>', file=_sync_stream)

      # 将XML足部输出到XML根内
      print('<FOOTER>', file=_sync_stream)
      print('<TEST_INFO>', file=_sync_stream)
      run = result.testsRun
      self.stream.writeln("Ran {} test{} in {}".format(
        run,
        run != 1 and "s" or "", str(self.time_taken)[:7]
      ))
      self.stream.writeln()

      expected_fails = len(result.expectedFailures)
      unexpected_successes = len(result.unexpectedSuccesses)
      skipped = len(result.skipped)

      infos = []
      if not result.wasSuccessful():
        self.stream.writeln("FAILED")
        failed, errors = map(len, (result.failures, result.errors))
        if failed:
          infos.append("Failures={0}".format(failed))
        if errors:
          infos.append("Errors={0}".format(errors))
      else:
        self.stream.writeln("OK")

      if skipped:
        infos.append("Skipped={}".format(skipped))
      if expected_fails:
        infos.append("Expected Failures={}".format(expected_fails))
      if unexpected_successes:
        infos.append("Unexpected Successes={}".format(unexpected_successes))

      if infos:
        self.stream.writeln(" ({})".format(", ".join(infos)))
      else:
        self.stream.writeln("\n")
      print('</TEST_INFO>', file=_sync_stream)

      self.stream.writeln()
      self.stream.writeln('Generating HTML reports... ')
      result.generate_reports(self)

      # XML标签结束
      print('</FOOTER>', file=_sync_stream)

      # XML结束
      print('</TEST_RESULT>', file=_sync_stream)

      if self.open_in_browser:
        import webbrowser
        for report in result.report_files:
          webbrowser.open_new_tab('file://' + report)
    finally:
      pass
    return result

