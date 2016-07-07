import random
import re

class Ngram:
    def __init__(self, doc, n=2):
        self.N = n
        self.makeWordList(doc)
        self.makeDB()

    def makeWordList(self,doc):
        with open(doc, 'r') as f:  
            x = f.read()
            self.words = re.findall("[A-Za-z']+|[.!?]", x)         
            self.makeStartTokens(x)

    def makeStartTokens(self, doc):
        #self.startWords = [tuple(doc.split()[0:(self.N-1)])]
        #self.startWords += re.findall("(?<=[.?!]\s)[A-Z][a-z']+|(?<=[\n])[A-Z][a-z']+", doc)
        words = re.findall("[A-Za-z']+|[.!?]", doc)
        ind = [0] + [i+1 for i, j in enumerate(words) if re.search("[.!?]", j)]
        self.startWords = [tuple(words[i:i+(self.N-1)]) for i in ind]
            
            
    def grams(self):
        for i in range(len(self.words) - (self.N -1)):
            chunk = self.words[i:(i+self.N)]
            yield tuple(chunk[:-1]), chunk[-1]

    def makeDB(self):
        self.db = {}
        for k,v in self.grams():
            if k in self.db.keys():
                self.db[k].append(v)
            else:
                self.db[k] = [v]

    def makeSentence(self):
        start_token = random.choice(self.startWords)
        print(start_token)
        sentence = [w for w in start_token]
        print(sentence)
        state = sentence[-(self.N-1):][0]
        print(state)
        while True:
            next_word = random.choice(self.db[state])
            if re.match("[.!?]", next_word):
                print(sentence)
                return " ".join(sentence)+ next_word
            sentence.append(next_word)
            state = tuple(sentence[-(self.N-1):])
    
#ngram1 = Ngram("test.txt")

#print("startWords", ngram1.startWords)
#print("words",ngram1.words)

#print(ngram1.db)

#print(ngram1.makeSentence())

if __name__ == "__main__":
  n = Ngram("test.txt")
  #print(n.db)
  #print(n.words)
  #print(set([tuple([x]) for x in n.words]) - set(n.db.keys()))
  #print(n.startWords)
  print(n.makeSentence())
  


