#summarizes java from a file
# python run.py file
# file = file in data/java, by default code.java
# if json, will extract multiple, use format in code.json

import sys
import javalang
import nltk
import re
import subprocess
import json
from types import SimpleNamespace
nltk.download('punkt') 

#point to the data directory
dataFolder = "../data/java"
#the name of the java file to summarize
codeFile = "code.java"
outputFile = "test.code"
nums = [
    javalang.tokenizer.DecimalInteger, 
    javalang.tokenizer.Integer, 
    javalang.tokenizer.FloatingPoint,
    javalang.tokenizer.DecimalFloatingPoint,
    javalang.tokenizer.HexInteger,
]
command = "bash generate.sh -1 code2jdoc test.code"
summaryFile = "../tmp/code2jdoc_beam.json"

if(len(sys.argv) > 1):
    codeFile = sys.argv[1]

def run():
    """
    Auto run the process to take code from code.java, tokenize, save then run the summarization.
    For now we take a single file to try this out.
    """

    

    # get code
    f = open(dataFolder+"/"+codeFile, "r")
    code = f.read()

    if(codeFile.endswith(".java")):
        code = [code]
    elif(codeFile.endswith(".json")):
        data = json.loads(code)
        keys = data.keys()
        code = []
        for k in keys:
            code.append(data[k]["code"])

    lines = []
    for c in code:
        tokens = tokenize(c)
        line = " ".join(tokens)
        lines.append(line)


    #write to file
    f = open(dataFolder+"/"+outputFile, "w")
    f.write("\n".join(lines))
    f.close()

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    f = open(summaryFile, "r")
    data = f.read()
    x = json.loads(data)
    keys = x.keys()
    print("\n-----------------\n\nOUTPUT:\n")
    for k in keys:
        print(k + ": " + str(x[k][0]))


# the included tokenizer doesnt include the variable type processing, easier to just reimplement everything with
# the javalang tokenizer they linked in an issue for it
def tokenize(code):
    tokens = javalang.tokenizer.tokenize(code)
    tokenArray = []
    for t in tokens:
        if isinstance(t, javalang.tokenizer.Identifier):
            tokenArray.extend(identifier_tokenize(t.value))
            pass
        elif isinstance(t, javalang.tokenizer.String):
            tokenArray.append("STRING")
            pass
        elif isinstance(t, tuple(nums)):
            tokenArray.append("NUM")
            pass
        elif isinstance(t, javalang.tokenizer.Boolean):
            tokenArray.append("BOOL")
        else:
            tokenArray.append(t.value)
    return tokenArray

def identifier_tokenize(identifier):
    snake_split = identifier.split('_')
    modified_test = ' _ '.join(snake_split)
    tokens = []
    tokens.extend(tokenize_with_camel_case(modified_test))
    return tokens
    pass

def tokenize_with_camel_case(token):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', token)
    return [m.group(0) for m in matches]


run()