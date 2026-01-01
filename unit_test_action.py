from utest import Action

class TestAction(Action):
  def action(self):
    self.info('123')
    self.trace('456')
    self.assertTrue(False)

if __name__ == '__main__':
  test_action = TestAction()
  test_action.action()
