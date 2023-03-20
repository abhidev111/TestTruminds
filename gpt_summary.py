import os
import openai
openai.organization = "org-0t4UHmadsZ86PjLqG9Q3uwaT"
openai.api_key = "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"
# tru apikey - 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
# prsnl api key -  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


def summarize_using_gpt_3_0(paragraph):
    '''
    Input : 
      paragraph : paragraph that is to be summarised
    Output :
      summary of the paragraph provided
    '''
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt = paragraph+"\n\nTl;dr",
    temperature=0.7,
    max_tokens=300,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1
    )
    return response.choices[0].text


# Note: you need to be using OpenAI Python v0.27.0 for the code below to work

def summarize_using_gpt_3_5_turbo(paragraph,keyword):
    '''
    Input : 
      paragraph : paragraph that is to be summarised
      keyword   : Keyword with respect to which para is to be summarized
    Output :
      summary of the paragraph provided
    '''
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          
          {"role": "assistant", "content": paragraph},
          {"role": "user", "content": "summarize the given paragraphs with respect to"+keyword}
      ]
    )
    return response.choices[0].message.content
