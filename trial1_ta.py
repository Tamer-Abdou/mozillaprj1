#We begin by reading in the source code for a given web page and creating a Beautiful Soup object with the BeautifulSoup function.
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


req = Request('http://www.cmegroup.com/trading/products/#sortField=oi&sortAsc=false&venues=3&page=1&cleared=1&group=1', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

#r = urllib.request.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
soup = BeautifulSoup(webpage)
print(type(soup))
             #'"https://reviewboard.mozilla.org/r/?sort=review_id&datagrid-id=datagrid-0&columns=review_id&show-closed=1&page=1">')

#The soup object contains all of the HTML in the original document.
print(soup.prettify()[0:1000])
print(soup.prettify()[28700:30500])


letters = soup.find_all("div", class_="cmeEqualHeightRow")
print(type(letters))

letters[0]