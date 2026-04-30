from testcase.base.connect_device import BaseConnectDevice
from action.app.com_xiaomi_smarthome.app_test import action_mijia

class BaseMijiaAppTest(BaseConnectDevice):
  def setUp(self):
    super().setUp()
    self.info('前置条件：打开米家APP')
    action_mijia.launch_app()
  def tearDown(self):
    self.info('后置处理：关闭米家APP')
    action_mijia.close_app()
    super().tearDown()

