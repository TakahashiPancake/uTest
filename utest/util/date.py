import datetime as _datetime

class DateTime(object):
  @staticmethod
  def get_formatted_datetime(format_: str, /):
    return _datetime.datetime.now().strftime(format_)

