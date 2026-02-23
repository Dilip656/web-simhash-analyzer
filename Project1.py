import requests
from bs4 import BeautifulSoup
import sys
import re

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

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9]+",text.lower())
def freq_map(word):
    freq_m= {}
    for w in word:
        freq_m[w] = freq_m.get(w,0)+1
    return freq_m

P = 53
Mask = (1<<64)  -1

def polynomial_hash(word):
    h = 0
    for ch in word:
        h = (h * P + ord(ch)) & Mask
    return h
def simhash(freq):
    vector = [0]*64
    for word, weight in freq.items():
        h = polynomial_hash(word)
        bit_index = 0
        temp = h
        while bit_index < 64:
            if temp & 1:
                vector[bit_index] += weight
            else:
                vector[bit_index]-= weight
            temp >>= 1
            bit_index += 1
    final_hash = 0
    for i, score in enumerate(vector):
        if score > 0:
            final_hash |= (1 << i)
    return final_hash

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
    _,body1,_=parsing_page(html1)
    _,body2,_ = parsing_page(html2)

    freq1 = freq_map(tokenize(body1))
    freq2 = freq_map(tokenize(body2))

    simhash1 = simhash(freq1)
    simhash2 = simhash(freq2)

    print("commmon bits: ", bits_common(simhash1,simhash2))