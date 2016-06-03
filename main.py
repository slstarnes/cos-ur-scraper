import requests
from bs4 import BeautifulSoup
from IPython.display import display
import re
import pandas as pd
import os
import datetime as dt

req = requests.get('http://consequenceofsound.net/upcoming-releases/')
soup = BeautifulSoup(req.text, 'html.parser')

class Album():
    def __init__(self, date, artist, album_title):
        self.date = date
        self.artist = artist
        self.album_title = album_title
    def __str__(self):
        return '%s - %s (%s)'%(self.artist, self.album_title, self.date)

def strip_non_ascii(string):
    ''' Returns the string without non-ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def date_cleaner(date):
    return re.sub(r'\({1}.*\){1}','',date).strip()


albums = []
article = soup.find(id="main-content")
for e1 in article.find_all('section', class_ = 'results-chunk'):
    for e2 in e1.find_all('h2'):
        date = date_cleaner(e2.text)
        for e3 in e1.find_all('span', class_ = 'title'):
            s = e3.text.replace(u'\u2013','-')
            s = s.replace(u'\xa0',' ')
            if s == "Fitz and the Tantrums: Fitz and the Tantrums":
                s = s.replace(": "," - ")
            s = s.split(" - ")
            if len(s) == 2:
                artist = strip_non_ascii(s[0])
                album_title = strip_non_ascii(s[1])
            else:
                artist = strip_non_ascii(str(s))
                album_title = ""
                print ("issue with: " + str(s))
            albums.append(Album(date,artist,album_title))

if os.path.exists('albums.csv'):
    old_albums_df = pd.read_csv('albums.csv')
else:
    old_albums_df = pd.DataFrame()

prev_size = len(old_albums_df)

albums_df = pd.DataFrame()
for i, a in enumerate(albums):
    albums_df.at[i, 'Artist'] = a.artist
    albums_df.at[i, 'Title'] = a.album_title
    albums_df.at[i, 'Date'] = a.date

albums_df = pd.concat([old_albums_df,albums_df])
albums_df.drop_duplicates(subset = ['Artist','Title'],inplace=True)
albums_df['Date'] = albums_df['Date'].apply(lambda x:
                                            dt.datetime.strptime(x,"%B %d, %Y"))
albums_df.sort_values(['Date','Artist','Title'],inplace=True)
albums_df['Date'] = albums_df['Date'].apply(lambda x:
                                            x.strftime("%B %d, %Y"))

print("Number of rows added: %i"%(prev_size - len(albums_df)))

albums_df.to_csv('albums.csv',index=False)
