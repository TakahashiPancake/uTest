<!--
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

-->
# uTest测试用例编写方法

### 测试用例的基本编写方法

1. 导入测试用例类

   ```python
   # 导入测试类
   from utest import TestCase
   ```

2. 编写测试用例

   ```python
   from utest import TestCase

   # 编写测试用例
   # - 类名: 测试用例编号
   # - 类:   继承自utest.TestCase
   class TEST_CASE_EXAMPLE_001(TestCase):

     # 前置条件
     # - precondition()方法: 测试用例（测试单元）的前置条件
     def precondition(self):
       self.info('这里是一些前置步骤')
       ...

     # 测试步骤
     # - testcase()方法: 测试用例（测试单元）的操作步骤
     def testcase(self):
       self.info('这里是一些测试步骤')
       ...

     # 后置条件
     # - postcondition()方法: 测试用例（测试单元）的后置条件
     def postcondition(self):
       self.info('这里是一些后置步骤')
       ...

     # 此外若需要给整个测试类添加前置条件和后置条件:
     # - 可使用 precondition_class()方法 和 postcondition_class()方法，
     #   但比较难用，不推荐使用
     @classmethod
     def precondition_class(cls) -> None:
       ...

     @classmethod
     def postcondition_class(cls) -> None:
       ...
   ```

3. 测试用例日志输出结果

   ```text
   2026-05-04 15:46:53,868 |  TEST_CASE | TEST_CASE_EXAMPLE_001
   ======================================================================
   2026-05-04 15:46:53,868 |  TEST_UNIT | testcase
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,868 |    PRECOND | 前置条件:
   2026-05-04 15:46:53,868 |       INFO | 这里是一些前置步骤
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,869 |       INFO | 这里是一些测试步骤
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,869 |   POSTCOND | 后置条件:
   2026-05-04 15:46:53,869 |       INFO | 这里是一些后置步骤
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,869 |       PASS | testcase OK (0.001023)s
   ```

### 编写测试日志

1. uTest框架内集成了多样化的日志输出方法

   - 我们可以在框架内使用以下方法输出测试日志

   ```python
   # 在日志中输出测试步骤
   def step(self, step: int, msg: str) -> None: ...

   # 在日志中输出调试信息
   # - 由于debug()方法被占用，所以框架内使用trace()方法代替debug()方法
   def trace(self, msg: str) -> None: ...

   # 在日志中输出提示信息
   def info(self, msg: str) -> None: ...

   # 在日志中输出警告信息
   def warn(self, msg: str) -> None: ...

   # 在日志中输出错误信息
   def error(self, msg: str) -> None: ...

   # 在日志中输出致命错误信息
   # - 发生致命错误时，直接停止测试用例，并将测试用例置为失败
   def fatal(self, msg: str) -> None: ...
   ```

2. 示例代码

   ```python
   from utest import TestCase

   class TEST_CASE_EXAMPLE_002(TestCase):

     def testcase(self):

       # 日志

       # 1. 输出测试步骤
       self.step(1, '测试步骤 1')
       self.step(2, '测试步骤 2')
       self.step(3, '测试步骤 3')

       # 输出日志

       # 1. 输出提示信息
       self.info('这是一行提示信息。')

       # 2. 输出警告信息
       self.warn('这是一行警告信息。')

       # 3. 输出错误信息
       self.error('这是一行错误信息。')

       # 4. 输出调试信息
       self.trace('这是一行调试信息。')

       # 5. 输出致命错误信息
       # - 致命错误发生时，测试用例（测试单元）置为失败
       self.fatal('这是一行致命错误信息。【致命错误发生时，测试用例（测试单元）置为失败】')

       ...
   ```

3. 日志输出结果

   ```text
   2026-05-04 15:46:53,869 |  TEST_CASE | TEST_CASE_EXAMPLE_002
   ======================================================================
   2026-05-04 15:46:53,869 |  TEST_UNIT | testcase
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,869 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,869 |       STEP | 1. 测试步骤 1
   2026-05-04 15:46:53,869 |       STEP | 2. 测试步骤 2
   2026-05-04 15:46:53,869 |       STEP | 3. 测试步骤 3
   2026-05-04 15:46:53,870 |       INFO | 这是一行提示信息。
   2026-05-04 15:46:53,870 |    WARNING | 这是一行警告信息。
   2026-05-04 15:46:53,870 |      ERROR | 这是一行错误信息。
   2026-05-04 15:46:53,870 |      DEBUG | 这是一行调试信息。
   2026-05-04 15:46:53,870 |      FATAL | 这是一行致命错误信息。【致命错误发生时，测试用例（测试单元）置为失败】
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,872 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,872 |       FAIL | testcase FAIL (0.003047)s
 
   ======================================================================
   FAIL [0.003047s]: example_case.TEST_CASE_EXAMPLE_002.testcase
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "D:\Users\LuxAEterna\Documents\PycharmProjects\hannto\utest\example_case.py", line 75, in testcase
       self.fatal('这是一行致命错误信息。【致命错误发生时，测试用例（测试单元）置为失败】')
     File "D:\Users\LuxAEterna\Documents\PycharmProjects\hannto\utest\utest\core\base.py", line 135, in fatal
       self.fail(msg)
     File "E:\python\Lib\unittest\case.py", line 703, in fail
       raise self.failureException(msg)
   AssertionError: 这是一行致命错误信息。【致命错误发生时，测试用例（测试单元）置为失败】
   ```

### 一个测试用例含有多个测试单元的编写方式

1. 一个测试用例有多个测试单元时，每个测试单元的方法用'unit_'打头命名

   ```python
   def unit_001(self): ...

   def unit_002(self): ...

   def unit_003(self): ...
   ```

2. 示例代码:

   ```python
   from utest import TestCase

   class TEST_CASE_EXAMPLE_003(TestCase):

     # - 一个测试用例有多个测试单元时，
     #   每个测试单元用 'unit_' 打头命名

     # 例:

     # 测试单元 1
     def unit_001(self):
       self.info('这是第 1 个测试单元')
       ...

     # 测试单元 2
     def unit_002(self):
       self.info('这是第 2 个测试单元')
       ...

     # 测试单元 3
     def unit_003(self):
       self.info('这是第 3 个测试单元')
       ...

     # 注意！
     # - 每个测试单元执行之前都会执行 同一个precondition()方法 和 同一个postcondition()方法，
     #   若需要在所有测试单元执行之前执行一次前置条件，并在所有测试单元执行之后执行一次后置条件，
     #   则需要编写 precondition_class()方法 和 postcondition_class()方法
   ```

3. 日志输出结果

   ```text
   2026-05-04 15:46:53,872 |  TEST_CASE | TEST_CASE_EXAMPLE_003
   ======================================================================
   2026-05-04 15:46:53,872 |  TEST_UNIT | unit_001
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,872 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,873 |       INFO | 这是第 1 个测试单元
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,873 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,873 |       PASS | unit_001 OK (0.001015)s
   ======================================================================
   2026-05-04 15:46:53,873 |  TEST_UNIT | unit_002
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,873 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,874 |       INFO | 这是第 2 个测试单元
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,874 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,874 |       PASS | unit_002 OK (0.001014)s
   ======================================================================
   2026-05-04 15:46:53,874 |  TEST_UNIT | unit_003
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,874 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |       INFO | 这是第 3 个测试单元
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |       PASS | unit_003 OK (0.000507)s
   ```

### 断言

utest.TestCase内可使用unittest的断言方法

1. 示例代码

   ```python
   from utest import TestCase

   class TEST_CASE_EXAMPLE_004(TestCase):
   
     # 例:

     def unit_001(self):
       # 编写第 1 个断言
       self.info('第 1 个断言')
       self.assertTrue(True, '断言 1')
       ...

     def unit_002(self):
       # 编写第 2 个断言
       self.info('第 2 个断言')
       self.assertTrue(False, '断言 2')
       ...
   ```

2. 日志输出结果

   ```text
   2026-05-04 15:46:53,875 |  TEST_CASE | TEST_CASE_EXAMPLE_004
   ======================================================================
   2026-05-04 15:46:53,875 |  TEST_UNIT | unit_001
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |       INFO | 第 1 个断言
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,875 |       PASS | unit_001 OK (0.000000)s
   ======================================================================
   2026-05-04 15:46:53,876 |  TEST_UNIT | unit_002
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,876 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,876 |       INFO | 第 2 个断言
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,876 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,876 |       FAIL | unit_002 FAIL (0.000503)s

   ======================================================================
   FAIL [0.000503s]: example_case.TEST_CASE_EXAMPLE_004.unit_002
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "D:\Users\LuxAEterna\Documents\PycharmProjects\hannto\utest\example_case.py", line 127, in unit_002
       self.assertTrue(False, '断言 2')
     File "E:\python\Lib\unittest\case.py", line 715, in assertTrue
       raise self.failureException(msg)
   AssertionError: False is not true : 断言 2
   ```

### 编写动作 (Action)

Action类内，可使用utest.TestCase的日志方法、断言方法

1. 导入Action类

   ```python
   # 导入Action类
   from utest import Action
   ```

2. 编写一个动作类，并实例化它

   ```python
   from utest import Action

   # 编写一个动作类
   class Test_Action(Action):

     # 编写一个动作方法
     def action_001(self):

       # 1. 编写一些日志
       self.info('这是一个Action类内的日志')

       # 2. 编写一些断言
       self.fail('这是一个Action类内的断言')

       ...

     ...

   # 实例化 Action类
   test_action = Test_Action()
   ```

3. 在测试用例内使用Action实例的方法
   ```python
   from utest import TestCase

   # 导入action实例
   from ... import test_action

   class TEST_CASE_EXAMPLE_005(TestCase):
     def testcase(self):
       # 例:
       # - 在测试用例内使用 Action实例 的方法
       test_action.action_001()
   
       ...
   ```

4. 日志输出结果

   ```text
   2026-05-04 15:46:53,877 |  TEST_CASE | TEST_CASE_EXAMPLE_005
   ======================================================================
   2026-05-04 15:46:53,877 |  TEST_UNIT | testcase
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,877 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,877 |       INFO | 这是一个Action类内的日志
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,878 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 15:46:53,878 |       FAIL | testcase FAIL (0.001022)s
   
   ======================================================================
   FAIL [0.001022s]: example_case.TEST_CASE_EXAMPLE_005.testcase
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "D:\Users\LuxAEterna\Documents\PycharmProjects\hannto\utest\example_case.py", line 159, in testcase
       test_action.action_001()
     File "D:\Users\LuxAEterna\Documents\PycharmProjects\hannto\utest\example_case.py", line 145, in action_001
       self.fail('这是一个Action类内的断言')
     File "D:\Users\LuxAEterna\Documents\PycharmProjects\hannto\utest\utest\core\action.py", line 121, in fail
       self._get_case_instance().fail(msg=msg)
     File "E:\python\Lib\unittest\case.py", line 703, in fail
       raise self.failureException(msg)
   AssertionError: 这是一个Action类内的断言
   ```

### 保存文件

通过utest.saving_path()方法获取当前保存目录

1. 示例代码

   ```python
   from utest import TestCase
   from utest import variable
   
   class TEST_CASE_EXAMPLE_006(TestCase):
     def testcase(self):
       self.info(f'内容保存路径: {variable.saving_path}')
     ...
   ```

2. 日志输出结果

   ```text
   2026-05-04 23:33:21,977 |  TEST_CASE | TEST_CASE_EXAMPLE_006
   ======================================================================
   2026-05-04 23:33:21,977 |  TEST_UNIT | testcase
   ----------------------------------------------------------------------
   2026-05-04 23:33:21,977 |    PRECOND | 前置条件:
   ----------------------------------------------------------------------
   2026-05-04 23:33:21,977 |       INFO | 内容保存路径: ./reports/测试报告_2026-05-04_23-33-21\example_case.TEST_CASE_EXAMPLE_006
   ----------------------------------------------------------------------
   2026-05-04 23:33:21,977 |   POSTCOND | 后置条件:
   ----------------------------------------------------------------------
   2026-05-04 23:33:21,977 |       PASS | testcase OK (0.000000)s
   ```

### 执行测试

在main模块内导入HTMLTestExecutor，加载模块或测试，并执行

1. 示例代码

   ```python
   if __name__ == '__main__':
   
     # 1. 导入HTMLTestExecutor
     from utest import HTMLTestExecutor
   
     # 2. 实例化HTMLTestExecutor
     executor = HTMLTestExecutor()
   
     # 3. 从模块加载用例
     import sys
     test_module = sys.modules[__name__] # 导入自身模块
     executor.load(test_module)          # 从模块加载用例
   
     # 4. 执行测试用例
     executor.run()
   ```

