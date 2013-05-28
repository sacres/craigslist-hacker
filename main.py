from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date, timedelta
import re
import sys

DAYS_TO_SEARCH = 3

def build_soup(url, times = 3):
    page = None
    for i in range(1, times):
        try:
            page = urlopen(url)
            break
        except IOError:
            continue

    if page == None:
        return False
    return BeautifulSoup(page)

def parse_posts_from_tags(tags, url, days):
    posts = []

    headers = 0
    for tag in tags:
        if tag.name == 'h4':
            headers = headers + 1
            if headers > days:
                break
        if tag.name == 'p':
            try:
                link = tag.find('span', {'class': 'pl'}).find('a')
                posts.append((link.get_text(), url + link['href']))
            except AttributeError:
                continue
    return posts

def get_posts(url, days = DAYS_TO_SEARCH):
    new_url = url + '/cpg'

    print 'searching', new_url
    soup = build_soup(new_url)
    if not soup:
        return False

    blockquote = soup.find(id='toc_rows')
    if not blockquote:
        return False

    tags = blockquote({'h4': True, 'p': True})
    return parse_posts_from_tags(tags, url, days)

def write_posts(posts, file_name):
    f1 = open(file_name, 'w')

    print >> f1, '<!DOCTYPE html><html><head><title></title><style>body {'
    print >> f1, 'font: normal small Verdana; } a { color: #333; }'
    print >> f1, 'a:visited { color: #999; }</style><body>'

    for post in posts:
        try:
            print >> f1, '<p><a href="%s">%s</a><p />' % (post[1], post[0])
        except Exception:
            continue

    print >> f1, '</body></html>'

#################################################################################

def check_url(url):
    m = re.search('(http\:\/\/[a-z]*\.craigslist\.org)$', url)
    return m != None

def extract_valid_urls(links, count = 500):
    urls = []
    i = 0
    for link in links:
        url = link.get('href')
        if url != None:
            if check_url(url):
                urls.append(url)

        i = i + 1
        if i > count:
            break

    return urls
          
def get_location_urls():
    soup = build_soup('http://craigslist.org/about/sites')
    if not soup:
        return False

    links = soup('a')
    return extract_valid_urls(links)

def check_url_for_posts(url, repeats = 3, days = DAYS_TO_SEARCH):
    print 'checking', url

    page = None
    for i in range(1, repeats):
        try:
            page = urlopen(url).read()
            break
        except Exception:
            continue

    if not page:
        return False

    for i in range(1, days):
        if page.find((date.today() - deltatime(i)).strftime('%a %b %d')) != -1:
            return True
    return False

def build_url_list(category = 'cpg'):
    urls = get_location_urls()
    return [x for x in urls if check_url_for_posts('%s/%s' % (x, category))]

if __name__ == '__main__':

    ############################################################################
    ### build a list of urls to check in the future
    ############################################################################

    if '--init' in sys.argv:
        good_file = open('good.txt', 'w')
        urls = build_url_list()
        for url in urls:
            print >> good_file, url

    ############################################################################
    ### search for posts
    ############################################################################

    elif '--search' in sys.argv:
        urls = open('good.txt').read().splitlines()
        posts = []

        for url in urls:
            posts += get_posts(url)

        write_posts(posts, 'posts.html')
