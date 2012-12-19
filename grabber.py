import os
import pickle

import requests
from BeautifulSoup import BeautifulSoup

def grab(letter):
    '''
    Grabs spellings from wikipedia
    '''
    url = 'http://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/%s' % letter
    html = requests.get(url).content
    soup = BeautifulSoup(html)
    bullets = soup.findAll('li')
    retval = {}
    for bullet in bullets:
        if 'plainlinks' in repr(bullet):
            values = bullet.text.split('(')
            if len(values) == 2:
                retval[values[0]] = values[1][:-1] # shave off the ) at end
    return retval

def get_spellings():
    '''
    Returns a dictionary of {false: correct} spellings
    '''
    if not os.path.exists('words.pkl'):
        retval = {}
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            print 'Getting typos - %s' % c
            retval.update(grab(c))
        print 'Dumping...'
        f = open('words.pkl', 'w')
        pickle.dump(retval, f)
        f.close()
        return retval
    else:
        f = open('words.pkl', 'r')
        retval = pickle.load(f)
        f.close()
        return retval
    
if __name__ == '__main__':
    get_spellings()
