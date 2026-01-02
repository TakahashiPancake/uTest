__all__ = ['TestCase', 'Action']

from .meta import RootMeta as Meta
from .util import root_util as util


# 安装模块
from .feature.autopip import autopip
autopip.main(
  config_path = util.path.join(
    Meta.CONFIG_DIR, Meta.CONFIGs.AUTOPIP
  )
)

# 修补模块
from .core.patch import patcher
patcher.patch_logging(
  config_path = util.path.join(
    Meta.CONFIG_DIR, Meta.CONFIGs.LOGGING
  )
)
patcher.patch_unittest(
  config_path = util.path.join(
    Meta.CONFIG_DIR, Meta.CONFIGs.UNITTEST
  )
)

# 导入模块
from .core.case import TestCase
from .core.action import Action

