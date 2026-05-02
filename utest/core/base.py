import unittest as _unittest
from logging import Logger as _Logger
import utest.util as _util
import utest.meta as _meta
from utest.public.logger import u_logger as _u_logger



class Base(_unittest.TestCase):
  """框架基类"""

  # 引用日志器
  _logger: _Logger = _u_logger

  def __init__(self, methodName='runTest') -> None:
    """
    构造方法

    Args:
      methodName: 默认测试方法

    Returns:
      return:     无

    """
    super().__init__(methodName=methodName)

    # 获取日志方法
    self._get_logger_methods_by_config_file(logger = self._logger)


  def _get_logger_methods_by_config_file(
    self,
    logger: _Logger,
    logging_config_path: str = _util.path.framework.abs_path(_util.path.join(
      _meta.CONFIG_DIR, _meta.CONFIGs.LOGGING
    )),                                     # 配置文件路径
    config_file_encoding = 'utf-8'          # 配置文件默认用'UTF-8'编码
  ) -> None:
    """
    从日志器获取日志方法

    Args:
      logger:               日志器
      logging_config_path:  日志器配置文件路径
      config_file_encoding: 配置文件编码

    Returns:
      return:               无

    """
    # 定义字段名称
    more_levels = 'more_levels'

    def add_func_2_obj(
      obj: object,
      instance: object,
      func_name: str
    ) -> None:
      """
      将（日志）方法绑定到类

      Args:
        obj:           对象
        instance:      实例名称
        func_name:     方法名称

      Returns:
        return:        无

      """
      setattr(
        obj,
        func_name,
        getattr(instance, func_name)
      )

    # 读取配置文件
    config = _util.framework.read_yaml_config(
      config_path = logging_config_path,
      encoding    = config_file_encoding
    )

    # 导入更多日志级别
    if more_levels in config:
      for fn in config[more_levels].keys():
        add_func_2_obj(self, logger, fn)

    # 导入logging内置日志级别
    for fn in [
      'info',
      'warning',
      'error'
    ]:
      add_func_2_obj(self, logger, fn)

  def step(self, step: int, msg: str) -> None:
    """在日志中输出测试步骤"""
    self._step(f'{step}. {msg}')

  def trace(self, msg: str) -> None:
    """在日志中输出调试信息"""
    self._trace(msg)

  def info(self, msg: str) -> None:
    """在日志中输出一般信息"""
    self._info(msg)

  def warning(self, msg: str) -> None:
    """在日志中输出警告信息"""
    self._warning(msg)

  def error(self, msg: str) -> None:
    """在日志中输出错误信息"""
    self._error(msg)

  def fatal(self, msg: str) -> None:
    """在日志中输出致命错误信息"""
    self._fatal(msg)
    # 致命错误时，直接停止执行用例
    self.fail(msg)

  def _trace(self, msg, *args, **kwargs) -> None: ...
  def _info(self, msg, *args, **kwargs) -> None: ...
  def _warning(self, msg, *args, **kwargs) -> None: ...
  def _error(self, msg, *args, **kwargs) -> None: ...
  def _fatal(self, msg, *args, **kwargs) -> None: ...
  def _case(self, msg, *args, **kwargs) -> None: ...
  def _unit(self, msg, *args, **kwargs) -> None: ...
  def _precondition(self, msg, *args, **kwargs) -> None: ...
  def _postcondition(self, msg, *args, **kwargs) -> None: ...
  def _step(self, msg, *args, **kwargs) -> None: ...
  def _pass(self, msg, *args, **kwargs) -> None: ...
  def _fail(self, msg, *args, **kwargs) -> None: ...

