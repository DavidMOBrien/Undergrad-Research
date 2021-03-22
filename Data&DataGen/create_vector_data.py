with open('FEATURE_WORDS.txt', 'r') as inputFile:
    dataset = inputFile.readlines()

    feature_words = []

    for item in dataset:
        feature_words.append(item[:item.find(' ')])
    
    del dataset


with open('COMMENTS_AND_TD.csv', 'r') as inputFile:
    dataset = inputFile.readlines()

    to_replace = ['\\','/','(', ')', '[', ']' ';',':', ',', '.', '!', '?', '#', '~', '_', '+','-', '1','2','3',
                    '4','5','6','7','8','9','0', '@','\'', '`', '"', '>', '<', '*']

    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    with open('trainable_data.csv','a') as outputFile:
        outputFile.write(','.join(feature_words))
        outputFile.write(',RESULT\n')

    for item in dataset:
        item = item.lower()
        item = item.split(',')

        for symbol in to_replace:
            item[0] = item[0].replace(symbol, ' ')

        comment_split = item[0].split()

        for i in range(len(comment_split)):
            comment_split[i] = lemmatizer.lemmatize(comment_split[i])
        
        toWrite = ''

        for feature in feature_words:
            if feature in comment_split:
                toWrite = toWrite + '1,'
            else:
                toWrite = toWrite + '0,'
        
        toWrite = toWrite + item[1]

        with open('trainable_data.csv', 'a') as outputFile:
            outputFile.write(toWrite)