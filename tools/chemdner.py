import io

class FormatError(Exception):
    pass

class Annotation(object):
    def __init__(self, docid, tiab, start, end, text, type_):
        self.docid = docid
        self.tiab = tiab
        self.start = start
        self.end = end
        self.text = text
        self.type = type_

    def verify(self, text):
        if text[self.start:self.end] != self.text:
            raise FormatError(
                'text mismatch: annotation "%s", document "%s"' %
                (self.text, text[self.start:self.end]))

    def to_standoff(self, idx):
        """Return list of annotation strings in the .ann standoff format."""
        anns = []
        anns.append(u'T%d\tChemical %d %d\t%s' %
                    (idx, self.start, self.end, self.text))
        # TODO: add Attribute for type
        return anns

class Document(object):
    def __init__(self, id_, title, abstract, annotations=None):
        if annotations is None:
            annotations = []
        self.id = id_
        self.title = title
        self.abstract = abstract
        self.annotations = annotations

    @property
    def text(self):
        return self.title + '\n' + self.abstract

    def add_annotation(self, a):
        # Annotations for the document abstract have offsets beginning
        # at zero, but output requires continuous offsets for title and
        # abstract. Adjust here.
        if a.tiab == 'A':
            a.start += len(self.title) + 1    # +1 for newline
            a.end += len(self.title) + 1
        self.annotations.append(a)
            
    def verify_annotations(self):
        for a in self.annotations:
            a.verify(self.text)

    def to_standoff(self):
        """Return list of annotation strings in the .ann standoff format."""
        anns = []
        for idx, a in enumerate(self.annotations, start=1):
            anns.extend(a.to_standoff(idx))
        return anns
        
def read_annotations(flo):
    """Read CHEMDNER annotations from file-like object, return list of
    Annotation objects.
    
    The format consists of lines with TAB-separated fields

        DOCID TIAB START END TEXT TYPE

    where DOCID id the ID of the document, TIAB is "T" or "A"
    identifying if the annotation is in the title or abstract, START
    and END are the span of the annotation in the document, TEXT is
    the annotated text and TYPE identifies chemical entity mention
    types such as "TRIVIAL" or "SYSTEMATIC".
    """
    annotations = []
    for ln, line in enumerate(flo, start=1):
        line = line.rstrip('\n')
        fields = line.split('\t')
        if len(fields) != 6:
            raise FormatError('expected 6 fields, got %d: %s' %
                              (len(fields), line))
        docid, tiab, start, end, text, type_ = fields
        try:
            start = int(start)
            end = int(end)
        except:
            raise FormatError('Failed to parse line %d: %s' % (ln, line))
        if len(text) != end-start:
            raise FormatError('Text "%s" length %d, end-start (%d-%d) is %s' %
                              (text, len(text), end, start, end-start))
        annotations.append(Annotation(docid, tiab, start, end, text, type_))
    return annotations

def read_documents(flo):
    """Read CHEMDNER document texts from file-like object, return list of
    Document objects.

    The format has one document per line with TAB-separated fields

        DOCID TITLE ABSTRACT

    where DOCID is the ID of the document and TITLE and ABSTRACT the
    texts of its title and abstract.
    """
    documents = []
    for line in flo:
        fields = line.rstrip('\n').split('\t')
        if len(fields) != 3:
            raise FormatError()
        docid, title, abstract = fields
        documents.append(Document(docid, title, abstract))
    return documents

def load_annotations(fn):
    with io.open(fn, encoding='utf-8') as f:
        return read_annotations(f)

def load_documents(fn):
    with io.open(fn, encoding='utf-8') as f:
        return read_documents(f)
        
def load_chemdner(txtfn, annfn):
    """Read CHEMDNER corpus data from given document text and annotation
    files, return list of Document objects.
    """
    documents = load_documents(txtfn)
    annotations = load_annotations(annfn)
    doc_by_id = { d.id: d for d in documents}
    for a in annotations:
        doc_by_id[a.docid].add_annotation(a)
    for d in documents:
        d.verify_annotations()
    return documents
