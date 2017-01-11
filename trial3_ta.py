#We begin by reading in the source code for a given web page and creating a Beautiful Soup object with the BeautifulSoup function.
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


req = Request('https://reviewboard.mozilla.org/r/?sort=review_id&datagrid-id=datagrid-0&columns=review_id&show-closed=1&page=1', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
#r = urllib.request.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
soup = BeautifulSoup(webpage, "lxml")
print(type(soup))
             #'"https://reviewboard.mozilla.org/r/?sort=review_id&datagrid-id=datagrid-0&columns=review_id&show-closed=1&page=1">')

#The soup object contains all of the HTML in the original document.
#print(soup.prettify()[0:1000000])
#print(soup.prettify()[28700:30500])


letters = soup.find_all("div", class_='"odd" data-url=')
print(type(letters))
print(letters)
lobbying = {}
for element in letters:
    lobbying[element.a.get_text()] = {}
