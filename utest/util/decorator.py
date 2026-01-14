import sys
import io
from collections.abc import Callable
from contextlib import redirect_stdout
from contextlib import redirect_stderr
import functools
import utest.util.path as path_util
import utest.util.framework as framework_util


def redirect_logging(path: str = None) -> Callable:
  """
  封装器 - 重置logging

  Args:
    path:   重定向日志路径

  Returns:
    return: 被封装的方法

  """
  def decorator(func):
    """装饰器"""

    # 模块名
    module_name = 'logging'

    # 导入外部方法
    abs_path_in_framework  = path_util.abs_path_in_framework
    get_dir_path_from_path = path_util.get_dir_path_from_path
    create_dirs            = path_util.create_dirs
    write_string_to_file   = framework_util.write_string_to_file
    get_var_name           = framework_util.get_var_name

    if path is not None:
      # 文件绝对路径
      abs_path = abs_path_in_framework(path)

      # 文件夹绝对路径
      dir_path = get_dir_path_from_path(abs_path)

    else:
      raise ValueError(f'{get_var_name(path)}的值不应该为None!')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      """封装器"""

      # 创建输入输出流
      io_stream = io.StringIO()

      # 执行pip命令，重定向到输入输出流
      with redirect_stdout(io_stream):
        with redirect_stderr(io_stream):

          # 导入模块
          if module_name not in sys.modules:
            sys.modules[module_name] = __import__(module_name)

          # 执行被封装的函数
          result = func(*args, **kwargs)

          # 移除模块
          if module_name in sys.modules:
            del sys.modules[module_name]

      str_: str = io_stream.getvalue()

      # 创建文件夹
      create_dirs(dir_path)

      # 写入日志
      write_string_to_file(str_, abs_path)

      return result

    return wrapper

  return decorator

