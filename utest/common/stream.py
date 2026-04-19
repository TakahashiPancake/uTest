import sys as _sys
from utest.util.stream import StringIO as _StringIO

# 创建一个同步输入输出流
sync_stream = _StringIO(sync_output = _sys.stderr)

