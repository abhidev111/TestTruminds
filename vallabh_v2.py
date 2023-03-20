'''
This code works only for the heading but uses regex for matching.
'''

import re
import requests
from bs4 import BeautifulSoup
import gpt_summary
import tikTokenn
resp = requests.get('https://en.wikipedia.org/wiki/India')
word = "Biodiversity"
lst_of_open_tags = ["<h1>","<h2>","<h3>","<h4>","<h5>","<h6>"]
lst_of_close_tags = ["</h1>","</h2>","</h3>","</h4>","</h5>","</h6>"]
index_of_lst_of_tags = 0
matches = []
para =""
while index_of_lst_of_tags< len(lst_of_open_tags):
    for item in re.finditer(lst_of_open_tags[index_of_lst_of_tags],resp.text):
        # print(item)
        matches.append(item)
    for index,match in enumerate(matches):
        if index == len(matches) - 1:
            break
        start = match.span()[0]
        end = matches[index+1].span()[0]
        text = resp.text[start:end]

        for item in re.finditer(lst_of_close_tags[index_of_lst_of_tags],text):
            header_text = text[:item.span()[1]]
            soup = BeautifulSoup(header_text, 'html.parser')
            # if "Biodiversity" in soup.text:
            if re.search(re.compile('.{0,100}' #100 charaters before the word until you find a newlinee
                                        + word 
                                        +'.{0,100}' #100 characters after the word untill you find a newline
                                        ,re.IGNORECASE
                                        ), soup.text):
                soup = BeautifulSoup(text, 'html.parser')
                para = para +" "+ soup.text
                print("this content is from :",lst_of_open_tags[index_of_lst_of_tags])
    index_of_lst_of_tags += 1
print(para)
with open("test.txt", 'w', encoding='utf-8') as html_file:
    html_file.write(para)
# print(tikTokenn.get_token_size(para))
print("\nSummary 1")           
summary1 = gpt_summary.summarize_using_gpt_3_0(para)
print(summary1)

# print("\n")
print("\nSummary 2")
summary2 = gpt_summary.summarize_using_gpt_3_5_turbo(para)
print(summary2)