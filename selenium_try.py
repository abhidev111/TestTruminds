'''
This code works for the heading and also looks for specific word in the paragraph 
if the word is found then it fetches 
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import gpt_summary
# from threading import *

driver =  webdriver.Chrome()
driver.get("https://www.wikipedia.org/")
driver.implicitly_wait(10)
search_field = driver.find_element(By.ID,"searchInput")
time.sleep(1)
search_field.send_keys("Los Angeles")
time.sleep(1)
search_button = driver.find_element(By.XPATH,'//*[@id="search-form"]/fieldset/button/i')
search_button.click()

resp = driver.page_source


from bs4 import BeautifulSoup
import re

Words = "American Name Society"
lst_of_open_tags = ["<h1>","<h2>","<h3>","<h4>","<h5>","<h6>"]
lst_of_close_tags = ["</h1>","</h2>","</h3>","</h4>","</h5>","</h6>"]
index_of_lst_of_tags = 0
matches = []
para =""
#This finds the contents between the headings 
while index_of_lst_of_tags< len(lst_of_open_tags):
    for item in re.finditer(lst_of_open_tags[index_of_lst_of_tags],resp):
        print(item)
        matches.append(item)
    for index,match in enumerate(matches):
        if index == len(matches) - 1:
            break
        start = match.span()[0]
        end = matches[index+1].span()[0]
        text = resp[start:end]

        for item in re.finditer(lst_of_close_tags[index_of_lst_of_tags],text):
            header_text = text[:item.span()[1]]
            soup = BeautifulSoup(header_text, 'html.parser')
            # if "Biodiversity" in soup.text:
            if re.search(re.compile('.{0,100}' #100 charaters before the word until you find a newlinee
                                        + Words 
                                        +'.{0,100}' #100 characters after the word untill you find a newline
                                        ,re.IGNORECASE
                                        ), soup.text):
                soup = BeautifulSoup(text, 'html.parser')
                para = para +" "+ soup.text
                print("this content is from :",lst_of_open_tags[index_of_lst_of_tags])
    index_of_lst_of_tags += 1
#------------------------------------------------------------------------------"
htmlParse = BeautifulSoup(resp, 'lxml')
Words =["American Name Society"]
for word in Words:
    for r in re.findall(re.compile('.{0,500}' #500 charaters before the word until you find a newlinee
                                    + word 
                                    +'.{0,1000}' #1000 characters after the word untill you find a newline
                                    ,re.IGNORECASE
                                    ), htmlParse.text ):
        para = para+ " " + r 

# with open("test.txt", 'w', encoding='utf-8') as html_file:
#     html_file.write(para)

summary1 = gpt_summary.summarize_using_gpt_3_0(para)
print(summary1)

print("\n")
summary2 = gpt_summary.summarize_using_gpt_3_5_turbo(para)
print(summary2)