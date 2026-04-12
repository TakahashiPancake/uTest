import sys as _sys
import io as _io
from collections.abc import Callable # 导入类型
from contextlib import redirect_stdout as _redirect_stdout, redirect_stderr as _redirect_stderr
import functools as _func_tools
import utest.util.path as _path
import utest.util.framework as _framework


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
    get_dir_path         = _path.dir_path
    create_dirs          = _path.create_dirs
    write_string_to_file = _framework.write_string_to_file
    get_var_name         = _framework.get_var_name

    if output_path is not None:

      # 获取文件夹路径
      dir_path = get_dir_path(output_path)

    else:
      raise ValueError(f'{get_var_name(output_path)} should not be None!')

    @_func_tools.wraps(func)
    def wrapper(*args, **kwargs):
      """封装器"""

      # 创建输入输出流
      io_stream = _io.StringIO()

      # 重定向到输入输出流
      with _redirect_stdout(io_stream):
        with _redirect_stderr(io_stream):

          # 导入模块
          if module_name not in _sys.modules:
            _sys.modules[module_name] = __import__(module_name)

          # 执行被封装的函数
          result = func(*args, **kwargs)

          # 移除模块
          if module_name in _sys.modules:
            del _sys.modules[module_name]

      str_: str = io_stream.getvalue()

      # 创建文件夹
      create_dirs(dir_path)

      # 写入日志
      write_string_to_file(str_, output_path)

      return result

    return wrapper

  return decorator

