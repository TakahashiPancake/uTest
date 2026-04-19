import os as _os
import platform as _platform_
from typing import Literal # 导入类型



class System(object):

  # 系统平台
  platform = None

  def __init__(self) -> None:
    self.platform = self._platform

  @property
  def _platform(self) -> _platform_.uname_result:
    return _platform_.uname()

  def set_cmd_encoding(self,
    encoding: Literal[
      'utf-8', 'UTF-8',
      'GBK',   'gbk'
    ]
  ) -> None:
    """设定命令行编码"""

    code_pages = {
      'utf-8': '65001',
      'UTF-8': '65001'
    }

    # TODO: 兼容各系统命令行操作
    if self.platform.system == 'Windows':
      # Windows chcp命令
      _os.system(f'chcp {code_pages[encoding]}')
    elif self.platform.system == 'Linux':
      ...
    else:
      ...


system = System()

if __name__ == '__main__':
  system.set_cmd_encoding('utf-8')
