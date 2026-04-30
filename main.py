from utest import HTMLTestExecutor
from example_case import TC_001_Framework, TC_002_Framework

if __name__ == '__main__':
  executor = HTMLTestExecutor()
  executor.load(TC_001_Framework, TC_002_Framework)
  executor.run()
