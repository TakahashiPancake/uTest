import io as _io
from sys import stdout as _stdout
from typing import TextIO # 导入类型


class StreamBuffer(object):
  """
  文本流缓存

  - 重定向文本输出到一个 io.StringIO 对象

  """
  ####################
  ### C++式编程
  ####################

  # 定义调用行为
  def __call__(self):
    return self.buffer

  buffer = _io.StringIO()

  def clear(self) -> int:
    """
    清空缓存区

    Error levels:
      ...

    """
    self.buffer.truncate(0)
    self.buffer.seek(0)
    return 0

  def output(self, file: TextIO | None = _stdout) -> int:
    """
    输出缓存区

    Args:
      file: 文件

    Error levels:
      ...

    """
    print(self.buffer.getvalue(), file=file)
    return 0

