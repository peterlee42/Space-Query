import nltk
import os
import string
from math import log

nltk.download('stopwords')
nltk.download('punkt')


def answerQuery(query, dataFolder="Data", FILE_MATCH=1, SENT_MATCH=1):
    """ Given 'dataFolder' (contains files with information about space topics),
    'query' (the question the user has asked), 'FILE_MATCH' (the number of files
    to find sentences from), and 'SENT_MATCH' (the number of sentences used to
    answer the query) """

    # Calculate IDF values across files
    fileDict = readFiles(dataFolder)
    docsMap = {
        filename: tokenize(fileDict[filename])
        for filename in fileDict
    }
    query = set(tokenize(query))

    # Extract sentences from top files according to TF-IDF
    filenames = topFiles(query, docsMap, computeIDFS(docsMap), FILE_MATCH)
    sentences = {}
    for filename in filenames:
        for passage in fileDict[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Determine top sentence matches
    return topSentences(query, sentences, computeIDFS(sentences), SENT_MATCH)


def readFiles(dir):
    """ Returns a map of the filename to the contents of the file for
    every file in the given directory dir. """
    fileDict = {}
    for filename in os.listdir(dir):  # loop though all files
        with open(os.path.join(dir, filename), encoding="utf-8") as fString:
            fileDict[filename] = fString.read()
    return fileDict


def tokenize(doc):
    """ Given a document(as a string), return an ordered list of its words. Coverts
    all words to lowercase and removes any punctuation or English stopwords. """

    # set up: tokenize the document in order to iterate through words
    word_document = nltk.tokenize.word_tokenize(doc.lower())
    punct = string.punctuation
    stop_words = nltk.corpus.stopwords.words('english')

    words = []  # finalize the list of words
    for word in word_document:
        # check to see if the word has punctuation or is a stop word
        if word not in punct and word not in stop_words:
            words.append(word)

    return words


def computeIDFS(docsMap):
    """ Given a map of file names to lists of words(docsMap),
    return a dictionary that maps every word to its IDF value. """

    num_docs = len(docsMap)
    occurrence = {}

    for doc in docsMap:  # loop though every file
        for word in set(docsMap[doc]):
            if word in occurrence.keys():
                occurrence[word] += 1
            else:
                occurrence[word] = 1

    IDFS = {}  # find IDF value of words
    for word in occurrence:
        IDFS[word] = log((num_docs/occurrence[word]))

    return IDFS


def topFiles(query, docsMap, IDFS, n):
    """ Given a 'query' (a set of words), 'docsMap' (a dictionary mapping
    names of files to a list of their words), and 'IDFS' (a dictionary
    mapping words to their IDF values), return a list of the filenames of
    the 'n' top files that match the query, ranked according to tf-idf. """
    fileIDFS = {}
    for doc in docsMap:
        fileIDFS[doc] = 0
        for word in query:
            words = docsMap[doc]
            tf = words.count(word)
            if word in IDFS:
                idf = IDFS[word]
                fileIDFS[doc] += idf * tf
    rank = sorted([doc for doc in docsMap.keys()],
                  key=lambda x: fileIDFS[x], reverse=True)
    return rank[:n]  # the top n files


def topSentences(query, sentences, IDFS, n):
    """ Given a 'query' (a set of words), 'sentences' (a dictionary mapping
    sentences to a list of their words), and 'IDFS' (a dictionary mapping words
    to their IDF values), return a list of the 'n' top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density. """
    sentTraits = {}  # map sentences to a list: (total idf, # matches or qtd)
    for sentence in sentences:
        sentTraits[sentence] = [0, 0]
        length = len(sentences[sentence])
        for word in query:  # determine the total idf an matches in each sentence
            # if the query word exists in sentence
            if word in sentences[sentence]:
                sentTraits[sentence][0] += IDFS[word]
                sentTraits[sentence][1] += sentences[sentence].count(word)
        sentTraits[sentence][1] = float(sentTraits[sentence][1] / length)
    sorted_sentences = sorted(sentTraits.keys(), key=lambda sentence: (
        sentTraits[sentence][0], sentTraits[sentence][1]), reverse=True)
    return sorted_sentences[:n]  # return the top n sentences


if __name__ == "__main__":
    print(answerQuery(input("Enter a query: "))[0])
