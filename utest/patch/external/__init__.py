__all__ = ['patch']

from utest.patch.external.html_testrunner_patch import \
  ResultPatch as HtmlTestRunnerResultPatch, \
  RunnerPatch as HtmlTestRunnerRunnerPatch

def patch():
  # 修补HtmlTestRunner
  HtmlTestRunnerRunnerPatch()()

  # 修补HtmlTestResult
  HtmlTestRunnerResultPatch()()

