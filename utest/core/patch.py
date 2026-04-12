import types as _types
import unittest as _unittest
import logging as _logging
import utest.util.framework as _framework_util
from utest.common.stream import stream_buffer as _stream_buffer_


class Patcher(object):
  """补丁"""
  _stream_buffer = _stream_buffer_

  @staticmethod
  def _set_log_level(
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
    # 添加新的日志级别
    _logging.addLevelName(level, name)

    # 动态创建方法
    func_code = compile(
      f'''def {func_name}(self, msg, *args, **kwargs):
        if self.isEnabledFor({level}):
          self._log({level}, msg, args, **kwargs)
      ''',
      '<string>',
      'exec'
    ).co_consts[0]
    func = _types.FunctionType(func_code, globals())

    # 绑定方法到类
    setattr(_logging.Logger, func_name, func)

  def patch_logging_by_config_file(self,
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
    # 定义字段名
    more_levels  = 'more_levels'
    basic_config = 'basic_config'

    if not hasattr(_logging, '_patched'):

      # 读取配置文件
      config = _framework_util.read_yaml_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 更多日志级别
      if more_levels in config:
        for fn in config[more_levels].keys():
          self._set_log_level(fn, **config[more_levels][fn])

      # 设置基本日志输出
      if basic_config in config:
        _logging.basicConfig(
          **config[basic_config],
          handlers = [
            _logging.StreamHandler(),
            _logging.StreamHandler(self._stream_buffer())
          ]
        )

      # 标记logging为patched
      setattr(_logging, '_patched', True)

      # 设置logging配置文件目录
      setattr(_logging, '_config_path', config_path)

    elif getattr(_logging, '_config_path') != config_path:
      raise ValueError(
        'Module logging has already been patched by another config!'
      )


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
    test_loader        = 'test_loader'
    test_method_prefix = 'test_method_prefix'

    if not hasattr(_unittest, '_patched'):

      # 读取配置文件
      config = _framework_util.read_yaml_config(
        config_path = config_path,
        encoding    = encoding
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


patcher = Patcher()

