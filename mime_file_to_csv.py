#!/usr/bin/env python3

import os
import email
import mimetypes
from email.policy import default
from argparse import ArgumentParser
import pandas as pd 
from bs4 import BeautifulSoup 

def html_tables_to_csv(filename):
    data = [] 
    list_header = [] 
    soup = BeautifulSoup(open(filename),'html.parser') 
    header = soup.find_all("table")[0].find("tr") 
      
    for items in header: 
        try: 
            list_header.append(items.get_text()) 
        except: 
            continue
      
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:] 
      
    for element in HTML_data: 
        sub_data = [] 
        for sub_element in element: 
            try: 
                sub_data.append(sub_element.get_text()) 
            except: 
                continue
        data.append(sub_data) 
      
    dataFrame = pd.DataFrame(data = data, columns = list_header) 
       
    dataFrame.to_csv('output.csv')


def main():
    parser = ArgumentParser(description="Unpack a MIME message")
    parser.add_argument('msgfile')
    args = parser.parse_args()

    with open(args.msgfile, 'rb') as fp:
        msg = email.message_from_binary_file(fp, policy=default)

    counter = 1
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                ext = '.bin'
            filename = 'part-%02d%s' % (counter, ext)
        counter += 1
        try:
            html_tables_to_csv(filename)
        except:
            pass

if __name__ == '__main__':
    main()