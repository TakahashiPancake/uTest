import universal.device as device
from utest import Action
import time as time_
import random

class Time(Action):
  def wait_about(self, seconds, deviation_pct = 10):
    if random.random()<0.5:
      deviation_pct *= -1
    actual = seconds * (1 + random.random() * (deviation_pct/100))
    self.info(f'等待约 {seconds} 秒（实际 {actual:.2f}）')
    time_.sleep(actual)


time = Time()


class UI(Action):
  def click_menu_item_by_xpath_down(self, xpath: str):
    counter = 1
    while True:
      self.trace(f'第 {counter} 次寻找元素')
      if device.device.xpath(xpath).wait(timeout=2):
        time.wait_about(1)
        device.device.xpath(xpath).click()
        return
      else:
        self.trace('找不到元素，下滑寻找元素')
        device.device.swipe_ext('up', scale=0.5)
        time.wait_about(0.5)
      if counter >= 10:
        self.warning(f'第 {counter} 次找不到元素，取消操作')
        break
      counter += 1
    counter = 1
    while True:
      self.trace(f'第 {counter} 次寻找元素')
      if device.device.xpath(xpath).wait(timeout=2):
        time.wait_about(1)
        device.device.xpath(xpath).click()
        return
      else:
        self.trace('找不到元素，上滑寻找元素')
        device.device.swipe_ext('down', scale=0.5)
        time.wait_about(0.5)
      if counter >= 20:
        self.warning(f'第 {counter} 次找不到元素，取消操作')
        break
      counter += 1
    raise Exception('找不到元素')

  def click_menu_item_by_xpath_up(self, xpath: str):
    counter = 1
    while True:
      self.trace(f'第 {counter} 次寻找元素')
      if device.device.xpath(xpath).wait(timeout=2):
        time.wait_about(1)
        device.device.xpath(xpath).click()
        return
      else:
        self.trace('找不到元素，下滑寻找元素')
        device.device.swipe_ext('down', scale=0.5)
        time.wait_about(0.5)
      if counter >= 10:
        self.warning(f'第 {counter} 次找不到元素，取消操作')
        break
      counter += 1
    counter = 1
    while True:
      self.trace(f'第 {counter} 次寻找元素')
      if device.device.xpath(xpath).wait(timeout=2):
        time.wait_about(1)
        device.device.xpath(xpath).click()
        return
      else:
        self.trace('找不到元素，上滑寻找元素')
        device.device.swipe_ext('up', scale=0.5)
        time.wait_about(0.5)
      if counter >= 20:
        self.warning(f'第 {counter} 次找不到元素，取消操作')
        break
      counter += 1
    raise Exception('找不到元素')


ui = UI()
