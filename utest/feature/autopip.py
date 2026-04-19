import sys as _sys
import io as _io
from typing import Any as _Any
from contextlib import redirect_stdout as _redirect_stdout
from contextlib import redirect_stderr as _redirect_stderr
from utest.util import date as _date, path as _path, framework as _framework
import utest.util.decorator as _decorator
import utest.meta as _meta


class AutoPIP(object):
  """自动调用pip安装依赖包"""

  _packages_installed = False

  @_decorator.redirect_module_output(
    module_name = 'logging',
    output_path = _path.framework.abs_path(_path.join(
      _meta.LOG_DIR, _meta.LOGs.AUTOPIP
    ))
  )
  def main(self,
    config_path: str, # 必须使用json格式配置文件
    encoding: str = 'utf-8',
    upgrade: bool = False
  ) -> _Any:
    """
    主方法

    - 面向过程

    - 自动调用pip安装依赖包

    Args:
      config_path: 配置文件路径；
                   （json格式配置文件，使用python内置json解析器解析）
      encoding:    配置文件编码（可选）
      upgrade:     是否升级pip

    Returns:
      return:      无

    """
    import ensurepip

    def print_l(*args, **kwargs) -> None:
      """输出流到stderr"""
      print(*args, **kwargs, file=_sys.stderr)

    def log_print(*args, **kwargs) -> None:
      """输出日志"""
      # 输出
      print_l(_date.DateTime.get_formatted_datetime('%Y-%m-%d %H:%M:%S.%f'))
      print_l(*args, **kwargs)

    def ensure_pip() -> None:
      log_print('Insuring PIP')
      try:
        ensurepip.bootstrap()
        log_print('PIP installed successfully')
      except Exception as e:
        raise e

    # 确保pip已安装
    try:
      pip = __import__('pip')
    except ImportError:
      ensure_pip()
      pip = __import__('pip')

    def pip_cmd(args: list) -> None:
      """
      pip命令

      Args:
        args:   pip命令参数列表

      Returns:
        return: 无

      """
      log_print('COMMAND:', 'pip', ' '.join(args), sep=' ')
      pip.main(args)


    def upgrade_pip() -> None:
      """更新PIP"""
      pip_cmd(['install', '--upgrade', 'pip'])



    def read_pip_list() -> str:
      """
      读取PIP列表

      Returns:
         return: PIP列表（文本）

      """
      # 定义输入输出流
      err_stream = _io.StringIO()
      io_stream  = _io.StringIO()

      # 执行pip命令，重定向到输入输出流
      with _redirect_stderr(err_stream):
        with _redirect_stdout(io_stream):
          pip_cmd(['list'])

      # 从输入输出流中读取

      # 日志
      log_info: str = err_stream.getvalue()

      # Python包
      packages: str = io_stream.getvalue()

      # 输出pip列表
      print_l(log_info)
      print(packages)

      return packages


    # 升级pip
    if upgrade:
      upgrade_pip()

    # 未安装依赖包
    if not self._packages_installed:

      pip_packages = read_pip_list()

      # 读取配置文件
      config = _framework.read_json_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 安装包
      if 'required_packages' in config:
        for package in config.get('required_packages'):
          if package.lower() not in pip_packages.lower():
            # 通过requirements安装
            if 'requirements' in config:
              requirements = config.get('requirements')
              if 'pip_index_url' in config:
                pip_cmd([
                  'install',
                  '-r',
                  _path.join(_path.framework.abs_path(_meta.CONFIG_DIR), requirements),
                  '-i',
                  config.get('pip_index_url')
                ])
              else:
                pip_cmd([
                  'install',
                  '-r',
                  _path.join(_path.framework.abs_path(_meta.CONFIG_DIR), requirements)
                ])
              break # 跳出遍历
            # 无法通过requirements安装时，使用命令安装
            if 'pip_index_url' in config:
              pip_cmd(['install', '--no-input', package, '-i', config.get('pip_index_url')])
            else:
              pip_cmd(['install', '--no-input', package])

      self._packages_installed = True

    # 已安装依赖包
    else:
      print('Packages already installed!')


autopip = AutoPIP()

