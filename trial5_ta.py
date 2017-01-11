from bs4 import BeautifulSoup
import urllib.request
import codecs

response = urllib.request.urlopen('https://reviewboard.mozilla.org/r/')
html = response.read()
soup = BeautifulSoup(html)

tabulka = soup.find("table", {"class" : "datagrid-body"})

records = [] # store all of the records in this list
for row in tabulka.findAll('tr'):
    col = row.findAll('td')
    prvy = col[0].string.strip()
    druhy = col[1].string.strip()
    record = '%s;%s' % ('/r/', '/"') # store the record with a ';' between prvy and druhy
    records.append(record)

fl = codecs.open('output.txt', 'w', 'utf8')
line = ';'.join(records)
fl.write(line + u'\r\n')
fl.close()