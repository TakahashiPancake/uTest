import sys
import io
from collections.abc import Callable
from contextlib import redirect_stdout, redirect_stderr
import functools
import utest.util.path as path_util
import utest.util.framework as framework_util


def redirect_module_output(
  module_name: str,
  output_path: str = None
) -> Callable:
  """
  装饰器工厂 - 重定向模块输出

  Args:
    module_name: 模块名称
    output_path: 输出日志路径

  Returns:
    return: 被封装的方法

  """
  def decorator(func):
    """装饰器"""

    # 导入外部方法
    get_dir_path         = path_util.dir_path
    create_dirs          = path_util.create_dirs
    write_string_to_file = framework_util.write_string_to_file
    get_var_name         = framework_util.get_var_name

    if output_path is not None:

      # 获取文件夹路径
      dir_path = get_dir_path(output_path)

    else:
      raise ValueError(f'{get_var_name(output_path)} should not be None!')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      """封装器"""

      # 创建输入输出流
      io_stream = io.StringIO()

      # 重定向到输入输出流
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
      write_string_to_file(str_, output_path)

      return result

    return wrapper

  return decorator

