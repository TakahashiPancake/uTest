import inspect as _inspect
from typing import Literal as _Literal


# 文件写模式
_write_mode = _Literal[
  "w", "wt", "tw",
  "a", "at", "ta",
  "x", "xt", "tx",
  "w+", "+w", "wt+", "w+t", "+wt", "tw+", "t+w", "+tw",
  "a+", "+a", "at+", "a+t", "+at", "ta+", "t+a", "+ta",
  "x+", "+x", "xt+", "x+t", "+xt", "tx+", "t+x", "+tx"
]

# 文件读模式
_read_mode = _Literal[
  "r", "rt", "tr",
  "r+", "+r", "rt+", "r+t", "+rt", "tr+", "t+r", "+tr",
  "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"
]


def read_json_config(
  config_path: str,
  encoding: str = 'utf-8'
) -> dict:
  """
  读取json格式的日志文件

  Args:
    config_path: 配置文件路径
    encoding:    配置文件编码（默认：utf-8）

  Returns:
    return:      配置（字典）

  """
  import json

  # 读取配置文件
  with open(
    config_path,
    'r',
    encoding=encoding
  ) as config_file:

    config = json.load(config_file)

  return config


def read_yaml_config(
  config_path: str,
  encoding: str = 'utf-8'
) -> dict:
  """
  读取json格式的日志文件

  Args:
    config_path: 配置文件路径
    encoding:    配置文件编码（默认：utf-8）

  Returns:
    return:      配置（字典）

  """
  import yaml

  # 读取配置文件
  with open(
    config_path,
    'r',
    encoding=encoding
  ) as config_file:
    config = yaml.safe_load(config_file)

  return config


def write_string_to_file(
  content: str,
  file_path: str,
  mode: _write_mode = 'wt',
  encoding: str = 'utf-8'
) -> None:
  """
  将文本写入文件

  Args:
    content:   文本内容
    file_path: 文件路径
    mode:      写入模式（默认为'w'）
    encoding:  文件编码

  """
  with open(
    file     = file_path,
    mode     = mode,
    encoding = encoding
  ) as file:
    file.write(content)


def get_var_name(var) -> str | None:
  """
  获取变量名（单层作用域）

  Args:
    var:    变量

  Returns:
    return: 变量名称

  """
  frame = _inspect.currentframe().f_back

  for name, value in frame.f_locals.items():
    if value is var:
      return name

  return None

