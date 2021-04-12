import logging
import math


def main():
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s \n', level=logging.WARNING) #change to logging.DEBUG to get
                                                                                                     #output of each dictionary.

    example_comments = get_data()

    #I decided to hardcode in some comments just for this quick test run. Shouldn't be hard to take input files and transform
    # them into this same format.
    # CLASSIFICATION:
    #    - 0 = No Technical Debt
    #    - 1 = Contains Traditional Technical Debt
    #    - 2 = Contains Machine Learning Technical Debt                                                                                         
    '''example_comments = { 'licensed by microsoft filler text' : 0,
                         'checks that valid input was given' : 0,
                         'todo write tests' : 1,
                         'fixme workaround that an unknown error is fixed with' : 1,
                         'todo write prediction tests for a new model' : 2,
                         'todo preprocess this model data' : 2,
                         'todo train this model with new hyperparameters' : 2 }'''
    

    #from our input, create a dictionary consisting of each word and a 0 for now (will be changed later to the information gained)
    information_per_word = setupDict(example_comments)
    logging.debug(information_per_word)

    #create a dictionary consisting of the probability that each word appears in a comment
    word_prob = setupWordProb(example_comments, information_per_word)
    logging.debug(word_prob)

    #create a dictionary consisting of the probability that each label is used
    label_prob = setupLabelProb(example_comments)
    logging.debug(label_prob)

    #using the previous 4 dictionaries: comments + label, word with dedicated spot for information gained,
    #   every word and its probability that it appears, and each label and the probability that it appears
    #   find the information gain using the correct formula
    information_per_word = informationGain(example_comments, information_per_word, word_prob, label_prob)
    
    feature_words = []
    for k,v in sorted(information_per_word.items(), key=lambda p:p[1]):
        feature_words.append(k + ' ' + str(v))
    
    percent_chosen = int(len(feature_words) * 0.15)
    
    with open('FEATURE_WORDS.txt','w') as outputFile:

        for item in feature_words[len(feature_words) - percent_chosen:]:
            outputFile.write(item)
            outputFile.write('\n')

    


def setupDict(aDict):

    output = {}

    for item in aDict:
        for word in item.split():
            output[word] = 0
    return output

def setupWordProb(commentDict, wordDict):
    
    output = {}

    for word in wordDict:
        counter = 0
        for comment in commentDict:
            if word in comment.split(): #need to split, otherwise a word like 'autodoc' would be a false positive including 'todo'
                counter += 1
        output[word] = counter / len(commentDict)

    return output

def setupLabelProb(commentDict):

    output = {}

    for item in commentDict:
        if commentDict[item] not in output:
            output[commentDict[item]] = 1
        else:
            output[commentDict[item]] += 1
    
    for item in output:
        output[item] = output[item] / len(commentDict)

    return output

def informationGain(commentDict, outputDict, wordDict, labelDict):

    #using each word in the outputDict
    for word in outputDict:

        #reset result to 0
        result = 0

        #keep track of the amount of times each word is found within a comment of each label
        #the dictionary is initialized as: 
        #   - We have seen label 0 a total of 0 times
        #   - We have seen label 1 a total of 0 times
        #   - We have seen label 2 a totla of 0 times
        information_gained = {0: 0, 1: 0, 2: 0, 3: 0}
        for comment in commentDict:
            if word in comment.split():

                #if we find the current word in a comment, increment the appropriate counter in our dictionary
                information_gained[commentDict[comment]] += 1
        
        #Information Gain Formula:
        #   IG = p(w,t) * log ( p(w,t) / ( p(w) * p(t) ) )
        #       - p(w,t) = probability that a word 'w' appears in a comment with label 't'
        #       - p(w) = probability that a word 'w' appears in a comment
        #       - p(t) = probability that a label 't' appears in a comment
        for info in information_gained:

            prob_word_label = information_gained[info] / len(commentDict) #finds p(w,t)

            if prob_word_label != 0: #math.log throws an error if we pass it 0
                result += prob_word_label * math.log( prob_word_label / (wordDict[word] * labelDict[info]))

        outputDict[word] = result

    #return the Information Gain Dictionary recorded and pray that I didn't make any algorithmic errors anywhere :)
    return outputDict

def get_data():
    output = {}
    refer = {'TD\n': 1, 'DSTD\n': 2, 'NO TD\n': 3}
    with open('FINAL_COMMENTS_UNDERGRAD.csv', 'r') as inputFile:
        dataset = inputFile.readlines()
    for item in dataset:
        item = item.split(',')
        if item[6] in refer:
            output[preprocess(item[3])] = refer[item[6]]

    return output

def preprocess(comment):

    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()

    to_replace = ['\\','/','(', ')', '[', ']' ';',':', ',', '.', '!', '?', '#', '~', '_', '+','-', '1','2','3','4','5','6','7','8','9','0', '@','\'', '`', '"', '>', '<', '*']
    bad_words = ['but', '||', 'the', 'then', 'an', 'a', 'our', 'than', 'with','after', 'give', 'of', 'what',
                 'me', 'own', 'too', 'for', 'on', 'that', 'so', 'and', 'ahundt','but', 'we','when','we', 'when',
                 'got', 'how','kgf','it',';', 'are','these','n','t','eof','==','c','l','those']

    for word in to_replace:
        comment = comment.replace(word, ' ')

    comment = comment.lower()
    comment = comment.split()

    toBuild = []
    for item in comment:
        item = lemmatizer.lemmatize(item)
        if item not in bad_words:
            toBuild.append(item)
    
    return ' '.join(toBuild)


if __name__ == '__main__':
    main()