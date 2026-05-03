from utest import HTMLTestExecutor
from example_case import \
  TEST_CASE_EXAMPLE_001, \
  TEST_CASE_EXAMPLE_002, \
  TEST_CASE_EXAMPLE_003, \
  TEST_CASE_EXAMPLE_004, \
  TEST_CASE_EXAMPLE_005

if __name__ == '__main__':
  executor = HTMLTestExecutor()
  executor.load(
    TEST_CASE_EXAMPLE_001,
    TEST_CASE_EXAMPLE_002,
    TEST_CASE_EXAMPLE_003,
    TEST_CASE_EXAMPLE_004,
    TEST_CASE_EXAMPLE_005
  )
  executor.run()
