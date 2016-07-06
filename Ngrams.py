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
            self.words = re.findall("(?<=[A-Za-z]\s)[A-Za-z']+|[.!?]", x)         
            self.startWords = [x.split()[0]]
            self.startWords += re.findall("(?<=[.?!]\s)[A-Z][a-z']+|(?<=[\n])[A-Z][a-z']+", x)
            
            

    def grams(self):
        for i in range(len(self.words) - (self.N-1)):
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
        sentence = list(random.choice(list(self.db.keys())))
        while True:
            state = tuple(sentence[-(self.N-1):])
            next_word = random.choice(self.db[state])
            if re.match("[.!?]", next_word):
                return " ".join(sentence)+ next_word
            sentence.append(next_word)
    
    
ngram1 = Ngram("test.txt")

print("startWords", ngram1.startWords)
print("words",ngram1.words)

#print(ngram1.db)

#print(ngram1.makeSentence())


