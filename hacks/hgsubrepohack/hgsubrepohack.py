"""
XXX, this is a BIG hack.

To ensure consistency, mercurial always tries to push all the subrepos
whenever you do a push in the main repo.  This is annoying because it
effectively doubles/triples/etc. the time spent for doing a push, when in the
common case there is nothing to push in the subrepo.

This "extension" solves it by pushing the subrepo only when is "dirty",
i.e. when it does not match current stored state.  Note that in general this
is not 100% safe, because in theory there could be an earlier revision in the
main repo pointing to a not-pushed-yet revision in the subrepo, and in this
case the subrepo would not be pushed. However, I think that this case is
uncommon enough (at least for my workflow) that I don't care.
"""

from mercurial.subrepo import hgsubrepo, subrelpath, _

# XXX this is a hack, it patches the subrepo.hgsubrepo class

original_push = hgsubrepo.push

def hacked_push(self, force):
    if self.dirty() or force:
        return original_push(self, force)
    self._repo.ui.status(_('skipping push of subrepo %s\n') % subrelpath(self))
    return True

hgsubrepo.push = hacked_push
