import os

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

