"""
Copyright (c) 2026 Yidong Zhu

Repository: https://github.com/TakahashiPancake/uTest

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

"""
import datetime as _datetime

class DateTime(object):
  @staticmethod
  def get_formatted_datetime(format_: str, /):
    return _datetime.datetime.now().strftime(format_)

