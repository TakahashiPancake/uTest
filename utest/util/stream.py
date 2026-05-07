"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

"""
import io as _io
from typing import TextIO as _TextIO


# 重写StringIO
class StringIO(_io.StringIO):

  _output: _TextIO | None = None

  def __init__(self, sync_output: _TextIO | None = None) -> None:
    """
    Args:
      sync_output:   同步输出流

    Returns:
      return: 无
    """

    # 同步输出到流
    self._output = sync_output

    # 调用父类构造方法
    super().__init__()

  ####################
  ### C++式编程
  ####################

  def clear_buffer(self) -> int:
    """
    清空缓存区

    Return:
      Error levels:
        ...

    """
    self.truncate(0)
    self.seek(0)
    return 0

  def print_buffer(self, file: _TextIO | None = None) -> int:
    """
    输出缓存区

    Args:
      file: 文件

    Return:
      Error levels:
        ...

    """
    print(self.getvalue(), file=file)
    return 0


  ####################
  ### 重写父类方法
  ####################

  # 重写write()方法
  def write(self, s: str, /) -> int:
    # 将字符串打印到_output
    print(s, sep='', end='', file=self._output)

    # 调用父类write()方法
    return super().write(s)


if __name__ == '__main__':
  from sys import stderr as _stderr
  _io.StringIO()
  string_io = StringIO(sync_output = _stderr)
  string_io.write('hello world')
  string_io.print_buffer()
  string_io.clear_buffer()
  print(string_io.getvalue())
