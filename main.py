from utest import HTMLTestExecutor
from testcase.app.com_xiaomi_smarthome.app_test import *

if __name__ == '__main__':
  html_executor = HTMLTestExecutor()
  html_executor.load(TC_001_First_Time_Login, TC_002_Change_Locale)
  html_executor.run()
