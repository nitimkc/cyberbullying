from nltk import ne_chunk, sent_tokenize
from itertools import groupby
from nltk.corpus import wordnet as wn
from nltk.chunk import tree2conlltags
from nltk.probability import FreqDist
from nltk.chunk.regexp import RegexpParser
from unicodedata import category as unicat
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag

GRAMMAR = r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'
GOODTAGS = frozenset(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])
GOODLABELS = frozenset(['PERSON', 'ORGANIZATION', 'FACILITY', 'GPE', 'GSP'])

grammar = GRAMMAR
chunker = RegexpParser(grammar)
tweet_tokenizer = TweetTokenizer()
labels = GOODLABELS

def normalize(sent):
    """
    Removes punctuation from a tokenized/tagged sentence and
    lowercases words.
    """
    sent = tweet_tokenizer.tokenize(sent)
    sent = [x for x in sent if not 'http' in x]
    is_punct = lambda word: all(unicat(char).startswith('P') for char in word)
    sent = filter(lambda t: not is_punct(t[0]), sent)
#     sent = map(lambda t: (t[0].lower(), t[1]), sent)
    sent = map(lambda t: t.lower(), sent)
    return list(sent)

# works on sentence tokenized documents.
def extract_keyphrases(tweets):
    """
    For a document, parse sentences using our chunker created by
    our grammar, converting the parse tree into a tagged sequence.
    Yields extracted phrases.
    """
    key_phrases = []
    for atweet in test:
        tw_phrases = []
        for sent in atweet:
            sent = pos_tag(normalize(sent))
            if not sent: continue
            chunks = tree2conlltags(chunker.parse(sent))
            phrases = [
                " ".join(word for word, pos, chunk in group).lower()
                for key, group in groupby(
                    chunks, lambda term: term[-1] != 'O' # O = outside of the keyphrase
                ) if key
            ]
            tw_phrases.append(phrases)
            tw_phrases = [x for x in tw_phrases if x] #[item for sublist in tw_phrase for item in sublist]
        key_phrases.append([item for sublist in tw_phrases for item in sublist])
    return key_phrases


def get_entities(tweets):
    entities = []
    for atweet in tweets:
        for sent in atweet:
            pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
            sent = list(pos_tagger.tag(normalize(sent)))
#             sent = pos_tag(normalize(sent))
            trees = ne_chunk(sent)
            for tree in trees:
                if hasattr(tree, 'label'):
                    if tree.label() in labels:
                        entities.append(
                            ' '.join([child[0].lower() for child in tree])
                            )
    return entities


# run this you have to connect to api
# go to dir - stanford-corenlp-full-2018-02-27
# the two lines below type in terminal as one line
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 
# -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000 & 

from nltk.parse import CoreNLPParser
parser = CoreNLPParser(url='http://localhost:9000')
list(parser.parse(doc)) # for sentence tokenized doc
list(parser.raw_parse(doc)) # for non tokenized docs

# on tokenized list of words
pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
list(pos_tagger.tag(doc))

ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
list(ner_tagger.tag(doc))


from nltk.parse.corenlp import CoreNLPDependencyParser
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
list(dep_parser.parse(doc))

