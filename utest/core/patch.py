import types
import utest.util.framework as framework_util


class Patcher(object):
  """补丁"""

  @staticmethod
  def patch_logging(config_path, encoding='utf-8'):
    """
    修补logging模块

    Args:
      config_path: 配置文件路径
      encoding:    配置文件编码

    Returns:
      return:      无

    """
    import logging

    # 定义字段名
    more_levels  = 'more_levels'
    basic_config = 'basic_config'


    def set_log_level(func_name, name, level):
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


    if not hasattr(logging, '_patched'):

      # 读取配置文件
      config = framework_util.read_yaml_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 更多日志级别
      if more_levels in config:
        for fn in config[more_levels].keys():
          set_log_level(fn, **config[more_levels][fn])

      # 设置基本日志输出
      if basic_config in config:
        logging.basicConfig(**config[basic_config])

      # 标记logging为patched
      setattr(logging, '_patched', True)

      # 设置logging配置文件目录
      setattr(logging, '_config_path', config_path)

    elif getattr(logging, '_config_path') != config_path:
      raise ValueError(
        'Module logging has already been patched by another config!'
      )


  @staticmethod
  def patch_unittest(config_path, encoding='utf-8'):
    """
    修补unittest模块

    Args:
      config_path: 配置文件路径
      encoding:    配置文件编码

    Returns:
      return:      无

    """
    import unittest

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


patcher = Patcher()

