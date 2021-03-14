"""
refernce:
https://github.com/WillKoehrsen/wikipedia-data-science/blob/master/notebooks/Downloading%20and%20Parsing%20Wikipedia%20Articles.ipynb
"""

import requests
import urllib
# Parsing HTML
from bs4 import BeautifulSoup
import os
import sys


def download_wiki(base_url='https://dumps.wikimedia.org/enwiki/'):
    index = requests.get(base_url).text
    soup_index = BeautifulSoup(index, 'html.parser')
    # Find the links that are dates of dumps
    dumps = [a['href'] for a in soup_index.find_all('a') if
             a.has_attr('href')]
    print(dumps)
    dump_url = base_url + '20210301/'
    # Retrieve the html
    dump_html = requests.get(dump_url).text
    print(dump_html[:50])
    # Convert to a soup
    soup_dump = BeautifulSoup(dump_html, 'html.parser')
    # Find li elements with the class file
    soup_dump.find_all('li', {'class': 'file'}, limit=10)[:4]
    files = []
    # Search through all files
    for file in soup_dump.find_all('li', {'class': 'file'}):
        text = file.text
        # Select the relevant files
        if 'pages-articles' in text:
            files.append((text.split()[0], text.split()[1:]))
    print(files[:5])
    files_to_download = [file[0] for file in files if '.xml-p' in file[0]]
    print(files_to_download[-5:])
    file_home = '/home/zglg/SLU/psd/corpus/'
    data_paths = []
    file_info = []
    # Iterate through each file
    for file in files_to_download:
        path = file_home + file
        # Check to see if the path exists (if the file is already downloaded)
        if not os.path.exists(file_home + file):
            print('Downloading')
            data_paths.append(urllib.request.urlretrieve(dump_url + '/' + file, filename=file))
            # Find the file size in MB
            file_size = os.stat(path).st_size / 1e6
            # Find the number of articles
            file_articles = int(file.split('p')[-1].split('.')[-2]) - int(file.split('p')[-2])
            file_info.append((file, file_size, file_articles))
