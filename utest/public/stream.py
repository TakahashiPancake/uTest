"""
Copyright (c) 2026 Yidong Zhu

Repository: https://github.com/TakahashiPancake/uTest

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

"""
import sys as _sys
from utest.util.stream import StringIO as _StringIO

# 创建一个同步输入输出流
sync_output_stream = _StringIO(sync_output = _sys.stderr)

