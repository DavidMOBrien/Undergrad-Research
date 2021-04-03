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

def commentToVector(comment):
    import pandas as pd

    feature_words = []

    with open('FEATURE_WORDS.txt', 'r') as inputFile:
        dataset = inputFile.readlines()

        for item in dataset:
            feature_words.append(item[:item.find(' ')])
        
        del dataset

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

    loaded_model = pickle.load(open('saved_model.pkl', 'rb'))

    return loaded_model.predict(myVector)


def classify(comment):

    comment = preprocess(comment)

    commentVector = commentToVector(comment)

    print(classifyComment(commentVector))

classify('the code below preprocesses our connections')