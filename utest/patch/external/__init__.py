"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT (https://github.com/TakahashiPancake/uTest/blob/main/LICENSE)

Repository: https://github.com/TakahashiPancake/uTest

"""
__all__ = ['patch']

from utest.patch.external.html_testrunner_patch import \
  ResultPatch as HtmlTestRunnerResultPatch, \
  RunnerPatch as HtmlTestRunnerRunnerPatch

def patch():
  # 修补HtmlTestRunner
  HtmlTestRunnerRunnerPatch()()

  # 修补HtmlTestResult
  HtmlTestRunnerResultPatch()()

