# chemdner-corpora

Work related to the BioCreative CHEMDNER corpora 

## Quickstart

Download, unpack and convert to `.ann` standoff format

```
wget https://biocreative.bioinformatics.udel.edu/media/store/files/2014/chemdner_corpus.tar.gz
tar xzf chemdner_corpus.tar.gz
./tools/chemdner2ann.sh chemdner_corpus/ chemdner_standoff
```

Convert to CoNLL format (NOTE: does not preserve original annotation
offsets that do not match token boundaries, e.g. "Ser" -> "Ser421")

```
git clone https://github.com/spyysalo/standoff2conll
mkdir conll
for s in train devel test; do
    python3 standoff2conll/standoff2conll.py chemdner_standoff/$s > conll/$s.tsv
done
```
