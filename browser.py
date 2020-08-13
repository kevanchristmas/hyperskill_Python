import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore

browser_history = []
tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li', 'title']

# function to read the contents of the web page
def read_contents(page_url):
    if os.path.exists(dir_path + '/' + page_url) :
        file_path = os.path.join(dir_path, page_url)
        page = open(file_path, 'r')
        print(page.read())
        page.close()
    else:
        print('Error: Incorrect URL')


# function to write the contents into a file
def write_contents(page_file, source):
    file_path = os.path.join(dir_path, page_file)
    web_page = open(file_path, 'w')
    for item in source:
        format = f'{Fore.BLUE}' if item.name == 'a' else f'{Fore.RESET}'
        text = format + item.get_text()
        web_page.write(text)
    web_page.close()


# function to save a webpage to a directory in a file
def save_page(url):
    split_url = url.split('.')
    if len(split_url) > 2:  # e.g. docs.python.org
        file_name = '.'.join(split_url[: -1])
    else:  # nytimes.com
        file_name = split_url[0]

    if 'https://' not in url:
        url = 'https://' + url

    response = request_html(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find_all(tags)

    # open the page in write mode at the specified path and write it's contents
    write_contents(file_name, result)

    # append current page to browser history
    browser_history.append(file_name)

    # print the source html of the page using bs4
    for item in result:
        format = f'{Fore.BLUE}' if item.name == 'a' else f'{Fore.RESET}'
        text = format + item.get_text()
        print(text)



# function to mimic the 'back' button of a browser
def go_back():
    # check if the stack contains at least 2 elements
    # i.e. current page & a page to return to
    if len(browser_history) > 1 :
        browser_history.pop()  # pop the current page you're on
        page_to_load = browser_history[-1]  # last in, first out

        # open the page in read mode and print the contents
        read_contents(page_to_load)


# function to request the source HTML of a requested URL
def request_html(url):
    return requests.get(url)


# ------------------ main program execution starts here ---------------------------
# command line argument (directory name)
dir_name = sys.argv[1]

root_dir = os.getcwd()
dir_path = root_dir + '/' + dir_name
if not os.path.exists(dir_path) :  # if only the directory doesn't exist already
    os.mkdir(dir_name)

while True:
    command = input()
    if '.' in command:
        save_page(command)
    elif command == 'back':
        go_back()
    else:
        if command == 'exit':
            break
        else:
            read_contents(command)
            read_contents(command)
