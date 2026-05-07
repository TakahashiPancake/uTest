"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

"""
import os as _os

def abs_path(path: str | None) -> str:
  """
  返回包内文件的绝对路径

  Args:
    path:   路径

  Returns:
    return: 绝对路径

  """
  # 获取包的根目录
  root_path = _os.path.dirname(_os.path.abspath(__file__))

  if path is None:
    return root_path

  elif _os.path.isabs(path):
    return path

  else:
    # 返回绝对路径
    return str(_os.path.join(root_path, path))

