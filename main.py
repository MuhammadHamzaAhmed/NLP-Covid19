from cryptography.fernet import Fernet
from TwitterScrapper import TwitterScrapper
from Data_Preprocessing_Analysis import Preprocessing, Analysis
from time import sleep
import pandas as pd

file = open('key', 'r')
key = file.read()
f = Fernet(key)
mailEnc = b'gAAAAABhWs_IZbnUrWTZMjfIyeU_VltSRAidnCtn1N2RnBoDHuP7blFCeumYddW7307mL2kz03xUnz7C7s7G9III-dsYhdls1Q=='
passEnc = b'gAAAAABhWtELH4SUbh4DTQilQYl_byYFSjWFsOSJAWWrIijksszVqNIseK4lrKHmDEWvLjrYpysYFe9hCXqYBjDgChXiKap-qg=='

mail = f.decrypt(mailEnc).decode()
password = f.decrypt(passEnc).decode()
scrapper = TwitterScrapper()

scrapper.setBrowser(TwitterScrapper.SAFARI)
scrapper.open()
scrapper.enterUsername(mail)
scrapper.enterPassword(password)
scrapper.search('#covid_19 lang:en')
scrapper.latest()
i = 0
while i < 50:
    sleep(3)
    scrapper.tweets()
    tweets = scrapper.tweetList
    for tweet in tweets:
        scrapper.get_Tweet_Bunch(tweet)
    scrapper.scroll()
    i += 1
scrapper.saveCSV('Covid_19.csv')
scrapper.exit()

data = pd.read_csv('Covid_19.csv')
data = list(data['Tweets'])

processor = Preprocessing(data)
processor.wordToken(processor.data)
processor.cleaning(processor.word_Token)
processor.lemmatize(processor.clean_Data)
processor.stopWordRemoval(processor.lemmatize_data)
processor.joinedList(processor.stop_word_removed)

analyzer = Analysis(processor.data)
analyzer.compute_begOfWord(analyzer.data)
analyzer.compute_Unique(analyzer.begOfWord)
analyzer.countWordEachDoc(analyzer.begOfWord, analyzer.unique)
analyzer.computeTermFrequency(analyzer.count, analyzer.begOfWord)
analyzer.comupteIDF(analyzer.count)
analyzer.computrTFIDF_BegOfWord(analyzer.termFrequency, analyzer.idf)
analyzer.countQuery('positive vaccine '.split())
analyzer.cosineSimilarty(analyzer.tfidf, analyzer.query)
analyzer.displayRanked(data, analyzer.cosine)
