import sys
import os

sys.path.append("../util")

import util
util.json2ft(jsonfile="data/data_with_middle_layer.json", ftfile="midlevel_bhr.txt", sourceLabel='middle_categories', targetLabel='category')
