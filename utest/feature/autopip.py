import sys
import io
from contextlib import redirect_stdout
from contextlib import redirect_stderr
from datetime import datetime
import utest.util as util
import utest.util.decorator as decorator
import utest.meta as meta


class AutoPIP(object):
  """自动调用pip安装依赖包"""

  _packages_installed = False


  @decorator.redirect_module_output(
    module_name = 'logging',
    output_path = util.path.framework.abs_path(util.path.join(
      meta.LOG_DIR, meta.LOGs.AUTOPIP
    ))
  )
  def main(self,
    config_path, # 必须使用json格式配置文件
    encoding = 'utf-8',
    upgrade  = False
  ) -> ...:
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
    import pip

    def printl(*args, **kwargs) -> None:
      print(*args, **kwargs, file=sys.stderr)


    def log_print(*args, **kwargs) -> None:
      printl(datetime.now())
      printl(*args, **kwargs)


    def pip_cmd(args: list) -> None:
      log_print('COMMAND:', 'pip', ' '.join(args), sep=' ')
      pip.main(args)


    def upgrade_pip() -> None:
      pip_cmd(['install', '--upgrade', 'pip'])


    def read_pip_list() -> str:
      # 定义输入输出流
      err_stream = io.StringIO()
      io_stream  = io.StringIO()

      # 执行pip命令，重定向到输入输出流
      with redirect_stderr(err_stream):
        with redirect_stdout(io_stream):
          pip_cmd(['list'])

      # 从输入输出流中读取

      # 日志
      log_info: str = err_stream.getvalue()

      # Python包
      packages: str = io_stream.getvalue()

      # 输出pip列表
      printl(log_info)
      print(packages)

      return packages


    # 升级pip
    if upgrade:
      upgrade_pip()

    # 未安装依赖包
    if not self._packages_installed:

      pip_packages = read_pip_list()

      # 读取配置文件
      config = util.framework.read_json_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 安装包
      if 'requirements' in config:
        for package in config.get('requirements'):
          if package.lower() not in pip_packages.lower():
            if 'pip_index_url' in config:
              pip_cmd(['install', '--no-input', package, '-i', config.get('pip_index_url')])
            else:
              pip_cmd(['install', '--no-input', package])

      self._packages_installed = True

    # 已安装依赖包
    else:
      print('Packages already installed!')


autopip = AutoPIP()

