# # create iterable of train and test sets for CV

# import numpy as np
# from sklearn.model_selection import KFold
# from sklearn.model_selection import train_test_split as tts

# class CorpusLoader(object):

#     def __init__(self, reader, folds=12, shuffle=True, label=None, size=None):
#         self.reader = reader
#         self.folds  = KFold(n_splits=folds, shuffle=shuffle)
#         self.files  = np.asarray(list(self.reader.fields('id')))
#         self.label = label
#         self.idx = range(0,size)


#     def documents(self, idx=None):
#         tweets = self.reader.process_tweet()
#         if idx is None:
#             return tweets
#         return  list(tweets[i] for i in idx)

#     def labels(self, idx=None):
#         labels = list(self.reader.fields(self.label))
#         if idx is None:
#             return labels
#         return list(labels[i] for i in idx)

#     def __iter__(self):
#         i=1
#         for train_index, test_index in self.folds.split(self.idx):
#             print('iter', i)
#             print(len(train_index), len(test_index))
            
#             i = i+1
#             X_train = self.documents(train_index)
#             y_train = self.labels(train_index)
#             X_test = self.documents(test_index)
#             y_test = self.labels(test_index)

#             yield X_train, X_test, y_train, y_test

from sklearn.model_selection  import KFold

class CorpusLoader(object):

    def __init__(self, corpus, folds=None, shuffle=True):
        self.n_docs = len(corpus.fileids())
        self.corpus = corpus
        self.folds  = folds

        if folds is not None:
            # Generate the KFold cross validation for the loader.
            self.folds = KFold(self.n_docs, folds, shuffle)

    @property
    def n_folds(self):
        """
        Returns the number of folds if it exists; 0 otherwise.
        """
        if self.folds is None: return 0
        return self.folds.n_folds

    def fileids(self, fold=None, train=False, test=False):

        if fold is None:
            # If no fold is specified, return all the fileids.
            return self.corpus.fileids()

        # Otherwise, identify the fold specifically and get the train/test idx
        train_idx, test_idx = [split for split in self.folds][fold]

        # Now determine if we're in train or test mode.
        if not (test or train) or (test and train):
            raise ValueError(
                "Please specify either train or test flag"
            )

        # Select only the indices to filter upon.
        indices = train_idx if train else test_idx
        return [
            fileid for doc_idx, fileid in enumerate(self.corpus.fileids())
            if doc_idx in indices
        ]

    def documents(self, fold=None, train=False, test=False):
        for fileid in self.fileids(fold, train, test):
            yield list(self.corpus.docs(fileids=fileid))

    def labels(self, fold=None, train=False, test=False):
        return [
            self.corpus.categories(fileids=fileid)[0]
            for fileid in self.fileids(fold, train, test)
        ]


if __name__ == '__main__':
    from reader import TweetsCorpusReader
    target = 'bullying_trace'
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    loader = CorpusLoader(corpus, folds=None, shuffle=True)

    for fid in loader.fileids(0, test=True):
        print(fid)