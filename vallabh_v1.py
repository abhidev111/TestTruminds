'''
this code works perfectly fine if the keyword is present in the heading 
'''

import re
import requests
from bs4 import BeautifulSoup
import gpt_summary
resp = requests.get('https://en.wikipedia.org/wiki/Los_Angeles')
matches = []
para =""
for item in re.finditer("<h2>",resp.text):
    print(item)
    matches.append(item)
for index,match in enumerate(matches):
    if index == len(matches) -1:
        break
    start = match.span()[0]
    end = matches[index+1].span()[0]
    text = resp.text[start:end]

    for item in re.finditer("</h2>",text):
        header_text = text[:item.span()[1]]
        soup = BeautifulSoup(header_text, 'html.parser')
        if "American Name Society" in soup.text:
            soup = BeautifulSoup(text, 'html.parser')
            # print(soup.text)
            para = para + " "+ soup.text
print(para)
print("\nSummary 1")           
summary1 = gpt_summary.summarize_using_gpt_3_0(para)
print(summary1)

# print("\n")
print("\nSummary 2")
summary2 = gpt_summary.summarize_using_gpt_3_5_turbo(para)
print(summary2)