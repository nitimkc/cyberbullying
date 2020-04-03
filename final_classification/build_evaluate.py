import os
import time
import string
import pickle
<<<<<<< HEAD
import numpy as np
=======


>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
from operator import itemgetter

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
<<<<<<< HEAD
from sklearn.linear_model import LogisticRegressionCV
=======
from sklearn.linear_model import LogisticRegression
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.metrics import classification_report as clsr
from sklearn.metrics import confusion_matrix as cm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split as tts


def timeit(func):
    """
    Simple timing decorator
    """
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        delta  = time.time() - start
        return result, delta
    return wrapper

def identity(words):
    return words

<<<<<<< HEAD
def build_and_evaluate(X, y, n=None, classifier=LogisticRegressionCV, outpath=None, verbose=True, multiclass=False):
=======
def build_and_evaluate(X, y, n=None, classifier=LogisticRegression, outpath=None, verbose=True):
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
    """
    Builds a classifer for the given list of documents and targets in two
    stages: the first does a train/test split and prints a classifier report,
    the second rebuilds the model on the entire corpus and returns it for
    operationalization.
    X: a list or iterable of raw strings, each representing a document.
    y: a list or iterable of labels, which will be label encoded.
    Can specify the classifier to build with: if a class is specified then
    this will build the model with the Scikit-Learn defaults, if an instance
    is given, then it will be used directly in the build pipeline.
    If outpath is given, this function will write the model as a pickle.
    If verbose, this function will print out information to the command line.
    """

    @timeit
    def build(classifier, X, y=None):
        """
        Inner build function that builds a single model.
        """
        if isinstance(classifier, type):
<<<<<<< HEAD
            if multiclass:
                classifier = classifier(cv=10, random_state=0,  max_iter=1000, solver='newton-cg', multi_class="multinomial")
            else:
                classifier = classifier(cv=10, random_state=0,  max_iter=1000)
        
=======
            classifier = classifier(solver='lbfgs', penalty='none')

>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
        model = Pipeline([
            # ('preprocessor', TextNormalizer_lemmatize()),
            ('vectorizer', TfidfVectorizer(
                tokenizer=identity, preprocessor=None, lowercase=False, ngram_range=(1,2))
                ),
            ('classifier', classifier),
        ])

        model.fit(X, y)

        return model

    # Label encode the targets
    labels = LabelEncoder()
    y = labels.fit_transform(y)

    # Begin evaluation
    if n:
<<<<<<< HEAD
        if verbose: print("splitting test and test set by: "+str(n))
        X_train, X_test, y_train, y_test = tts(X, y, test_size=n)
        # X_train, X_test, y_train, y_test = X[:n], X[n:], y[:n], y[n:]
        print(len(X_train), len(X_test))
        from collections import Counter
        print(Counter(y_train))

        model, secs = build(classifier, X_train, y_train)
        model.labels_ = labels
=======
        if verbose: print("Building for evaluation")
        X_train, X_test, y_train, y_test = tts(X, y, test_size=n)
        model, secs = build(classifier, X_train, y_train)
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73

        if verbose: print("Evaluation model fit in {:0.3f} seconds".format(secs))
        y_pred = model.predict(X_test)

        if verbose: print("Classification Report:\n")
        print(clsr(y_test, y_pred, target_names=labels.classes_))
<<<<<<< HEAD
        print(cm(y_test, y_pred))
        print('acc', accuracy_score(y_test, y_pred))
        print('f1', f1_score(y_test, y_pred, average='weighted'))

    else:
        if verbose: print("Building for evaluation with full set")    
        model, secs = build(classifier, X, y)
        model.labels_ = labels
=======
        print(cm(y_test, y_pred, labels=[1,0]))

    else:
        if verbose: print("Building for evaluation")    
        model, secs = build(classifier, X, y)
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73

        if verbose: print("Evaluation model fit in {:0.3f} seconds".format(secs))
        y_pred = model.predict(X)

        if verbose: print("Classification Report:\n")
        print(clsr(y, y_pred, target_names=labels.classes_))
<<<<<<< HEAD
        print(cm(y, y_pred))
        print(accuracy_score(y, y_pred))

    if verbose: print("Evaluation of naive prediction ...")
    y_naive = [0]*len(y_test)
    print(type(y_test))
    print('acc naive', accuracy_score(y_test, y_naive))
=======
        print(cm(y, y_pred, labels=[1,0]))

    if verbose: print("Building complete model and saving ...")
    model, secs = build(classifier, X, y)
    model.labels_ = labels
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73

    if verbose: print("Complete model fit in {:0.3f} seconds".format(secs))

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

        print("Model written out to {}".format(outpath))

    return model


def show_most_informative_features(model, text=None, n=10):
    """
    Accepts a Pipeline with a classifer and a TfidfVectorizer and computes
    the n most informative features of the model. If text is given, then will
    compute the most informative features for classifying that text.
    Note that this function will only work on linear models with coefs_
    """
    # Extract the vectorizer and the classifier from the pipeline
    vectorizer = model.named_steps['vectorizer']
    classifier = model.named_steps['classifier']

    # Check to make sure that we can perform this computation
    if not hasattr(classifier, 'coef_'):
        raise TypeError(
            "Cannot compute most informative features on {} model.".format(
                classifier.__class__.__name__
            )
        )

    if text is not None:
        # Compute the coefficients for the text
        tvec = model.transform([text]).toarray()
    else:
        # Otherwise simply use the coefficients
        tvec = classifier.coef_

    # Zip the feature names with the coefs and sort
    coefs = sorted(
        zip(tvec[0], vectorizer.get_feature_names()),
        key=itemgetter(0), reverse=True
    )

    topn  = zip(coefs[:n], coefs[:-(n+1):-1])

    # Create the output string to return
    output = []

    # If text, add the predicted value to the output.
    if text is not None:
        output.append("\"{}\"".format(text))
        output.append("Classified as: {}".format(model.predict([text])))
        output.append("")

    # Create two columns with most negative and most positive features.
    for (cp, fnp), (cn, fnn) in topn:
        output.append(
            "{:0.4f}{: >15}    {:0.4f}{: >15}".format(cp, fnp, cn, fnn)
        )

    return "\n".join(output)


# ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
# CORPUS = os.path.join(ROOT, 'data/labelled_tweets')
# RESULTS = os.path.join(ROOT, 'results')

# DOC_PATTERN = r'.*\.json' 

# if __name__ == "__main__":
#     PATH = "model.pickle"

#     if not os.path.exists(PATH):
#         # Time to build the model
#         from reader import TweetsCorpusReader
        
#         corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN)

#         X = corpus.docs
#         y = list(corpus.fields('bullying_trace'))

#         model = build_and_evaluate(X,y, outpath=PATH)

#     else:
#         with open(PATH, 'rb') as f:
#             model = pickle.load(f)

#     print(show_most_informative_features(model))