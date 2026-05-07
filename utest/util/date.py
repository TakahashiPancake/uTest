"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

"""
import datetime as _datetime

class DateTime(object):
  @staticmethod
  def get_formatted_datetime(format_: str, /):
    return _datetime.datetime.now().strftime(format_)

