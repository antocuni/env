import sys
import py
import cPickle as pickle
import pipes
from commands import getoutput

MD5 = py.path.local.sysfind('md5sum')
def md5(f):
    cmd = '%s %s' % (MD5, pipes.quote(str(f)))
    out = getoutput(cmd)
    parts = out.split()
    md5hash = parts[0]
    assert len(md5hash) == 32
    return md5hash

class Md5Database(object):

    def __init__(self, root):
        self.root = root
        self.dbfile = root.join('db.pickle')
        if self.dbfile.check(exists=True):
            self.data = pickle.loads(self.dbfile.read())
        else:
            self.data = {}

    def save(self):
        print
        print 'Writing to', self.dbfile
        self.dbfile.write(pickle.dumps(self.data))

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, tb):
        self.save()



def main(root):
    root = py.path.local(root)

    def should_visit(f):
        fname = f.relto(root)
        if fname.startswith('home/'):
            return False
        return True

    allfiles = []
    for f in root.visit(should_visit):
        allfiles.append(f)

    with Md5Database(root) as db:
        N = len(allfiles)
        for i, f in enumerate(allfiles):
            fname = f.relto(root)
            status = '%5d/%5d %6.2f%% %140s' % (i, N, float(i)/N * 100, fname[:140])
            sys.stdout.write('\r')
            sys.stdout.write(status)
            if fname in db.data:
                continue
            if f.check(file=True):
                db.data[fname] = md5(f)

try:
    main(sys.argv[1])
except:
    import pdb;pdb.xpm()

