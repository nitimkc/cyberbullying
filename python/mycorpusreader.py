from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader import TwitterCorpusReader
import codecs

DOC_PATTERN = r'(?!\.)[\w_\s]+/[\w\s\d\-]+\.json'
CAT_PATTERN = r'([\w_\s]+)/.*'

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/filtered'

class JSONCorpusReader(TwitterCorpusReader, CorpusReader): 
    """
    A corpus reader for raw HTML documents to enable preprocessing.
    """
    
    def __init__(self, root, fileids=DOC_PATTERN, encoding='utf8', **kwargs):
        """
        Initialize the corpus reader. Categorization arguments (``cat_pattern``, ``cat_map``, and ``cat_file``) are passed to the ``CategorizedCorpusReader`` constructor. The remaining arguments are passed to the ``CorpusReader`` constructor.
        """
        # Add the default category pattern if not passed into the class. 
        if not any(key.startswith('cat_') for key in kwargs.keys()):
            kwargs['cat_pattern'] = CAT_PATTERN
        
        # Initialize the NLTK corpus reader objects
        TwitterCorpusReader.__init__(self, kwargs) 
        CorpusReader.__init__(self, root, fileids, encoding)

    def resolve(self, fileids, categories): 
        """
        Returns a list of fileids or categories depending on what is passed
        to each internal corpus reader function. Implemented similarly to
        the NLTK ``CategorizedPlaintextCorpusReader``.
        """
        if fileids is not None and categories is not None:
            raise ValueError("Specify fileids or categories, not both")
        
        if categories is not None:
            return self.fileids(categories)
        return fileids

    def docs(self, fileids=None, categories=None): 
        """
        Returns the complete text of an HTML document, closing the document
        after we are done reading it and yielding it in a memory safe fashion.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)
        
        # Create a generator, loading one document into memory at a time.
        for path, encoding in self.abspaths(fileids, include_encoding=True): 
            with codecs.open(path, 'r', encoding=encoding) as f:
                yield f.read()
 

reader = JSONCorpusReader(PATH)

