from __future__ import nested_scopes

#
#  Point to this file in your $PYTHONSTARTUP environment variable.
#
#  In interactive use of Python, all modules will be automatically
#  imported when you first reference them.  This is done by creating
#  instances of ModuleLoader and putting them into the __main__ scope
#  under the name of all existing modules.
#

def startup():
    import sys

    #
    #  Module auto-loader
    #
    import imp, os, __main__, __builtin__

    def loadmodule(self):
        import __main__
        name = self.__name__
        m = __main__.__dict__.get(name)
        if m is self:
            del __main__.__dict__[name]
        if m is self or m is None:
            #import sys; print >> sys.stderr, "<auto-loading '%s'>" % name
            m = __import__(name, __main__.__dict__, __main__.__dict__, [])
            __main__.__dict__[name] = m
        return m
    
    if sys.version_info < (2,2):

        class ModuleLoader:
            def __init__(self, m):
                self.__dict__['__name__'] = m
            def __repr__(self):
                return '<module %r (auto-load)>' % self.__name__
            def __getattr__(self, attr):
                return getattr(self.__load__(), attr)
            def __setattr__(self, attr, value):
                setattr(self.__load__(), attr, value)
            def __delattr__(self, attr):
                delattr(self.__load__(), attr)
        ModuleLoader.__load__ = loadmodule
        
    else:
        
        class ModuleLoader(type(__main__)):
            __slots__ = []
            def __init__(self, name):
                super(ModuleLoader, self).__init__(name)
                d = super(ModuleLoader, self).__getattribute__('__dict__')
                d['__name__'] = name
            def __repr__(self):
                return '<module %r (auto-load)>' % self.__name__
            def __getattribute__(self, attr):
                if attr == '__name__':
                    d = super(ModuleLoader, self).__getattribute__('__dict__')
                    return d['__name__']
                if attr == '__call__':
                    raise AttributeError
                return getattr(loadmodule(self), attr)
            def __setattr__(self, attr, value):
                setattr(loadmodule(self), attr, value)
            def __delattr__(self, attr):
                delattr(loadmodule(self), attr)

    modules = list(sys.builtin_module_names)
    suff = [ext for ext, mod, typ in imp.get_suffixes()]
    for path in sys.path:
        if path:# path.startswith(sys.prefix):
            try:
                dirlist = os.listdir(path)
            except OSError:
                continue
            for fn in dirlist:
                for suf in suff:
                    if fn.endswith(suf):
                        modules.append(fn[:-len(suf)])
                        break
    d = __main__.__dict__
    d2 = __builtin__.__dict__
    for m in modules:
        if not m.startswith('__') and m not in d and m not in d2:
            d[m] = ModuleLoader(m)

    try:
        old_help = __builtin__.help
    except AttributeError:
        pass
    else:
        def help(*args, **kw):
            if args and isinstance(args[0], ModuleLoader):
                args = (loadmodule(args[0]),) + args[1:]
            return old_help(*args, **kw)
        __builtin__.help = help


    #
    #  Local .pystartup file
    #
    import os, __main__
    
    if os.path.isfile('.pystartup'):
        execfile('.pystartup', __main__.__dict__)


startup()
del startup

try:
    del __file__
except NameError:
    pass

import fancycompleter
fancycompleter.interact(persist_history=True)
