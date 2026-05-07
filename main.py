"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

"""
from utest import HTMLTestExecutor
import example_case

if __name__ == '__main__':
  executor = HTMLTestExecutor()
  executor.load(example_case)
  executor.run()
