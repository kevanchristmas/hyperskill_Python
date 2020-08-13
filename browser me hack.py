import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore

browser_history = []


# function to read the contents of the web page
def read_contents(page_url):
    if os.path.exists(dir_path + '/' + page_url):
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
    for row in source.split('\n'):
        web_page.write(row + '\n')
    web_page.close()


# function to save a webpage to a directory in a file
def save_page(url):
    split_url = url.split('.')
    if len(split_url) > 2:
        file_name = '.'.join(split_url[: -1])
    else:
        file_name = split_url[0]
    print(Fore.BLUE + file_name)

    if 'https://' not in url:
        url = 'https://' + url

    page_source = request_html(url)

    # open the page in write mode at the specified path and write it's contents
    write_contents(file_name, page_source)

    # append current page to browser history
    browser_history.append(file_name)

    # print the source html of the page
    for line in page_source.split('\n'):
        print(line)


# function to mimic the 'back' button of a browser
def go_back():
    # check if the stack contains at least 2 elements
    # i.e. current page & a page to return to
    if len(browser_history) > 1:
        browser_history.pop()  # pop the current page you're on
        page_to_load = browser_history[-1]  # last in, first out

        # open the page in read mode and print the contents
        read_contents(page_to_load)


# function to request the source HTML of a requested URL (hacked with beautifulsoup by me)
def request_html(url):
    response = requests.get(url)
    html_page = response.content
    output = ''
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', ]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output


# ------------------ main program execution starts here ---------------------------
# command line argument (directory name)
dir_name = sys.argv[1]

root_dir = os.getcwd()
dir_path = root_dir + '/' + dir_name
if not os.path.exists(dir_path):  # if only the directory doesn't exist already
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
