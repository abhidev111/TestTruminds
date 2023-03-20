'''
This code works for the heading and also looks for specific word in the paragraph 
if the word is found then it fetches the entire content below the heading till the next heading 
'''
#RUNNING COMMAND : python -u "c:\Users\Abhishek K\Desktop\soup\actual_task\selenium_v2.py" --link "https://en.wikipedia.org/" --keywords "homelessness" --out "output.json"

#python -u "c:\Users\Abhishek K\Desktop\soup\actual_task\selenium_v2.py" --link "https://en.wikipedia.org/" --keywords "2023 AFC Asian Cup Qualifiers" --out "output.json"

#python -u "c:\Users\Abhishek K\Desktop\soup\actual_task\selenium_v2.py" --link "https://en.wikipedia.org/" --keywords "2021 SAFF Championship" --out "output4.json"

#python -u "c:\Users\Abhishek K\Desktop\soup\actual_task\selenium_v2.py" --link "https://en.wikipedia.org/" --keywords "Asian Icon" --out "output5.json"

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import gpt_summary
import sys
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("--link", help = "Please enter URL", required=True)  # https://en.wikipedia.org/
parser.add_argument("--keywords", help = "Please enter keywords",required=True)  
parser.add_argument("--out", help = "Please enter outfile name") 

args = parser.parse_args()

URL = args.link
FILE_NAME = args.out
CITY_NAME = "Sunil Chhetri"
driver =  webdriver.Chrome()
driver.get(URL)
driver.implicitly_wait(10)
search_field = driver.find_element(By.ID,"searchInput")
time.sleep(1)
search_field.send_keys(CITY_NAME)
time.sleep(1)
search_button = driver.find_element(By.XPATH,'//*[@id="searchform"]/div/button')
search_button.click()

resp = driver.page_source


from bs4 import BeautifulSoup
import re

Words = args.keywords #"Global Financial Centres Index" #args.keywords
lst_of_open_tags = ["<h1","<h2","<h3","<h4","<h5","<h6"]
# lst_of_close_tags = ["</h1>","</h2>","</h3>","</h4>","</h5>","</h6>"]
index_of_lst_of_tags = 0
matches = []
para = ""
p_matches = []

while index_of_lst_of_tags< len(lst_of_open_tags):
    for item in re.finditer(lst_of_open_tags[index_of_lst_of_tags],resp):
        # print(item)
        matches.append(item)
    index_of_lst_of_tags+=1

def find_upper_header_tag(start):
    '''
    Function that finds nearest header tag to the paragraph where desired word is found
    '''
    min_head_idx = 0
    min_diff = sys.maxsize
    tag = "<h2>"
    for match in matches:
        if abs(match.span()[0]-start) < min_diff:
            min_head_idx = match.span()[0]
            #  print("------>>>>",type(match.group()))
            min_diff = abs(match.span()[0]-start) 
            tag = match.group()
    # print(min_head_idx, tag)  
    return (min_head_idx, tag)

def find_lower_header_tag(end , tag):
    min_head_idx = end
    min_diff = sys.maxsize
    for match in matches:
        if abs(match.span()[0]-end) < min_diff and (match.span()[0] > end) and (match.group()==tag):
            min_head_idx = match.span()[0]
            min_diff = abs(match.span()[0] - end)
    # print(min_head_idx, tag)  
    return (min_head_idx)


for item in re.finditer("<p>",resp):
    # print(item)
    p_matches.append(item)

for index, match in enumerate(p_matches):
    if index == len(p_matches) - 1:
            break
    start = match.span()[0]
    end = p_matches[index+1].span()[0]
    p_text = resp[start:end]
    soup = BeautifulSoup(p_text, 'html.parser')
    if re.search(re.compile('.{0,100}' #100 charaters before the word until you find a newlinee
                                        + Words 
                                        +'.{0,100}' #100 characters after the word untill you find a newline
                                        ,re.IGNORECASE
                                        ), soup.text):
        
        upper_head_idx, tag = find_upper_header_tag(start)
        lower_head_idx = find_lower_header_tag(end,tag)
        req_content = resp[upper_head_idx:lower_head_idx]
        soup = BeautifulSoup(req_content, 'html.parser')
        para += soup.text

if para == "":
    print("No Content was found")

else :
    print(para)
    # summary1 = gpt_summary.summarize_using_gpt_3_0(para)
    # print(summary1)
    summary2 = gpt_summary.summarize_using_gpt_3_5_turbo(para,Words)
    print(summary2)


    # Rendering output in the form of Json file
    final_output = {
        "Link" : driver.current_url,
        "Keyword" : Words,
        "Summary" : summary2
                }

    with open(FILE_NAME, "w") as outfile:
        json.dump(final_output, outfile,ensure_ascii=False)



























#This finds the contents between the headings 
# while index_of_lst_of_tags< len(lst_of_open_tags):
#     for item in re.finditer(lst_of_open_tags[index_of_lst_of_tags],resp):
#         print(item)
#         matches.append(item)
#     for index,match in enumerate(matches):
#         if index == len(matches) - 1:
#             break
#         start = match.span()[0]
#         end = matches[index+1].span()[0]
#         text = resp[start:end]

#         for item in re.finditer(lst_of_close_tags[index_of_lst_of_tags],text):
#             header_text = text[:item.span()[1]]
#             soup = BeautifulSoup(header_text, 'html.parser')
#             # if "Biodiversity" in soup.text:
#             if re.search(re.compile('.{0,100}' #100 charaters before the word until you find a newlinee
#                                         + Words 
#                                         +'.{0,100}' #100 characters after the word untill you find a newline
#                                         ,re.IGNORECASE
#                                         ), soup.text):
#                 soup = BeautifulSoup(text, 'html.parser')
#                 para = para +" "+ soup.text
#                 print("this content is from :",lst_of_open_tags[index_of_lst_of_tags])
#     index_of_lst_of_tags += 1
#------------------------------------------------------------------------------"
# htmlParse = BeautifulSoup(resp, 'lxml')
# Words =["American Name Society"]
# for word in Words:
#     for r in re.findall(re.compile('.{0,500}' #500 charaters before the word until you find a newlinee
#                                     + word 
#                                     +'.{0,1000}' #1000 characters after the word untill you find a newline
#                                     ,re.IGNORECASE
#                                     ), htmlParse.text ):
#         para = para+ " " + r 

# with open("test.txt", 'w', encoding='utf-8') as html_file:
#     html_file.write(para)

