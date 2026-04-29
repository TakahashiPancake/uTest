from utest import TestCase
from actions import action_connect, action_mijia

class PluginTestBase(TestCase):
  def setUp(self):
    super().setUp()
    self.step('前置步骤1. 连接设备')
    action_connect.connect_device()
    self.step('前置步骤2. 打开米家')
    action_mijia.launch_app()

class TC_Launch_MiJia(PluginTestBase):
  def unit_01(self):
    pass

