import math

def clean_text(txt):
    new_words = txt
    for symbol in """.,?"'!;:""":
        new_words = new_words.replace(symbol, '')
        lowercase = new_words.lower()
        split = lowercase.split()
    return split

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)
    
def stem(s): 
    """ accepts a string as a parameter. The function should then 
        return the stem of s.
    """
    if len(s) > 0 and len(s) < 4:
        return s
    
    if s[-1] == 's':
        s = s[:-1]
    if s[-3:] == 'ize' or s[-3:] == 'ing' or s[-3:] == 'ise':
        if len(s) <= 4:
            s = s
        elif s[-4] == s[-5]:
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-2:] == 'er':
        s = s[:-2]
    elif s[-1] == 'e':
        s = s[:-1]
    elif s[-1] == 'y':
        s = s[:-1] + 'i'
    if s[-4:] == 'ship' and s != 'ship':
        s = s[:-4]
    if s[:3] == 'pre' or s[:3] == 'sub' or s[:3] == 'dis':
        s = s[3:]
    if s[:2] == 'un':
        s = s[2:]
        
    return s

def compare_dictionaries(d1, d2):
    """ take two feature dictionaries d1 and d2 as inputs, 
        and it should compute and return their log similarity 
        score – using the procedure described above.
    """
    count = 0
    total = sum(d1.values())
    for s in d2:
        if s in d1:
            count += math.log(d1[s] / total) * d2[s]
        else:
            count += math.log((1/2) / total) * d2[s]
    return count


        
class TextModel:
        
    def __init__(self, model_name):
            self.name = model_name
            self.words = {}
            self.word_lengths = {}
            self.stems = {}
            self.sentence_lengths = {}
            self.num_of_periods = {}
            
    def __repr__(self):
        """ returns a string that includes the name of the model as 
            well as the sizes of the dictionaries for each feature of the text.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of periods: ' + str(len(self.num_of_periods)) + '\n'

        return s
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model.
        """

    # Add code to clean the text and split it into a list of words.
    # *Hint:* Call one of the functions you have already written!
        count = 0
        for w in s.split():
            count += 1
            if w[-1] == '.' or w[-1] == '?' or w[-1] == '!':
                if count not in self.sentence_lengths:
                    self.sentence_lengths[count] = 1
                    count = 0
                else:
                    self.sentence_lengths[count] += 1
                    count = 0
        
        periods = 0
        for w in s.split():   
            if w == '.':
                periods += 1
                if w not in self.num_of_periods:
                    self.num_of_periods[w] = 1
                else:
                    self.num_of_periods[w] += 1
                   
        word_list = clean_text(s)
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        
        for w in self.words:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
        
        for w in word_list:
            w = stem(w)
            if w not in self.stems:
                self.stems[w] = 1
            else:
                self.stems[w] += 1
                
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model. 
            It should not explicitly return a value.
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()  
        self.add_string(text)  
        
    def save_model(self):
        """ saves the TextModel object self by writing its various feature 
            dictionaries to files. There will be one file written for each 
            feature dictionary.
        """
        f1 = open((self.name + '_' + 'words'), 'w')
        f2 = open((self.name + '_' + 'word_lengths'), 'w')
        f3 = open((self.name + '_' + 'stems'), 'w')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'w')
        f5 = open((self.name + '_' + 'num_of_periods'), 'w')

        f1.write(str(self.words))
        f2.write(str(self.word_lengths))
        f3.write(str(self.stems))
        f4.write(str(self.sentence_lengths))
        f5.write(str(self.num_of_periods))

        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()

        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from 
            their files and assigns them to the attributes of the called TextModel.
        """
        f1 = open((self.name + '_' + 'words'), 'r')
        f2 = open((self.name + '_' + 'word_lengths'), 'r')
        f3 = open((self.name + '_' + 'stems'), 'r')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'r')
        f5 = open((self.name + '_' + 'num_of_periods'), 'r')

        d_str1 = f1.read()
        d_str2 = f2.read()
        d_str3 = f3.read()
        d_str4 = f4.read()
        d_str5 = f5.read()

        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
                
        self.words = eval(d_str1)
        self.word_lengths = eval(d_str2)
        self.stems = eval(d_str3)
        self.sentence_lengths = eval(d_str4)
        self.num_of_periods = eval(d_str5)
    
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores 
            measuring the similarity of self and other – one score 
            for each type of feature
        """
        scores = []
        word_score = compare_dictionaries(other.words, self.words)
        scores += [word_score]
        word_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        scores += [word_score]
        word_score = compare_dictionaries(other.stems, self.stems)
        scores += [word_score]
        word_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        scores += [word_score]
        word_score = compare_dictionaries(other.num_of_periods, self.num_of_periods)
        scores += [word_score]
        return scores
        
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source” 
            TextModel objects (source1 and source2) and determines which of 
            these other TextModels is the more likely source of the called 
            TextModel.
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name, scores1)
        print('scores for ' + source2.name, scores2)
        weighted_sum1 = 10*scores1[0] + 5*scores1[1] + 7*scores1[2] + 3*scores1[3] + 1*scores1[4]
        weighted_sum2 = 10*scores2[0] + 5*scores2[1] + 7*scores2[2] + 3*scores2[3] + 1*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print()
            print('The work' + ' by ' + self.name + ' is more likely to have come from ' + source1.name)
            print()
        else:
            print()
            print('The work' + ' by ' + self.name + ' is more likely to have come from ' + source2.name)
            print()

                



def test():
    """ """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ """
    source1 = TextModel('rowling')
    source1.add_file('rowling.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('rowling2')
    new1.add_file('rowling2.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('Suzanne Collins')
    new2.add_file('hungergames.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('JRR Tolkien')
    new3.add_file('lord_of_the_rings.txt')
    new3.classify(source1, source2)
                
                