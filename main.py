import requests
from bs4 import BeautifulSoup, element
from bs4 import SoupStrainer

req = requests.get('http://consequenceofsound.net/upcoming-releases/')

soup = BeautifulSoup(req.text, 'html.parser')

sub = SoupStrainer(id='album-thumbnail')
for sibs in soup.find_next_siblings('album-thumbnail'):
    print(sibs)

# pretty = soup.prettify().encode('UTF-8')
albums = soup.find(id='main-content')

for e in albums:
    print('-'*10)
    if e.name == 'div':
        for child in e.children:
            print ('NAME:',child.contents)
            print(child)
            if isinstance(child, element.NavigableString):
                print ('YES')
                print(child.string)
        #print (type(element))
    print('-' * 10)

# rint(m.prettify())#.encode('UTF-8'))

# <h1 class='post-title'>Upcoming Releases</h1>
