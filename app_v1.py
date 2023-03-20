#python -u "c:\Users\Abhishek K\Desktop\soup\actual_task\app_v1.py" --link "https://en.wikipedia.org/wiki/india" --keywords "Biodiversity" --out "output3.json"

from bs4 import BeautifulSoup 
import re
import requests
import argparse
import remove_stopwords
import gpt_summary
import json

parser = argparse.ArgumentParser()
parser.add_argument("--link", help = "Please enter URL", required=True)  
parser.add_argument("--keywords", help = "Please enter keywords",required=True)  
parser.add_argument("--out", help = "operation") 
args = parser.parse_args()  

URL = args.link
Words = remove_stopwords.remove_stpwrds(args.keywords)
# print(Words)

# url = "https://en.wikipedia.org/wiki/india"
html = requests.get(URL).text
htmlParse = BeautifulSoup(html, 'lxml')

#suppose query is given as a statement : "India's biodiversity"
# Words = ["Biodiversity","India"]

textP = ""
for word in Words:
    for r in re.findall(re.compile('.{0,500}' #50 charaters before the word until you find a newlinee
                                    + word 
                                    +'.{0,1000}' #500 characters after the word untill you find a newline
                                    ,re.IGNORECASE
                                    ), htmlParse.text ):
        textP = textP + r  
print("\n"+textP+"\n\n")
summary1 = gpt_summary.summarize_using_gpt_3_0(textP)
print(summary1)

# print("\n")
# summary2 = gpt_summary.summarize_using_gpt_3_5_turbo(textP)
# print(summary2)

final_output = {
        "Link" : URL,
        "Keyword" : Words,
        "Summary" : summary1
                }

with open("abc.json", "w") as outfile:
    json.dump(final_output, outfile,ensure_ascii=False)