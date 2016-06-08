#!/bin/bash

# Convert BioCreative CHEMDNER corpus annotations to .ann standoff format.

set -e
set -u

# http://stackoverflow.com/a/246128
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 CHEMDNERDIR OUTDIR"
    exit 1
fi

INDIR="$1"
OUTDIR="$2"

if [ ! -d "$INDIR" ]; then
    echo "Not a directory: $INDIR"
    exit 1
fi

for s in "training" "development" "evaluation"; do
    for f in "abstracts" "annotations"; do
	if [ ! -e "$INDIR/$s.$f.txt" ]; then
	    echo "Missing file: $INDIR/$s.$f.txt"
	    exit 1
	fi
    done
done
	    
if [ -d "$OUTDIR" ]; then
    echo "Already exists: $OUTDIR"
    exit 1
fi

mkdir -p "$OUTDIR/"{train,devel,test}

python "$SCRIPTDIR/chemdner2ann.py" "$INDIR/training."{abstracts,annotations}".txt" "$OUTDIR/train"
python "$SCRIPTDIR/chemdner2ann.py" "$INDIR/development."{abstracts,annotations}".txt" "$OUTDIR/devel"
python "$SCRIPTDIR/chemdner2ann.py" "$INDIR/evaluation."{abstracts,annotations}".txt" "$OUTDIR/test"

for s in "train" "devel" "test"; do
    echo "Converted" $(ls "$OUTDIR/$s/"*.txt | wc -l) "files to $OUTDIR/$s" >&2
done
