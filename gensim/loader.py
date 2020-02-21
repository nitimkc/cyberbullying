# # create iterable of train and test sets for CV

from sklearn.model_selection  import KFold

class CorpusLoader(object):

    def __init__(self, reader, folds=None, shuffle=True, label=None, size=None):
        self.reader = reader
        self.folds  = folds
        self.label = label
        self.idx = range(0, size)

        if folds is not None:
            # Generate the KFold cross validation for the loader.
            self.folds = KFold(n_splits=self.folds, shuffle=shuffle)

    @property
    def n_folds(self):
        """
        Returns the number of folds if it exists; 0 otherwise.
        """
        if self.folds is None: 
            return 0
        return self.folds.n_splits

    def index(self, train=False, test=False):

        if self.folds is None:
            # If no fold is specified, return all the fileids.
            return self.idx
        else: 
            if not (test or train) or (test and train):
                raise ValueError(
                    "Please specify either train or test flag"
                )
            idx = list(self.folds.split(self.idx))
            train_idx = [i[0] for i in idx]
            test_idx = [i[1] for i in idx]

            indices = train_idx if train else test_idx
            return indices

    # def documents(self, fold=None, train=False, test=False, idx=None):
    #     tweets = self.reader.process_tweet()
    #     [id for id_idx, idx in enumerate(self.index()) if id_idx in indices]
    #     # if train:
    #     #     docs = [tweet[ind] for ]
    #     if idx is None:
    #         return tweets
    #     for ind in self.index:
    #         tweets =  [tweets[i] for i in folds
    #                     for folds in train_idx]
    #     return  tweets

    def documents(self, fold=None, train=False, test=False):
        for fileid in self.fileids(fold, train, test):
            yield list(self.corpus.docs(fileids=fileid))

    # def labels(self, idx=None):
    #     labels = list(self.reader.fields(self.label))
    #     if idx is None:
    #         return labels
    #     return list(labels[i] for i in idx)

    def labels(self, fold=None, train=False, test=False):
        return [
            self.corpus.categories(fileids=fileid)[0]
            for fileid in self.fileids(fold, train, test)
        ]
    
#     def labels(self, idx=None):
#         labels = list(self.reader.fields(self.label))
#         if idx is None:
#             return labels
#         return list(labels[i] for i in idx)


if __name__ == '__main__':
    from reader import TweetsCorpusReader
    target = 'bullying_trace'
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    loader = CorpusLoader(corpus, folds=None, shuffle=True)

    for fid in loader.fileids(0, test=True):
        print(fid)