import feedparser
from dateutil import parser
import urllib
import requests
import re
from subprocess import call, Popen, PIPE, STDOUT

# sys and os are needed to invoke sys.path.append()
import sys
import os

sys.path.append("../util")
import util
import future


#google_news_rss_url = 

feed_url_list = [
"https://www.google.com/alerts/feeds/13351239696798776176/3559988229559370877",
"http://feeds.reuters.com/reuters/businessNews",
]

future_calls = [future.Future(feedparser.parse,rss_url) for rss_url in feed_url_list]
feeds = [future_obj() for future_obj in future_calls]

entries = []
for feed in feeds:
    entries.extend( feed[ "items" ] )

#for entry in entries:
#    print(entry.keys())
#    if not "date_parsed" in entry:
#        entry["date_parsed"] = entry["published"]
    

try:
    sorted_entries = sorted(entries, key=lambda entry: parser.parse(entry["published"]))
except:
    print("exception occurred")
sorted_entries.reverse() # for most recent entries first
#sorted_entries = entries

for item in sorted_entries:
#    print(item["date"] + " : " + item["title"])
    print(item["published"])


# 1. Traverse the link to capture the news item content

    response = requests.get(item["link"]) 

    # Process google newsfeed by traversing the link
    if "window.googleJavaScriptRedirect" in response.text:
        match = re.search('navigateTo\(window.parent,window,(.+?)\)', html)
        if match:
            url = match.group(1)
            try:
                url = url.replace('"', '')
                response = requests.get(url)
                item["link"] = url
            except:
                print('exception')


# 2. clense the content

    html = response.text
    item["content"] = util.clense(html, to_lower=False, remove_punc=False).strip()
    print(item["link"])
#    print(item["content"])

# 3. classify the content
#    - store rejected items and their content  in a file

    process = Popen(["fasttext", "predict", "../classify/classify_model.bin", "-", "1"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    (output, err) = process.communicate(input=item["content"].encode("utf-8"))
    exit_code = process.wait()

    # print the category label
    print(output.decode("utf-8"))

# 4. get non-leaf and leaf categories for the content
#    - Be as close as possible to RSS format
#      [{"published":<published date>, "link": <url to news>, 
#        "summary": <summary>
#
# 5. Use hashmap for converting to json
    if "__label__HR__" in output.decode("utf-8"):
        process = Popen(["fasttext", "predict", "../categorize/midlevel_model.bin", "-", "8"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (output, err) = process.communicate(input=item["content"].encode("utf-8"))
        exit_code = process.wait()
        print("midlevel categories: " + output.decode("utf-8"))

        process = Popen(["fasttext", "predict", "../categorize/leaflevel_model.bin", "-", "8"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (output, err) = process.communicate(input=item["content"].encode("utf-8"))
        exit_code = process.wait()
        print("leaf level categories: " + output.decode("utf-8"))

    print(item["summary"])
