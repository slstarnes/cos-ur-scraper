import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
req  = requests.get('http://consequenceofsound.net/upcoming-releases/')

soup = BeautifulSoup(req.text, 'html.parser')

sub = SoupStrainer(id='album-thumbnail')
for sibs in sub.find_next_siblings('album-thumbnail'):
	print(sibs)

#pretty = soup.prettify().encode('UTF-8')
m = soup.find(id='main-content')
#rint(m.prettify())#.encode('UTF-8'))

#<h1 class='post-title'>Upcoming Releases</h1>