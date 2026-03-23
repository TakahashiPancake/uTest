import io
from typing import TextIO

class RedirectStream(object):
  """重定向文本输出到一个 io.StringIO 对象"""

  # C++式编写方法

  buffer = io.StringIO()

  def clear(self) -> int:
    self.buffer.truncate(0)
    self.buffer.seek(0)
    return 0

  def output(self, file: TextIO | None = None) -> int:
    print(self.buffer.getvalue(), file=file)
    return 0

redirect_stream = RedirectStream()

