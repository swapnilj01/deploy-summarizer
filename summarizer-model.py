import bs4
import urllib.request as url
import re
#!pip3 install nltk
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')
import string


url_name = input("Enter the URL of the page you want to summarize:\n")


#Parsing the HTML file and storing a list of all paragraph tags in it
web = url.urlopen(url_name)
page = bs4.BeautifulSoup(web,'html.parser')
elements = page.find_all('p')
article = ''
for i in elements:
    article+= (i.text)

#Processing the data to remove irrelavant text
processed = article.replace(r'^\s+|\s+?$','')
processed = processed.replace('\n',' ')
processed = processed.replace("\\",'')
processed = processed.replace('===','')
processed = processed.replace(",",'')
processed = processed.replace('"','')
processed = processed.replace(';','')
processed = processed.replace('\t','')
processed = processed.replace('{','')
processed = processed.replace('}','')
processed = re.sub(r'\[[0-9]*\]','',processed)
processed


#function to clean the sentences
def cleanSentence(sentences):
    counter = 0
    for sentence in sentences:
        count = 0
        for character in sentence:
            if(character == '('):
                count+=1
        if(count>=10):
            sentences.pop(counter)
        counter+=1
    return sentences



dirty_sentences = sent_tokenize(processed)
cleaned = cleanSentence(dirty_sentences)
separator = "."
cleaned_string = separator.join(cleaned)



#counting the frequency of all the tokenized words
frequency = {}
processed1 = cleaned_string.lower()
for word in word_tokenize(processed1):
    if word not in stop_word:
        if word not in frequency.keys():
            frequency[word]=1
        else:
            frequency[word]+=1


#calulating and storing the importance values of the words
max_fre = max(frequency.values())
for word in frequency.keys():
    frequency[word]=(frequency[word]/max_fre)


#calculating the sentence scores
sentence_score = {}
for sent in cleaned:
    for word in word_tokenize(sent):
        if word in frequency.keys():
            if len(sent.split(' '))<30:
                if sent not in sentence_score.keys():
                    sentence_score[sent] = frequency[word]
                else:
                    sentence_score[sent] += frequency[word]


import heapq

print("\nTotal number of sentences in the dictionary={0}\n".format(len(sentence_score)))
number = int(input("Enter the number of sentences you want the summary to contain:\n"))
#storing the summary according to the sentence importances
summary = heapq.nlargest(number,sentence_score,key = sentence_score.get)
summary = ' '.join(summary)
final = "SUMMARY:- \n  " +summary
print("\n===============SUMMARY===============\n")
print("\n")
print(summary)
print("\n\n=====================================\n")
