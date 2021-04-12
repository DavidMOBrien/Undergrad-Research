import os
import classify

def getComments(filename):
    import tokenize

    fileObj = open(filename, 'r')

    output = []
    for toktype, tok, start, end, line in tokenize.generate_tokens(fileObj.readline):
        # we can also use token.tok_name[toktype] instead of 'COMMENT'
        # from the token module 
        if toktype == tokenize.COMMENT:
            output.append(tok)

    return output

def runner(path):
    from datetime import datetime

    output = recursive_helper(path)

    os.chdir(path + '/5-OUTPUT')

    now = datetime.now()
    filename = now.strftime("%d-%m-%Y-%H-%M-%S.txt")

    with open(filename, 'w') as outputFile:
        outputFile.write(output)


def recursive_helper(path):

    os.chdir(path)
    print('going to ' + path)

    ignorable_directories = ['.git', '__pycache__']

    content = os.listdir()
    
    output = ''

    #first, we want to classify all local python files before going into a directory
    for item in content:
        if item.endswith('.py'):
            comments = getComments(item)

            for comment in comments:
                result = classify.classify(comment)

                if result == ['td']:
                    output = output + os.getcwd() + ' : TD\n       ' + comment + '\n\n'

                if result == ['dstd']:
                    output = output + os.getcwd() + ' : DSTD\n       ' + comment + '\n\n'
    
    #next, we want to go into each neighboring directory
    for item in content:
        if os.path.isdir(item) and item not in ignorable_directories:
            output += recursive_helper(path + '/' + item)
        os.chdir(path)
    
    print('leaving ' + path)

    return output

runner('G:/My Drive/IMPORTANT_STUFF/8TH SEMESTER/UNDERGRAD_RESEARCH')