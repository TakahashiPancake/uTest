from utest import TestCase
from action.common.connect_device import action_connect

class BaseConnectDevice(TestCase):
  def setUp(self):
    super().setUp()
    self.info('前置条件：尝试连接设备')
    action_connect.connect_device()
  def tearDown(self):
    super().tearDown()

