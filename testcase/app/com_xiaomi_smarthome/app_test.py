from testcase.base.app.com_xiaomi_smarthome.app_test import BaseMijiaAppTest
from action.app.com_xiaomi_smarthome.app_test import action_mijia


class TC_001_First_Time_Login(BaseMijiaAppTest):
  def unit_01(self):
    self.step('1. 关闭引导页')
    action_mijia.close_onboarding_page()

class TC_002_Change_Locale(BaseMijiaAppTest):
  def unit_01(self):
    self.step('1. 点击我的')
    action_mijia.click_profile()
    self.step('2. 点击更多设置')
    action_mijia.click_settings()
    self.step('3. 点击地区')
    action_mijia.click_settings_locale()
    self.step('4. 点击英国')
    action_mijia.click_settings_locale_igirisu()
    self.step('5. 点击确认切换')
    action_mijia.click_settings_locale_igirisu_ok()

