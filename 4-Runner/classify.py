def preprocess(comment):

    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()

    #follow same preprocess methods used to create feature data
    to_replace = ['\\','/','(', ')', '[', ']' ';',':', ',', '.', '!', '?', '#', '~', '_', '+','-', '1','2','3','4','5','6','7','8','9','0', '@','\'', '`', '"', '>', '<', '*']
    bad_words = ['but', '||', 'the', 'then', 'an', 'a', 'our', 'than', 'with','after', 'give', 'of', 'what',
                 'me', 'own', 'too', 'for', 'on', 'that', 'so', 'and', 'ahundt','but', 'we','when','we', 'when',
                 'got', 'how','kgf','it',';', 'are','these','n','t','eof','==','c','l','those']

    for word in to_replace:
        comment = comment.replace(word, ' ')

    comment = comment.lower()
    comment = comment.split()

    #lemmatize all legal words and reconstruct the preprocessed string
    toBuild = []
    for item in comment:
        item = lemmatizer.lemmatize(item)
        if item not in bad_words:
            toBuild.append(item)
    
    return ' '.join(toBuild)

def commentToVector(comment):
    import pandas as pd

    feature_words = []

    #the FEATURE_WORDS.txt file follows the structure:
    #       feature_word value
    #we only want the feature_word, and not the information gain value
    with open('G:/My Drive/IMPORTANT_STUFF/8TH SEMESTER/UNDERGRAD_RESEARCH/4-Runner/FEATURE_WORDS.txt', 'r') as inputFile:
        dataset = inputFile.readlines()

        for item in dataset:
            feature_words.append(item[:item.find(' ')])
        
        del dataset

    #construct a list of 0s and 1s indicating if word at index n is in the given comment
    outputVector = []
    comment_split = comment.split()

    for item in feature_words:
        if item in comment_split:
            outputVector.append('1')
        else:
            outputVector.append('0')

    outputVector = pd.DataFrame([outputVector]).values

    return outputVector

def classifyComment(myVector):
    import pickle
    from sklearn.neural_network import MLPClassifier as Classifier
    from sklearn.model_selection import train_test_split

    #load our pretrained model that currently has an 89% accuracy rating
    #and use it to classify the comment, return the predicted result
    loaded_model = pickle.load(open('G:/My Drive/IMPORTANT_STUFF/8TH SEMESTER/UNDERGRAD_RESEARCH/4-Runner/saved_model_v2.pkl', 'rb'))

    return loaded_model.predict(myVector) 

def classify(comment):

    #preprocess the comment
    comment = preprocess(comment)

    #turn the preprocessed comment into a classifiable data structure
    commentVector = commentToVector(comment)

    return classifyComment(commentVector)
