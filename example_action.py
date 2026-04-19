from utest import Action

class TestAction(Action):
  def action_03(self):
    self.info('test_03_01')
    self.trace('test_03_02')
    self.assertTrue(False)


test_action = TestAction()

