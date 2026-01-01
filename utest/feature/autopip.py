from .util import util
from contextlib import redirect_stdout
import io

class AutoPIP(object):
  """自动调用pip安装依赖包"""

  _log_path = 'log/autopip.log'

  _packages_installed = False


  @util.RedirectLogging(_log_path)
  def main(self,
    config_path, # 必须使用json格式配置文件
    encoding = 'utf-8',
    upgrade  = False
  ):
    """
    主方法 - 自动调用pip安装依赖包

    Args:
      config_path: 配置文件路径；
                   （json格式配置文件，使用python内置json解析器解析）
      encoding:    配置文件编码（可选）
      upgrade:     是否升级pip

    Returns:
      return:      无

    """
    import pip

    def pip_cmd(args: list) -> None:
      print('COMMAND:', 'pip', ' '.join(args), sep=' ')
      pip.main(args)


    def upgrade_pip():
      print('Upgrading pip...')
      pip_cmd(['install', '--upgrade', 'pip'])


    def read_pip_list():
      print('Reading pip list...')

      # 定义一个输入输出流
      io_stream = io.StringIO()

      # 执行pip命令，重定向到输入输出流
      with redirect_stdout(io_stream):
        pip_cmd(['list'])

      # 从输入输出流中读取pip包列表
      packages: str = io_stream.getvalue()

      # 输出pip列表
      print(packages)

      return packages


    # 升级pip
    if upgrade:
      upgrade_pip()

    # 未安装依赖包
    if not self._packages_installed:

      pip_packages = read_pip_list()

      # 读取配置文件
      config = util.read_json_config(
        config_path = config_path,
        encoding    = encoding
      )

      # 安装包
      if 'requirements' in config:
        for package in config.get('requirements'):
          if package.lower() not in pip_packages.lower():
            if 'pip_index_url' in config:
              print('Installing:', package, sep=' ')
              pip.main(
                ['install', '--no-input', package, '-i', config.get('pip_index_url')]
              )
            else:
              pip.main(['install', '--no-input', package])

      self._packages_installed = True

    # 已安装依赖包
    else:
      print('Packages already installed!')


autopip = AutoPIP()

