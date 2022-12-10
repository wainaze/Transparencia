from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import *
import re
import ssl
import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
#function to parse a website from a url and find the links that contain the content about transparency.

disable_warnings(InsecureRequestWarning)

def transp_url(url):
    #hearders because some pages return 403 error
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    #globalise variable a to make the return accessible inside all function
    global a
    #SSL certificate error with some pages, thus adding this:
    ssl._create_default_https_context = ssl._create_unverified_context

    #make sure the URL is valid otherwise and if exception return website error
    try:
        response = requests.get(url, timeout=10,verify=False)
        req = Request(url, headers=hdr)
        html_page = urlopen(req)

        #find one href link URL that contains "transpar"
        #problem with casing doesn't recognise uper or lower.
        soup = BeautifulSoup(html_page, "lxml")
        link = soup.select_one("a[href*=transpar]")

        #if there is a link url that contains transpar return the link direclty
        if link:
            #print("link found")
            a = link['href']
            # join the URL if it's relative (not absolute link)
            a = urljoin(url, a)
            #parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            #a = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + parsed_href.params + parsed_href.query + parsed_href.fragment
            #print(href)
            #print(a)

        else:
        #get the link of the transparence page based on anchor.
        #problem with casing doesn't recognise uper or lower so need to do with upper and lowercase.
            link2 = soup.find("a", string=re.compile("Transpar"))
            if link2:
                #print("link found")
                a = link2['href']     
                # join the URL if it's relative (not absolute link)
                a = urljoin(url, a)
                #parsed_href = urlparse(href)
                # remove URL GET parameters, URL fragments, etc.
                #a = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + parsed_href.params  + parsed_href.query + parsed_href.fragment
                #print(href)
                #print(a)
            else: 
                link3 = soup.find("a", string=re.compile("transpar"))
                if link3:
                    #print("link found")
                    a = link3['href']
                    #print(a)
                    a = urljoin(url, a)
                    #parsed_href = urlparse(href)
                    # remove URL GET parameters, URL fragments, etc.
                    #a = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + parsed_href.params + parsed_href.query + parsed_href.fragment
                    #print(href)
                    #print(a)

                else:
                    #print("No Transparency page")            
                    a = "No Transparency page"
                    #print(a)

    except Exception:
        a = "Website problem"
    print(url + a)
    return (a)


#print(transp_url('https://www.arp-gan.be/fr/'))

#https://www.vivaqua.be/fr/
#https://www.vivaqua.be/fr/
#http://www.brulabo.irisnet.be/
#https://www.vivaqua.be/fr/
#http://www.cremabru.be/
#https://www.brutele.be/index-1-fr.html
#https://www.anderlecht.be/fr