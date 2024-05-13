import requests
from bs4 import BeautifulSoup
import re

def github() -> str:

    return "https://github.com/jphopk/ECON481-Homework/blob/main/ECON481-HW5-JustinHopkins.py"

def scrape_code(url: str) -> str:
    webpage = requests.get(url)

    soup = BeautifulSoup(webpage.text, 'html.parser')

    codes = []
    for codeChunk in soup.find_all('code', {'class': 'sourceCode python'}):
        code = codeChunk.get_text().strip()
        code = '\n'.join(line for line in code.split('\n') if not line.strip().startswith('%'))
        if code:
            codes.append(code)

    new_code = '\n'.join(codes)
    return new_code