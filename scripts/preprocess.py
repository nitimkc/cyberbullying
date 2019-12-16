import os
import nltk
import re
import pickle
from nltk import pos_tag, sent_tokenize, wordpunct_tokenize

class Preprocessor(object):
	"""
	Wraps a TweetCorspusReader and manages the stateful tokenization
	and part of speech tagging into a directory that is stored in a
	format that can be read by PickedCorpusReader. This format is more
	compact and necessarily removed a variety of fields from the document
	that are stored in JSON representation dumped from original data. This
	format however is more easily accessed for common parsing activity.
	"""

	def __init__(self, corpus, target=None, **kwargs):
		"""
        The corpus is the `JSONCorpusReader` to preprocess and pickle. The 
		target is the directory on disk to output the pickled corpus to.
        """
		self.corpus = corpus
		self.target = target

	def fileids(self, fileids=None):
		"""
        Helper function access the fileids of the corpus
        """
		return self.corpus.fileids()

	def abspath(self, fileid):
		"""
        Returns the absolute path to the target fileid from the corpus fileid.
        """
		parent = os.path.relpath(
			os.path.dirname(self.corpus.abspath(fileid)), self.corpus.root
		)

		# compute the name parts to reconstruct
		basename = os.path.basename(fileid)
		name, ext = os.path.splitext(basename)

		# create the pickle file extension
		basename = name + '.pickle'

		# return the path to the file relative to the target
		return os.path.normpath(os.path.join(self.target, parent, basename))


	def tokenize(self, fileid):
		"""
		:return: the given file(s) as a list of the text content of Tweets as
        as a list of words, screenanames, hashtags, URLs and punctuation symbols.

        :rtype: list(list(str))
		"""
		tweets = list(self.corpus.tokenized(fileids=fileid))
		return [ pos_tag(token) for token in tweets
		]


	def process_tweet(self, fileid):
		"""
		### PREPROCESS Tweets    
		###   steps:
		###     2. lowercase all characters ('Thanks' == 'thanks')
		###     3. remove hashtags ('#love' == 'love')
		###     4. remove multiple white spaces ('       ' == ' ')
		###     5. remove punctuation ('Hey!!!!!' == 'Hey')
		###     6. remove URLs ('https:twit.co...' == 'URL')
		###     7. if more than 3 consonants in sequence, reduce to 2 ('yeaaaaaaaah' == 'yeaah')
		"""
		tweets = self.tokenize(fileid)

		emoji_pattern = re.compile("["
			u"\U0001F600-\U0001F64F"  # emoticons
         	u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         	u"\U0001F680-\U0001F6FF"  # transport & map symbols
         	u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         	u"\U00002702-\U000027B0"
         	u"\U000024C2-\U0001F251"
         	"]+", flags=re.UNICODE)

		mod_tweets = []
		for tweet in tweets:
			mod_tweet=[]
			for (token, tag) in tweet:
				if len(token) >= 3:
					token = re.sub(r'(.)\1+', r'\1\1', token)
					token = token.lower()
					if '@' in token:
						token = '@user'
					elif '#' in token:
						token = token[1:]
					elif ('http' or 'https') in token:
						token = 'UR'
					elif token == 'luv':
						token = 'love'
					else:
						pass
					mod_tweet.append((token,tag))
			mod_tweets.append(mod_tweet)
		return mod_tweets

	def process(self, fileid):

		"""
		"""
		# compute the outpath to write the file to
		target = self.abspath(fileid)
		parent = os.path.dirname(target)

		# make sure the directory exists
		if not os.path.exists(parent):
			os.makedirs(parent)

		# make sure that the parent is a directory and not a file
		if not os.path.isdir(parent):
			raise ValueError(
				'Please supply a directory to write preprocessed data to.'
			)
		
		# create a data structure for the pickle
		document = self.process_tweet(fileid)

		# open and serialize the pickle to disk
		with open(target, 'wb') as f:
			pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)
		
		# Clean up the document
		del document

		# return the target fileid
		return target
		
	def transform(self, fileids=None):
		"""
		Transform the wrapped corpus, writing out the segmented, tokenized, 
		and part of speech tagged corpus as a pickle to the target directory.
		This method will also directly copy files that are in the corpus.root 
		directory that are not matched by the corpus.fileids()
		"""
		# Make the target directory if it doesn't already exist
		if not os.path.exists(self.target):
			os.makedirs(self.target)

        # Resolve the fileids to start processing and return the list of 
        # target file ids to pass to downstream transformers. 
		return [
            self.process(fileid)
            for fileid in self.fileids(fileids)
        ]	
		

def process_tweet(tweets):
	"""
	### PREPROCESS Tweets    
	###   steps:
	###     2. lowercase all characters ('Thanks' == 'thanks')
	###     3. remove hashtags ('#love' == 'love')
	###     4. remove multiple white spaces ('       ' == ' ')
	###     5. remove punctuation ('Hey!!!!!' == 'Hey')
	###     6. remove URLs ('https:twit.co...' == 'URL')
	###     7. if more than 3 consonants in sequence, reduce to 2 ('yeaaaaaaaah' == 'yeaah')
	"""
	import re
	mod_tweets = []
	for tweet in tweets:
		mod_tweet=[]
		for (token, tag) in tweet:
			if len(token) >= 0:
				token = re.sub(r'(.)\1+', r'\1\1', token)
				token = token.lower()
				if '#' in token:
					token = token[1:]
				elif ('http' or 'https') in token:
					token = 'UR'
				elif token == 'luv':
					token = 'love'
				else:
					pass
				mod_tweet.append((token,tag))
		mod_tweets.append(mod_tweet)
	return mod_tweets


