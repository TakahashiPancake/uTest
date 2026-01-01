"""
Utility

- 禁止在文件顶部导入第三方包

"""
import functools
from typing import Literal
from contextlib import redirect_stdout
from contextlib import redirect_stderr
import inspect
import io
import sys
import os


class FrameworkUtil(object):
  """复用功能"""

  # 文件写模式
  write_modes = Literal[
    "w", "wt", "tw",
    "a", "at", "ta",
    "x", "xt", "tx",
    "w+", "+w", "wt+", "w+t", "+wt", "tw+", "t+w", "+tw",
    "a+", "+a", "at+", "a+t", "+at", "ta+", "t+a", "+ta",
    "x+", "+x", "xt+", "x+t", "+xt", "tx+", "t+x", "+tx"
  ]

  # 文件读模式
  read_modes = Literal[
    "r", "rt", "tr",
    "r+", "+r", "rt+", "r+t", "+rt", "tr+", "t+r", "+tr",
    "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"
  ]


  class RedirectLogging(object):
    """
    装饰器 - 重置logging

    Args:
      path:   重定向日志路径

    Returns:
      return: 被封装的方法

    """
    # 定义模块名
    _module_name = 'logging'


    def __init__(self, path: str = None) -> None:
      """
        初始化方法

        Args:
          path:   重定向日志路径

        Returns:
          return: 无

      """
      # 获取外部类
      self.Outer = FrameworkUtil

      # 导入外部类方法
      self._abs_path_in_framework  = self.Outer.abs_path_in_framework
      self._get_dir_path_from_path = self.Outer.get_dir_path_from_path
      self._create_directories     = self.Outer.create_directories
      self._write_string_to_file   = self.Outer.write_string_to_file
      self._get_var_name           = self.Outer.get_var_name

      if path is not None:
        # 文件绝对路径
        self._abs_path = self._abs_path_in_framework(path)

        # 文件夹绝对路径
        self._dir_path = self._get_dir_path_from_path(self._abs_path)

      else:
        raise ValueError(f'{self._get_var_name(path)}的值不应该为None!')


    def __call__(self, func):

      @functools.wraps(func)
      def wrapper(*args, **kwargs):
        """
        封装器

        Args:
          args:
          kwargs:

        Return:
          return:

        """
        io_stream = io.StringIO()

        # 执行pip命令，重定向到输入输出流
        with redirect_stdout(io_stream):
          with redirect_stderr(io_stream):

            # 导入模块
            if self._module_name not in sys.modules:
              sys.modules[self._module_name] = __import__(self._module_name)

            # 执行被封装的函数
            result = func(*args, **kwargs)

            # 移除模块
            if self._module_name in sys.modules:
              del sys.modules[self._module_name]

        str_: str = io_stream.getvalue()

        # 创建文件夹
        self._create_directories(self._dir_path)

        # 写入日志
        self._write_string_to_file(str_, self._abs_path)

        return result

      return wrapper


  def read_json_config(self,
    config_path: str,
    encoding: str = 'utf-8'
  ) -> dict:
    """
    读取json格式的日志文件

    Args:
      config_path: 配置文件路径
      encoding:    配置文件编码（默认：utf-8）

    Returns:
      return:      配置（字典）

    """
    import json

    # 读取配置文件
    with open(
      self.abs_path_in_framework(config_path),
      'r',
      encoding=encoding
    ) as config_file:

      config = json.load(config_file)

    return config


  def read_yaml_config(self,
    config_path: str,
    encoding: str = 'utf-8'
  ) -> dict:
    """
    读取json格式的日志文件

    Args:
      config_path: 配置文件路径
      encoding:    配置文件编码（默认：utf-8）

    Returns:
      return:      配置（字典）

    """
    import yaml

    # 读取配置文件
    with open(
      self.abs_path_in_framework(config_path),
      'r',
      encoding=encoding
    ) as config_file:
      config = yaml.safe_load(config_file)

    return config


  @staticmethod
  def abs_path_in_framework(path: str) -> str:
    """
    获取包内绝对路径

    Args:
      path:   路径

    Returns:
      return: 绝对路径

    """
    if os.path.isabs(path):
      return path

    else:
      # 获取包的根目录
      pkg_root_path = os.path.dirname(os.path.abspath(__file__))

      # 返回绝对路径
      return str(os.path.join(pkg_root_path, path))


  @staticmethod
  def get_dir_path_from_path(file_path: str) -> str:
    """
    通过文件路径获取所在文件夹路径

    Args:
      file_path: 文件路径

    Returns:
      return:    文件所在文件夹路径

    """
    dir_path = os.path.dirname(file_path)

    return dir_path


  @staticmethod
  def create_directories(path: str) -> None:
    """
    递归创建目录

    Args:
      path:   路径

    Returns:
      return: 无

    """
    if not os.path.exists(path):
      os.makedirs(path)


  @staticmethod
  def write_string_to_file(
    content: str,
    file_path: str,
    mode: write_modes = 'wt',
    encoding: str = 'utf-8'
  ) -> None:
    """
    将文本写入文件

    Args:
      content:   文本内容
      file_path: 文件路径
      mode:      写入模式（默认为'w'）
      encoding:  文件编码

    """
    with open(
      file     = file_path,
      mode     = mode,
      encoding = encoding
    ) as file:
      file.write(content)


  @staticmethod
  def get_var_name(var) -> str | None:
    """
    获取变量名（单层作用域）

    Args:
      var:    变量

    Returns:
      return: 变量名称

    """
    frame = inspect.currentframe().f_back

    for name, value in frame.f_locals.items():
      if value is var:
        return name

    return None


framework_util = FrameworkUtil()

