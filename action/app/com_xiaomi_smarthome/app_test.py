import universal.device as device
from action.common.common import ui
from action.common.common import time
from utest import Action

class ActionMiJia(Action):

  def launch_app(self):
    """启动应用"""
    # 尝试启动应用
    try:
      device.device.app_start(device.package_name)
    except Exception as e:
      self.assertTrue(False, e)
    # 等待5秒
    self.info('等待 5 秒，APP启动')
    time.wait_about(5)

  def close_onboarding_page(self):
    """关闭引导页"""
    self.info('点击同意')
    device.device.xpath('//*[@resource-id="com.xiaomi.smarthome:id/appwidget_ok"]').click()
    time.wait_about(3)
    self.info('点击同意并继续')
    device.device.xpath('//*[@resource-id="com.xiaomi.smarthome:id/x3"]').click()
    time.wait_about(3)
    self.info('点击同意')
    device.device.xpath('//*[@resource-id="com.xiaomi.smarthome:id/x3"]').click()
    time.wait_about(3)
    self.close_onboarding_page_extra()
    self.info('尝试同意定位权限')
    try:
      self.info('点击仅在使用中允许')
      device.device.xpath('//*[@text="仅在使用中允许"]').click()
    except Exception as e:
      self.warning('无法授予定位权限或无定位弹窗')
      self.warning(e)
    time.wait_about(3)
    self.info('尝试授权米家生态')
    try:
      self.info('点击确定')
      device.device.xpath('//*[@resource-id="com.xiaomi.smarthome:id/x3"]').click()
    except Exception as e:
      self.warning('无法授权或无弹窗')
      self.warning(e)
    time.wait_about(3)


  def close_onboarding_page_extra(self):
    """关闭引导页（额外）"""
    self.info('点击"去体验"')
    device.device.xpath('//android.widget.TextView[@text="去体验"]').click()
    time.wait_about(3)

  def click_profile(self):
    self.info('点击我的')
    device.device.xpath('//*[@text="我的"]').click()
    time.wait_about(3)

  def click_settings(self):
    self.info('点击更多设置')
    ui.click_menu_item_by_xpath_down('//*[@text="更多设置"]')
    time.wait_about(3)

  def click_settings_locale(self):
    self.info('点击地区')
    ui.click_menu_item_by_xpath_down('//*[@text="地区"]')
    time.wait_about(3)

  def click_settings_locale_igirisu(self):
    self.info('点击英国')
    ui.click_menu_item_by_xpath_up('//*[@text="英国"]')
    time.wait_about(3)

  def click_settings_locale_igirisu_ok(self):
    self.info('点击确认')
    device.device.xpath('//*[@resource-id="com.xiaomi.smarthome:id/x3"]').click()
    time.wait_about(5)

  def close_app(self):
    """关闭应用"""
    # 尝试关闭应用
    try:
      device.device.app_stop(device.package_name)
    except Exception as e:
      self.assertTrue(False, e)
    # 等待1秒
    time.wait_about(1)

action_mijia = ActionMiJia()

if __name__ == '__main__':
  from action.common.connect_device import action_connect
  action_connect.connect_device()
  action_mijia.launch_app()
  action_mijia.close_onboarding_page()
  #action_mijia.close_onboarding_page_extra()
