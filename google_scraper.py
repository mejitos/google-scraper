"""
Simple webscraping tool which:
- takes one string (without whitespaces) as a argument,
- does a google search with given argument, 
- scrapes the url of the ten first search results,
- scrapes all paragraphs which contains the given argument from each of the given websites, and
- saves the data to a text file
"""


__version__ = '0.1'
__author__ = 'Timo Mehto'


import sys
import os
import requests
from bs4 import BeautifulSoup


# Info for saving the file
file_name = 'scraped-text.txt'
file_path = os.path.expanduser('~/Desktop')
full_path = os.path.join(file_path, file_name)

def main(arg):
    """
    Main function of the script

    :param arg: Argument passed by user
    :returns: None
    """

    print("Scraping the webs....")

    # Making Google search with the given argument
    search = arg
    google_query = f'https://www.google.com/search?q={search}'
    response = requests.get(google_query).text
    parser = 'lxml'
    soup = BeautifulSoup(response, parser)
    parsed_urls = []

    # Scraping the URLs from the search results
    urls = soup.find_all('h3', class_='r')

    for url in urls:
        parsed_url = url.find('a')['href'].replace('/url?q=', '').split('&')[0]
        parsed_urls.append(parsed_url)

    # Scraping data from the URLs and saving it to .txt file
    for url in parsed_urls:
        response = requests.get(url).text
        parser = 'lxml'
        soup = BeautifulSoup(response, parser)
        text = soup.find_all('p')
        
        with open(full_path, 'a', encoding='utf-8') as f:
            for t in text:
                if t.text.lower().find(search) >= 0:
                    f.write(t.text)
                    f.write('\n')
                    f.write(url)
                    f.write('\n')
                    f.write('~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~')
                    f.write('\n')
    
    print("Scraping completed and the result file is saved to your desktop")


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        main(sys.argv[1])
    else:
        print("You didn't pass an argument for the script")
        print()
        print("Use command 'python {filename}.py {argument}' where:")
        print("\tfilename = name of your Python script")
        print("\targument = keyword for your Google scraping ")