import requests 
from bs4 import BeautifulSoup 
import urllib
import json
import re
import cssutils


data = {}
link_list = []
text = 'python'
text = urllib.parse.quote_plus(text)
  
URL = "https://www.udacity.com/courses/all?search="+text
print(URL)

r = requests.get(URL)

  
soup = BeautifulSoup(r.content,'html.parser')
for a in soup.findAll('div', attrs={'class':'catalog-component__card'}):
     link = a.find('a', href = True)
     links = 'https://www.udacity.com'+ link['href']
     title = a.find('h3', attrs={'class':'card__title__school greyed'})
     sub_title = a.find('h2', attrs={'class':'card__title__nd-name'})
     skills = a.find('p', attrs={'class':'text-content__text'})
     data['links'] = links
     data['title'] = title.text
     data['sub_title'] = sub_title.text
     data['skills'] = skills.text
     link_list.append(data)


print(link_list)
# If this line causes an error, run 'pip install html5lib' or install html5lib 
 
with open("textbooks.json", "w") as writeJSON:
   json.dump(data, writeJSON, ensure_ascii=False)