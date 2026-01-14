import logging
import unittest
import utest.util as util
import utest.meta as meta
from .patch import patcher



class Base(unittest.TestCase):
  """
  框架基类

  1. 框架基类继承自unittest.TestCase

  2. 包含一个创建日志器的方法

  3. 声明日志方法

  """
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
    logger_name          = 'uLogger',       # uLogger是uTest框架下的日志器
    logging_config_path  = util.path.join(
      meta.CONFIG_DIR, meta.CONFIGs.LOGGING
    ),                                      # 配置文件路径
    config_file_encoding = 'utf-8'          # 配置文件默认用UTF-8编码
  ) -> None:
    """
    创建日志器

    Args:
      logger_name:          日志器名称
      logging_config_path:  日志器配置文件路径
      config_file_encoding: 配置文件编码

    Returns:
      return:               无

    """
    # 定义字段名称
    more_levels = 'more_levels'

    def add_func_2_obj(obj, instance_name, func_name):
      """
      将（日志）方法绑定到类

      Args:
        obj:           对象
        instance_name: 实例名称
        func_name:     方法名称

      Returns:
        return:        无

      """
      setattr(
        obj,
        func_name,
        getattr(
          getattr(
            obj,
            instance_name
          ),
          func_name
        )
      )

    # 给logging打补丁
    patcher.patch_logging(logging_config_path)

    # 创建日志器并绑定到类
    setattr(self, logger_name, logging.getLogger(logger_name))

    # 读取配置文件
    config = util.framework.read_yaml_config(
      config_path = logging_config_path,
      encoding    = config_file_encoding
    )

    # 导入更多日志级别
    if more_levels in config:
      for fn in config[more_levels].keys():
        add_func_2_obj(self, logger_name, fn)

    # 导入logging内置日志级别
    for fn in [
      'info',
      'warning',
      'error'
    ]:
      add_func_2_obj(self, logger_name, fn)


  def trace(self, msg, *args, **kwargs):
    """在日志中输出详细信息"""
    pass

  def info(self, msg, *args, **kwargs):
    """在日志中输出一般信息"""
    pass

  def warning(self, msg, *args, **kwargs):
    """在日志中输出警告信息"""
    pass

  def error(self, msg, *args, **kwargs):
    """在日志中输出错误信息"""
    pass

  def fatal(self, msg, *args, **kwargs):
    """在日志中输出致命错误信息"""
    pass

  def _case(self, msg, *args, **kwargs):
    """在日志中输出测试用例标题"""
    pass

  def _unit(self, msg, *args, **kwargs):
    """在日志中输出测试单元标题"""
    pass

  def step(self, msg, *args, **kwargs):
    """在日志中输出测试步骤"""
    pass

  def _pass(self, msg, *args, **kwargs):
    """在日志中输出测试成功"""
    pass

  def _fail(self, msg, *args, **kwargs):
    """在日志中输出测试失败"""
    pass

