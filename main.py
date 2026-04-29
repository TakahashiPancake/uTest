from utest import HTMLTestExecutor
from cases import TC_Launch_MiJia

if __name__ == '__main__':
  html_executor = HTMLTestExecutor()
  html_executor.load(TC_Launch_MiJia)
  html_executor.run()


