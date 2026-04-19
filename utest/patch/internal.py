# 内部补丁松耦合

class _PatchLogging(object):

  from io import StringIO
  from utest.common.stream import sync_stream
  sync_stream: StringIO = sync_stream

  @staticmethod
  def set_log_level(
    func_name: str,
    name: str,
    level: int
  ) -> None:
    """
    添加自定义日志级别

    Args:
      func_name: 方法名
      name:      日志名称
      level:     日志级别

    Returns:
      return:    无

    """
    import types
    import logging

    # 添加新的日志级别
    logging.addLevelName(level, name)

    # 动态创建方法
    func_code = compile(
      f'''def {func_name}(self, msg, *args, **kwargs):
        if self.isEnabledFor({level}):
          self._log({level}, msg, args, **kwargs)
      ''',
      '<string>',
      'exec'
    ).co_consts[0]
    func = types.FunctionType(func_code, globals())

    # 绑定方法到类
    setattr(logging.Logger, func_name, func)


class _PatchUnittest(object):

  @staticmethod
  def patch_test_suite_class():
    import inspect as _inspect
    from unittest import TestSuite as _TestSuite
    from unittest import TestCase as _TestCase
    from utest.util.date import DateTime as _DateTime
    from utest.common.stream import sync_stream as _sync_buffer

    def run_test_custom(
      self,
      result,
      debug                              = False,
    ):
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
            print(
              r'<TEST_LOG TEST_CASE="{}" DATETIME="{}">'.format(
                # 测试用例标题
                _inspect.getmodule(test._tests[0]).__name__+ '.' + type(test._tests[0]).__name__,
                # 测试日期&测试时间
                _DateTime.get_formatted_datetime('%Y-%m-%d_%H:%M:%S.%f')
              ),
              sep='', file=_sync_buffer
            )
            # 执行测试套件
            test(result)
            # XML结束标签
            print(
              '</TEST_LOG>',
              sep = '', file = _sync_buffer
            )
          elif isinstance(test, _TestCase):
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

    # 修补TestSuite.run
    _TestSuite.run = run_test_custom

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
      #self.stream.writeln()
      self.stream.flush()
    self.printErrorList('ERROR', self.errors_custom)
    self.printErrorList('FAIL', self.failures_custom)
    unexpected_successes = getattr(self, 'unexpectedSuccesses', ())
    if unexpected_successes:
      self.stream.writeln(self.separator1)
      for test in unexpected_successes:
        self.stream.writeln(f"UNEXPECTED SUCCESS: {self.getDescription(test)}")
      self.stream.flush()


class _PatchFramework(object):
  @staticmethod
  def patch_case() -> None:
    from utest.core.case import TestCase

    def tear_down(self) -> None:
      _ = self
      ...

    # 重载tearDown
    TestCase.tearDown = tear_down


class Patcher(object):
  """补丁"""

  @staticmethod
  def patch_logging_by_config_file(
    config_path: str,
    encoding: str = 'utf-8'
  ):
    """
    修补logging模块

    Args:
      config_path: 配置文件路径
      encoding:    配置文件编码

    Returns:
      return:      无

    """
    import logging
    import utest.util.framework as framework_util

    # 定义字段名
    more_levels  = 'more_levels'
    basic_config = 'basic_config'

    if not hasattr(logging, '_patched'):

      # 读取配置文件
      config = framework_util.read_yaml_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 更多日志级别
      if more_levels in config:
        for fn in config[more_levels].keys():
          _PatchLogging.set_log_level(fn, **config[more_levels][fn])

      # 设置基本日志输出
      if basic_config in config:
        logging.basicConfig(
          **config[basic_config],
          handlers = [
            # 输出到同步输出流
            logging.StreamHandler(_PatchLogging.sync_stream)
          ]
        )

      # 标记logging为patched
      setattr(logging, '_patched', True)

      # 设置logging配置文件目录
      setattr(logging, '_config_path', config_path)

    elif getattr(logging, '_config_path') != config_path:
      raise ValueError(
        'Module logging has already been patched by another config!'
      )

  @staticmethod
  def patch_unittest():
    """
    修补unittest模块

    """
    from unittest import TestResult

    TestResult.errors_custom       = []
    TestResult.failures_custom     = []
    TestResult.clear_errors_custom = _PatchUnittest.clear_errors_custom
    TestResult.print_errors_custom = _PatchUnittest.print_errors_custom

    # 修补TestSuite
    _PatchUnittest.patch_test_suite_class()

  @staticmethod
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
    import unittest
    import utest.util.framework as framework_util

    test_loader        = 'test_loader'
    test_method_prefix = 'test_method_prefix'

    if not hasattr(unittest, '_patched'):

      # 读取配置文件
      config = framework_util.read_yaml_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 更多日志级别
      if test_loader in config:
        unittest.TestLoader.testMethodPrefix = \
          config[test_loader][test_method_prefix]

      # 标记unittest为patched
      setattr(unittest, '_patched', True)

      # 设置unittest配置文件目录
      setattr(unittest, '_config_path', config_path)

    elif getattr(unittest, '_config_path') != config_path:
      raise ValueError(
        'Module unittest has already been patched by another config!'
      )

  @staticmethod
  def patch_framework():
    _PatchFramework.patch_case()


patcher = Patcher()

