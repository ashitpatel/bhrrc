import re
import json
from random import shuffle
from w3lib.html import remove_tags
import lxml
from lxml.html.clean import Cleaner

def clense(text, space_replacer = ' ', to_lower = True, remove_punc = True):
    # remove HTML comments first as suggested in https://stackoverflow.com/questions/28208186/how-to-remove-html-comments-using-regex-in-python

    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    text = cleaner.clean_html(text.encode("utf-8")).decode("utf-8")

    text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)
    text = remove_tags(text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text)   #remove non-ascii characters
    text = text.replace("&amp;", "and")
    text = text.replace("&", "and")
    text.strip()
    text.rstrip()
    text = text.replace("\r\n", "")
    text = text.replace("\n", "")
    text = text.replace("\"", "")
    if to_lower:
        text = text.lower()

    if remove_punc:
        # from https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
        text = re.sub(r'[^\w\s]', '', text)   #remove punctuation marks and non-word
        text = text.replace(",", "")

    text = re.sub(' +', space_replacer, text)
    #if  all(ord(char) < 128 for char in text) == False:
    #    text = ''
    ''.join(i for i in text if ord(i)<128)
    return text

# create the file ready-to-consume by fasttext from json file
#
# fasttext expects format of
# [__label__<label name>__ ]+ <text>
# e.g. __label__Other__ __label__Health__ The much-awaited debate on how 
#      international patent laws affect developing counties' access
#      to medications begins ...
#

def json2ft(jsonfile, ftfile, sourceLabel, targetLabel, sourceBody='body', targetBody='body'):
    with open(jsonfile) as json_posFile:
        posData = json.load(json_posFile)

    new_posData = []
    for x in posData:
        each_data = {}
        if x[sourceBody] is not None:
            if len(x[sourceBody]) < 5: # if body is empty
                continue
            each_data[targetBody] = x[sourceBody]
            unitemp = each_data[targetBody].encode('utf8').decode('utf-8')
            each_data[targetBody] = clense(unitemp,to_lower=False,remove_punc=False).strip()
            each_data[targetLabel] = []
            for y in range (len(x[sourceLabel])):
                each_data[targetLabel].append(x[sourceLabel][y])
            new_posData.append(each_data)

    shuffle(new_posData)

    f = open(ftfile, "w+")
    for x in new_posData:
        label = ""
        body = x[targetBody].strip()
        for y in x[targetLabel]:
            cat = ''
            for i in y:
                if i == ' ':
                    cat = cat + '_'
                else :
                    cat = cat + i
            label = label + '__label__' + cat.strip() + '__  '        
        f.write(label + body + '\n')
    f.close()
    return


# test the utility
# For example,
# when the following call is made, the result should be same as the result 
# obtained when running mid_level_data_process.ipynb
# json2ft("data/data_with_middle_layer.json", "mid_level_bhr.txt", 'middle_categories', 'mid_category')


#json2ft("data/data_with_middle_layer.json", "leaf_level_bhr.txt", 'leaf_categories', 'category')
