import unittest as _unittest
import utest.util as _util
import utest.meta as _meta
from utest.common.logger import u_logger as _u_logger



class Base(_unittest.TestCase):
  """
  框架基类

  1. 框架基类继承自unittest.TestCase

  2. 包含一个创建日志器的方法

  3. 声明日志方法

  """

  # 引用日志器
  _logger = _u_logger

  def __init__(self, methodName='runTest') -> None:
    """
    构造函数

    Args:
      methodName: 默认测试方法

    Returns:
      return:     无

    """
    super().__init__(methodName=methodName)

    # 创建日志器
    self._get_logger()


  def _get_logger(
    self,
    logging_config_path  = _util.path.framework.abs_path(_util.path.join(
      _meta.CONFIG_DIR, _meta.CONFIGs.LOGGING
    )),                                     # 配置文件路径
    config_file_encoding = 'utf-8'          # 配置文件默认用UTF-8编码
  ) -> None:
    """
    创建日志器

    Args:
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
        add_func_2_obj(self, self._logger, fn)

    # 导入logging内置日志级别
    for fn in [
      'info',
      'warning',
      'error'
    ]:
      add_func_2_obj(self, self._logger, fn)


  def trace(self, msg, *args, **kwargs) -> None:
    """在日志中输出详细信息"""
    ...

  def info(self, msg, *args, **kwargs) -> None:
    """在日志中输出一般信息"""
    ...

  def warning(self, msg, *args, **kwargs) -> None:
    """在日志中输出警告信息"""
    ...

  def error(self, msg, *args, **kwargs) -> None:
    """在日志中输出错误信息"""
    ...

  def fatal(self, msg, *args, **kwargs) -> None:
    """在日志中输出致命错误信息"""
    ...

  def _case(self, msg, *args, **kwargs) -> None:
    """在日志中输出测试用例标题"""
    ...

  def _unit(self, msg, *args, **kwargs) -> None:
    """在日志中输出测试单元标题"""
    ...

  def step(self, msg, *args, **kwargs) -> None:
    """在日志中输出测试步骤"""
    ...

  def _pass(self, msg, *args, **kwargs) -> None:
    """在日志中输出测试成功"""
    ...

  def _fail(self, msg, *args, **kwargs) -> None:
    """在日志中输出测试失败"""
    ...

