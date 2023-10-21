from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys


pages = set([])
def getlinks(pageUrl):
    global pages
    html = urlopen('https://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html.read(), 'html.parser')
    
    try:
        tittle = bs.find('h1',{'id':'firstHeading'}).get_text()
        print(tittle)
        
    except AttributeError:
        print('This page is missing tittle! Continuing....')
        
    try:
        first_paragraph = bs.find('div' , {'class': 'mw-content-ltr'}).find('div' , {'class':'mw-parser-output'}).find_all('p')[2].get_text()
        print(first_paragraph)
        
    except AttributeError and IndexError:
        print('This page is missing first paragraph! Continuing....')
        
    try:
            
        edit_link = bs.find('div' , {'class': 'vector-page-toolbar-container'}).find('a' , href = re.compile('^/wiki/.*Talk.*$'))
        
        
        html_2 = urlopen('https://en.wikipedia.org{}'.format(edit_link['href']))
        bs_2 = BeautifulSoup(html_2.read(), 'html.parser')
        
        
        final_edit_link = bs_2.find('div' , {'class':'vector-page-toolbar'}).find('a' , href = re.compile('^.*index.*\.php.*$'))
        
        print('Edit link: ','https://en.wikipedia.org{}'.format(final_edit_link['href']) , '\n')
        
    except AttributeError:
        print('This page is missing edit link! Continuing....')
        
    try:
        links = bs.find('div', {'id':'bodyContent'}).find_all('a' , href = re.compile('^(/wiki/)((?!:).)*$'))
            
        specific_link = links[3]
        
    except IndexError:
        
        print("No link at the given index to continue")
        
        sys.exit()
        
        
    if 'href' in specific_link.attrs:
        newPage = specific_link.attrs['href']
        if newPage not in pages:
                
            print('Link of the new page: ','https://en.wikipedia.org{}'.format(newPage))
            pages.add(newPage)
            getlinks(newPage)

path = str(input('Enter the path of the wikipedia link: '))
                
getlinks(path)

