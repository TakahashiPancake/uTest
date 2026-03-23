import os
import utest._root as _framework_root


class _Framework(object):

  @staticmethod
  def abs_path(path: str | None) -> str:
    """
    返回包内文件的绝对路径

    Args:
      path:   路径

    Returns:
      return: 绝对路径

    """
    return _framework_root.abs_path(path)


framework = _Framework()


def dir_path(file_path: str) -> str:
  """
  通过文件路径获取所在文件夹路径

  Args:
    file_path: 文件路径

  Returns:
    return:    文件所在文件夹路径

  """
  dir_path_ = os.path.dirname(file_path)

  return dir_path_


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
  """拼接路径"""

  return os.path.join(path, *paths)

