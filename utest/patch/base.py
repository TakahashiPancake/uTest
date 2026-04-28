from inspect import getmembers as _getmembers


class PatcherBase(object):

  _class_to_patch: type[object] | None = None

  def __call__(self):
    self._patch_()

  def _patch_(self):
    self._patch_start(self._class_to_patch)

  def _patch_start(self, module: type[object]):
    for name, member in _getmembers(self):
      if not name.startswith('__') and not name.startswith('_patch_') \
        and not name == '_class_to_patch':
          setattr(module, name, member)

