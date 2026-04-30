import uiautomator2 as u2
import public.device as device
from utest import Action
from action.common.common import time

class ActionConnect(Action):

  def connect_device(self):
    # 尝试连接设备
    if device.device is None:
      self.warning('设备未连接，尝试连接设备')
      try:
        device.device = u2.connect(device.device_serial)
        self.info(f'设备信息: {device.device.info}')  # 获取设备信息
      except Exception as e:
        self.assertTrue(False, e)
    else:
      self.warning('设备已连接，不用再连接')
    # 等待1秒
    time.wait_about(1)
    self.info('设置全局元素定位超时为 3 秒')
    device.device.implicitly_wait(3)


action_connect = ActionConnect()

