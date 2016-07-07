import random, re, sys

class Ngram:
    def __init__(self, doc, n=2):
        self.N = n
        self.makeWordList(doc)
        self.makeDB()

    def makeWordList(self,doc):
        # Takes a plaintext doc, returns a list of all words in doc,
        # including final punctuation marks as "words."
        
        with open(doc, 'r') as f:  
            x = f.read()
            self.words = re.findall("[A-Za-z']+|[.!?]", x)         
            self.makeStartTokens(x)

    def makeStartTokens(self, doc):
        # Takes a plaintext doc, returns a list of all sentence-openers

        # Find all words and closing punctuation
        words = re.findall("[A-Za-z']+|[.!?]", doc)
        # Get a list of the indices of all closing punctuation.
        ind = [0] + [i+1 for i, j in enumerate(words) if re.search("[.!?]", j)]
        # Select the word(s) following the closing punctuation
        self.startWords = [tuple(words[i:i+(self.N-1)]) for i in ind]
        #Remove trailing empty tuple, if exists
        if tuple('') in self.startWords:
            self.startWords.remove(tuple(''))
        
            
    def grams(self):
        # Goes through the list of words and generates ngrams in a tuple,
        # with the last element separated
        
        for i in range(len(self.words) - (self.N -1)):
            chunk = self.words[i:(i+self.N)]
            yield tuple(chunk[:-1]), chunk[-1]

    def makeDB(self):
        # Goes through the ngrams and creates a dictionary with tuples
        # as keys, and strings as values.
        
        self.db = {}
        for k,v in self.grams():
            if k in self.db.keys():
                self.db[k].append(v)
            else:
                self.db[k] = [v]

    def makeSentence(self, minLength=3, maxLength=20):
        # Generates a new Markov sentence from the database
        
        # Select the first word(s)
        start_token = random.choice(self.startWords)
        #print('START_TOKEN',start_token)

        # Begin creating the sentence
        sentence = [w for w in start_token]
        #print('SENTENCE', sentence)

        # Initialize the current state (as a tuple)
        state = start_token
        #print('STATE',state)
        
        while True:
            # Pick the next word from the dictionary, with state as key
            next_word = random.choice(self.db[state])
            if re.match("[.!?]", next_word):
                # If a closing punctuation is chosen, end the sentence
                #print(sentence)
                return " ".join(sentence) + next_word
            #sentence.append(next_word)
            if len(sentence) > maxLength:
                # If the max length is reached, add period and end sentence
                #sentence.append(next_word)
                #print(sentence)
                return " ".join(sentence) + '.'
            sentence.append(next_word)
            state = tuple(sentence[-(self.N-1):])


if __name__ == "__main__":
    f = str(sys.argv[1])
    n = Ngram(f)
    #print('WORDS\n',n.words,'\n')
    #print('STARTWORDS\n',n.startWords,'\n')
    #print('DATABASE','\n',n.db,'\n')
    #print(set([tuple([x]) for x in n.words]) - set(n.db.keys()))
    for i in range(0,20):
      print(n.makeSentence(),'\n')
  


