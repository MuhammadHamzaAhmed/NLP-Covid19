import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
import re
import csv


class Preprocessing:

    def __init__(self, data):
        self.__data = data
        self.__wordToken = None
        self.__sentToken = None
        self.__clean = None
        self.__stopwords = None
        self.__stem = None
        self.__lemmatize = None

    def wordToken(self, data):
        self.__wordToken = [word_tokenize(word) for word in data]

    def sentToken(self, data):
        self.__sentToken = [sent_tokenize(sen) for sen in data]

    def cleaning(self, data):
        self.__clean = []
        for words in data:
            clean = []
            for word in words:
                res = re.sub(r'[^\w\s]', "", word)
                text = re.sub('[0-9\n]', '', res)
                if text != "" and not re.findall("[^\u0000-\u05C0\u2100-\u214F]+", text):
                    clean.append(res)
            self.__clean.append(clean)

    def stopWordRemoval(self, data):
        self.__stopwords = []
        for words in data:
            self.__stopwords.append([word for word in words if word not in stopwords.words('english')])

    def stemming(self, data):
        port = SnowballStemmer("english")
        self.__stem = []
        for words in data:
            self.__stem.append([port.stem(word) for word in words])

    def lemmatize(self, data):
        net = WordNetLemmatizer()
        self.__lemmatize = []
        for words in data:
            self.__lemmatize.append([net.lemmatize(word) for word in words])

    def joinedList(self, data):
        self.__data = []
        for sent in data:
            self.__data.append(' '.join(sent))

    @property
    def data(self):
        return self.__data

    @property
    def word_Token(self):
        return self.__wordToken

    @property
    def sent_Token(self):
        return self.__wordToken

    @property
    def clean_Data(self):
        return self.__clean

    @property
    def stop_word_removed(self):
        return self.__stopwords

    @property
    def stem(self):
        return self.__stem

    @property
    def lemmatize_data(self):
        return self.__lemmatize


class Analysis:

    def __init__(self, processed):
        self.__processed = processed
        self.__begOfWord = None
        self.__nGram = None
        self.__word2vee = None
        self.__glove = None
        self.__tfidf = None
        self.__vsm = None
        self.__unique = None
        self.__count = None
        self.__termFrequency = None
        self.__idf = None
        self.__query = None
        self.__cosine = None

    @property
    def data(self):
        return self.__processed

    @property
    def begOfWord(self):
        return self.__begOfWord

    @property
    def nGram(self):
        return self.__nGram

    @property
    def word2vee(self):
        return self.__word2vee

    @property
    def glove(self):
        return self.__glove

    @property
    def tfidf(self):
        return self.__tfidf

    @property
    def vsm(self):
        return self.__vsm

    @property
    def unique(self):
        return self.__unique

    @property
    def count(self):
        return self.__count

    @property
    def termFrequency(self):
        return self.__termFrequency

    @property
    def idf(self):
        return self.__idf

    @property
    def query(self):
        return self.__query

    @property
    def cosine(self):
        return self.__query

    def compute_begOfWord(self, data):
        self.__begOfWord = []
        for word in data:
            self.__begOfWord.append(word.split(' '))

    def compute_nGram(self, data, range_):
        countVec = CountVectorizer(ngram_range=range_, stop_words='english')
        self.__nGram = countVec.fit_transform(data)

    def compute_tfidf_ngram(self, data, range_):
        tf_idf_vec = TfidfVectorizer(use_idf=True,
                                     smooth_idf=False,
                                     ngram_range=range_, stop_words='english')
        self.__tfidf = tf_idf_vec.fit_transform(data)

    def compute_Unique(self, data):
        unique = []
        for words in data:
            for word in words:
                if word not in unique:
                    unique.append(word)
        self.__unique = set(unique)

    def countWordEachDoc(self, begOfWord, uniqueWords):
        self.__count = []
        for doc in begOfWord:
            numOfWords = dict.fromkeys(uniqueWords, 0)
            for word in doc:
                numOfWords[word] += 1
            self.__count.append(numOfWords)

    def computeTermFrequency(self, count, begOfWord):
        self.__termFrequency = []
        for i in range(len(begOfWord)):
            self.__termFrequency.append(self._computeTF(count[i], begOfWord[i]))

    def comupteIDF(self, documents):
        N = len(documents)
        self.__idf = dict.fromkeys(documents[0].keys(), 0)
        for document in documents:
            for word, val in document.items():
                if val > 0:
                    self.__idf[word] += 1
        for word, val in self.idf.items():
            self.__idf[word] = math.log(N / float(val))

    def computrTFIDF_BegOfWord(self, tf, idf):
        self.__tfidf = []
        for begOfWord in tf:
            self.__tfidf.append(self._computeTF(begOfWord, idf))

    def saveCSV(self, name):
        with open(name, 'w') as f:
            header = ['term', 'IDF']
            for i in range(len(self.__begOfWord)):
                header.append('D'+str(i))
            writer = csv.writer(f)
            writer.writerow(header)
            for val in self.__unique:
                row = [val, self.__idf.get(val)]
                for beg in self.__tfidf:
                    row.append(beg.get(val))
                writer.writerow(row)

    def _computeTF(self, wordDict, bagOfWords):
        tfDict = {}
        bagOfWordsCount = len(bagOfWords)
        for word, count in wordDict.items():
            tfDict[word] = count / float(bagOfWordsCount)
        return tfDict

    def _computeTFID(self, tfBagOfWords, idfs):
        tfidf = {}
        for word, val in tfBagOfWords.items():
            tfidf[word] = val * idfs[word]
        return tfidf

    def countQuery(self, query):
        self.__query = []
        i = 0
        for val in self.__unique:
            self.__query.append(query.count(val) * self.__idf.get(val))
            i += 1

    def cosineSimilarty(self, tfidf, query):
        tfidf = np.array(tfidf)
        query = np.array(query)
        magQuery = np.linalg.norm(query)
        dot = []
        magDoc = []
        for doc in tfidf:
            val = doc.values()
            val_list = list(val)
            dot.append(np.dot(query, val_list))
            magDoc.append(np.linalg.norm(val_list))

        for i in range(len(magDoc)):
            self.__cosine = dot[i]/(magQuery*magDoc[i])

    def displayRanked(self, data, cosine):
        r1 = r2 = r3 = -1
        for i in range(len(cosine)):
            if r1 < cosine[i]:
                r1 = i
            elif r2 < cosine[i]:
                r2 = i
            elif r3 < cosine[i]:
                r3 = i
        print('Rank 1:\n', data[r1], '\nRank 2:\n', data[r2])
        print('Rank 3:\n', data[r3])
