import requests
from bs4 import BeautifulSoup
import sys

def fetching_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        print("Error: ",url)
        sys.exit(1)
def parsing_page(html):
    soup_ = BeautifulSoup(html,"html.parser")
    title = soup_.title.get_text(strip=True)if soup_.title else "No tittle"
    body=soup_.body.get_text(" ",strip=True)if soup_.body else ""
    links= [a["href"]for a in soup_.find_all("a",href=True)]
    return title,body,links

def word_freq(text):
    freq = {}
    word =""
    for ch in text:
        if ch.isalnum():
            word+=ch.lower()
        else:
            if word:
                freq[word] = freq.get(word,0)+1
                word = ""
    if word:
        freq[word] = freq.get(word, 0) +1
    return freq

P = 53
Mask = (1<<64)  -1

def polynomial_hash(word):
    val = 0
    power = 1
    for ch in word:
        val = (val+ord(ch)*power)&Mask
        power = (power*P) & Mask
    return val
def simhash(freq):
    vector = [0]*64
    for word, weight in freq.items():
        h = polynomial_hash(word)
        for i in range(64):
            if(h>> i) & 1:
                vector[i] += weight
            else:
                vector[i] -= weight
    result = 0
    for i in range(64):
        if vector[i] > 0:
            result |= (1 << i)
    return result

def bits_common(h1,h2):
    xor = h1^h2
    return 64 - bin(xor).count("1")

if len(sys.argv)<2:
    print("url-1 -> show page details")
    print("2 urls -> compare simhash")
    sys.exit(1)

if len(sys.argv)==2:
    html = fetching_html(sys.argv[1])
    title,body,links = parsing_page(html)
    print("Page Title: ", title)
    print("\n")
    print("Page Body: ",body)
    print("\n")
    print("Links")
    for link in links:
        print(link)
elif len(sys.argv)==3:
    html1 = fetching_html(sys.argv[1])
    html2 = fetching_html(sys.argv[2])
    body1=parsing_page(html1)
    body2 = parsing_page(html2)

    freq1 = word_freq(body1)
    freq2 = word_freq(body2)

    simhash1 = simhash(freq1)
    simhash2 = simhash(freq2)

    print("commmon bits: ", bits_common(simhash1,simhash2))