from inspect import getmembers as _getmembers


class PatcherBase(object):

  _patched_class: type[object] | None = None

  def __call__(self):
    self._patch()

  def _patch(self):
    self._patch_start(self._patched_class)

  def _patch_start(self, module: type[object]):
    for name, member in _getmembers(self):
      if not name.startswith('__') and not name.startswith('_patch_') \
        and not name.startswith('_patched_'):
          setattr(module, name, member)

