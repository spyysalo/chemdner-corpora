#!/usr/bin/env python

import sys
import io

from os import path

from chemdner import load_chemdner

def main(argv):
    if len(argv) != 4:
        print >> sys.stderr, 'Usage: chemdner2ann TXTFILE ANNFILE OUTDIR'
        return 1
    txtfn, annfn, outdir = argv[1:]

    if not path.isdir(outdir):
        print >> sys.stderr, '%s is not a directory' % outdir
        return 1

    documents = load_chemdner(txtfn, annfn)

    for d in documents:
        txtout = path.join(outdir, d.id+'.txt')
        with io.open(txtout, 'wt', encoding='utf-8') as out:
            out.write(d.text)
        annout = path.join(outdir, d.id+'.ann')
        with io.open(annout, 'wt', encoding='utf-8') as out:
            out.write(u'\n'.join(d.to_standoff()))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
