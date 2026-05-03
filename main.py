from utest import HTMLTestExecutor
import example_case
from example_case import *

if __name__ == '__main__':
  executor = HTMLTestExecutor()
  executor.load(example_case)
  executor.run()
