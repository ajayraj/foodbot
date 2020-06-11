import json
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from collections import Counter
import pickle

class NaiveBayes():
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.RecipeData = []
        # Frequency of each class (cuisine)
        self.ClassFreq = defaultdict(int)
        # Terms in this class (cuisine)
        self.ClassTermCount = defaultdict(set)  
        # Occurrences of terms in class
        self.TermClassFrequency = defaultdict(dict) 
        # Duh unique terms
        self.unique_terms = set([]) 
        self.num_entries = 0
        self.length = []
        

    def tokenize(self, ingredients):
        if len(ingredients)==0:
            return []
        else:
            tokens = []
            for ingredient in ingredients:
                terms = ingredient.lower().split()
                for word in terms:
                    if word not in stopwords.words('english'):
                        tokens.append(word)
            tokens = [self.lemmatizer.lemmatize(term) for term in tokens]
            tokens = [self.stemmer.stem(term) for term in tokens]
            return tokens  
    
    def train(self):
        train_json = r'./train.json'
        with open(train_json) as train_data:
            self.RecipeData = json.load(train_data)

        self.num_entries = len(self.RecipeData)
        for index in range(self.num_entries):
            current_class = self.RecipeData[index]['cuisine']
            if len(current_class)==0:
                continue
            terms = self.tokenize(self.RecipeData[index]['ingredients'])
            self.length.append(len(terms))
            self.ClassFreq[current_class] = self.ClassFreq[current_class] + 1
            u_term = Counter(terms).keys()
            u_count = list(Counter(terms).values())

            term_index = 0
            for term in u_term:
                self.ClassTermCount[current_class].add(term)
                self.TermClassFrequency[term][current_class] = self.TermClassFrequency[term].get(current_class, 0) + u_count[term_index]
                term_index += 1

            self.unique_terms.update(set(terms))
        for key in self.ClassFreq:
            self.ClassFreq[key] = self.ClassFreq[key] / self.num_entries

    def nb_classify(self, query):
        terms = self.tokenize(query)
        result = defaultdict()

        for key in self.ClassFreq:
            prob = self.ClassFreq[key]
            for term in terms:
                prob = prob * ((self.TermClassFrequency[term].get(key, 0) + 1) / (len(self.ClassTermCount[key]) + len(self.unique_terms)))
            result[key] = prob
            
        return sorted(result.items(),key=lambda k:k[1],reverse=True)[0:5]   
    
    def load_pickle(self):
        print('Loading pickle files.')
        tempickle = open("pickled_files/class_freq.pickle","rb")
        self.ClassFreq = pickle.load(tempickle)
        tempickle.close()

        tempickle = open("pickled_files/class_term_count.pickle","rb")
        self.ClassTermCount = pickle.load(tempickle)
        tempickle.close()

        tempickle = open("pickled_files/unique_terms.pickle","rb")
        self.unique_terms = pickle.load(tempickle)
        tempickle.close()

        tempickle = open("pickled_files/term_class_freq.pickle","rb")
        self.TermClassFrequency = pickle.load(tempickle)
        tempickle.close()


    def store_pickle(self):
        print('Storing pickle files.")
        # Storing "this" object breaks functionality, store individual dicts
        tempickle = open("pickled_files/class_freq.pickle","wb")
        pickle.dump(self.ClassFreq, tempickle)
        tempickle.close()

        tempickle = open("pickled_files/class_term_count.pickle","wb")
        pickle.dump(self.ClassTermCount, tempickle)
        tempickle.close()

        tempickle = open("pickled_files/unique_terms.pickle","wb")
        pickle.dump(self.unique_terms, tempickle)
        tempickle.close()

        tempickle = open("pickled_files/term_class_freq.pickle","wb")
        pickle.dump(self.TermClassFrequency, tempickle)
        tempickle.close()
        # And now pickle no longer looks like a word

