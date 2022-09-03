"""Manage names in a scope via context manager."""
__all__ = ['Scope']
import inspect

class Scope(object):
    """Track names in a scope.

    This class is intended to be used in with statements.  Use outside
    with statement is undefined.
    """
    def __init__(self, extras=None, state=None, ignore_=True):
        """Initialize scope.

        extras: extra names to be considered as current.  This would
            generally just be the variable name of the Scope if given.
            These are added to the initial set of names for diffing.
        state: dict from globals() or locals().  Used to find the names
            in the scope.  If not given, obtain from
            inspect.currentframe().f_back
            NOTE: if state is the result of locals(), the methods
            might not work unless locals() is called again beforehand.
            (the locals() dict can be outdated)
        """
        self.ignore_ = ignore_
        self.extras = extras
        self.f_locals = state
        self.pframe = self._starters = None

    def __enter__(self):
        """Begin scope."""
        if self.f_locals is None:
            here = inspect.currentframe()
            if here is None:
                raise Exception(
                    'failed to get current frame and no state given.')
            self.pframe = here.f_back
        else:
            self.pframe = self
        self._starters = set(self.pframe.f_locals)
        extras = self.extras
        if extras is not None:
            if isinstance(extras, str):
                self._starters.add(extras)
            else:
                self._starters.update(extras)
        return self

    def __exit__(self, exctp, exc, tb):
        self.pframe = None

    def update(self):
        """Reupdate start state."""
        self._starters.update(self.pframe.f_locals)

    def diff(self):
        """Return set of new names."""
        locs = self.pframe.f_locals
        ignore_ = self.ignore_
        return set(
            k for k in locs if not (ignore_ and k.startswith('_'))
            ).difference(self._starters)

    def items(self):
        """Generate (name,item), added since creation/last update."""
        locs = self.pframe.f_locals
        ignore_ = self.ignore_
        for k in set(locs).difference(self._starters):
            if not (ignore_ and k.startswith('_')):
                yield k, locs[k]


if __name__ == '__main__':
    def infuncscope(a, b):
        s = Scope()
        with s:
            x = 1
            y = 2
            assert s.diff() == set('xy')
            assert dict(s.items()) == dict(x=1, y=2)
            s.update()
            _ignored = 'krilin'
            assert not s.diff()
    infuncscope(3,4)

    with Scope() as thing:
        assert thing.diff() == set(['thing'])
        thing.update()
        _ignored = 'krilin'
        assert not thing.diff()

    with Scope(ignore_=False) as s:
        _notignored = 'plot'
        assert s.diff() == set(['s', '_notignored'])
        assert dict(s.items()) == dict(s=s, _notignored=_notignored)

    print('pass')
