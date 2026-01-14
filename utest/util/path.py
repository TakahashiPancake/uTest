import os
import utest._root as root_util


abs_path_in_framework = root_util.abs_path_in_framework


def get_dir_path_from_path(file_path: str) -> str:
  """
  通过文件路径获取所在文件夹路径

  Args:
    file_path: 文件路径

  Returns:
    return:    文件所在文件夹路径

  """
  dir_path = os.path.dirname(file_path)

  return dir_path


def create_dirs(path: str) -> None:
  """
  递归创建目录

  Args:
    path:   路径

  Returns:
    return: 无

  """
  if not os.path.exists(path):
     os.makedirs(path)


def join(path: str, /, *paths: str) -> str:

  return os.path.join(path, *paths)

