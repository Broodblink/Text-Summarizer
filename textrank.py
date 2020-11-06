import numpy as np
import pandas as pd
import nltk
nltk.download('punkt') # one time execution
nltk.download('stopwords')
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx


class TextRank():
    def __init__(self):
        print("TextRank model created")
        self.stop_words = stopwords.words('english')
        word_emb_path = "./data/glove.6B.100d.txt"
        #'glove.6B.100d.txt'
        self.word_embeddings = {}
        f = open(word_emb_path, encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            self.word_embeddings[word] = coefs
        f.close()

    def remove_stopwords(self,sen):
        sen_new = " ".join([i for i in sen if i not in self.stop_words])
        return sen_new

    def getSummary(self,text):
        df = pd.DataFrame({'article_text':[text]})
        sentences = []
        for s in df['article_text']:
            sentences.append(sent_tokenize(s))
        sentences = [y for x in sentences for y in x] # flatten list
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
        clean_sentences = [s.lower() for s in clean_sentences]
        clean_sentences = [self.remove_stopwords(r.split()) for r in clean_sentences]
        #create vectors for our sentences
        sentence_vectors = []
        for i in clean_sentences:
            if len(i) != 0:
                v = sum([self.word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
            else:
                v = np.zeros((100,))
            sentence_vectors.append(v)
        sim_mat = np.zeros([len(sentences), len(sentences)])
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)

        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        number_sentences = int(len(ranked_sentences)*0.3)
        #print(len(ranked_sentences))
        summary = []
        for i in range(number_sentences):
            summary.append(ranked_sentences[i][1])
            #print(ranked_sentences[i][1])
        return ''.join(summary)

def test():
    #read the data
    model = TextRank()
    PATH = "C:\\Users\\Roman2\\Documents\\PMP\\text_test\\example.txt"
    f = open(PATH,'r')
    text_lines = f.readlines()
    f.close()
    text = [line.split('\n')[0] for line in text_lines]
    text = ''.join(text)
    summary = model.getSummary(text)
    print("SUMMARY " + summary)
if __name__ == "__main__":
    test()
