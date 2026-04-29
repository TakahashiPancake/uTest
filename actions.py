from utest import Action
import uiautomator2 as u2

class Device(object):
  device_serial = '9XKZ699LBEAQAEZ9'
  device = None
  package_name = 'com.xiaomi.smarthome'


class ActionConnect(Action):

  def connect_device(self):
    # 尝试连接设备
    try:
      Device.device = u2.connect(Device.device_serial)
      self.info(f'设备信息: {Device.device.info}')  # 获取设备信息
    except Exception as e:
      self.assertTrue(False, e)


class ActionMiJia(Action):

  def launch_app(self):
    # 启动应用
    try:
      Device.device.app_start(Device.package_name)
    except Exception as e:
      self.assertTrue(False, e)

action_connect = ActionConnect()

action_mijia = ActionMiJia()

