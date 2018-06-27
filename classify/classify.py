import sys
import os

sys.path.append("../util")

import util
util.json2ft(jsonfile="data/classified_data.json", ftfile="classify.txt", sourceLabel='classification', targetLabel='classification')
