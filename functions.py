"""A collection of function for doing my project."""
#imports
import requests
from bs4 import BeautifulSoup

import pandas as pd

from collections import Counter

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt

import os.path

import csv

import numpy as np


def web_scrape(self):

    """
    Collect data from the input URL.
    Print out page title, and return school name, progam language and program type.
    
    References：
    https://github.com/SCALESD/workshop-4-datawrangling
    """

    # Request the page 
    page = requests.get(self.url, verify = False)

    # Parse the page, with BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the title of the page
    title_page = soup.title.string

    # Translate the title from Japanese into English
    engtitle= title_page.replace("早稲田大学 留学センター","Waseda University Center for international education")[12:]
    print("page title in Japanese" + ":" +title_page[12:])
    print("page title in English" + ":" +engtitle)
        
    # Collect each program name, program language and program type. 
    self.containers = soup.findAll("div", {"class": "cie-list-table push-double-bottom"})
     
    self.school_name = []
    self.program_language = []
    self.program_type = []
  
    # Append elements to lists.
    for container in self.containers:
        target_list = [str(i) for i in container.div.dl.dd.small.text.split(',')]
        self.school_name.append(target_list[1])
        self.program_language.append(target_list[-1])
        self.program_type.append(target_list[-2])
    
    return(self.school_name,self.program_language,self.program_type)


def writecsv(self):

    """
    Store data in a csv file.
    """

    # Add data to "exchange programs.csv" if the file has already existed, and if not, create a new file.
    if os.path.isfile("exchange programs.csv"):
        f = open("exchange programs.csv","a")
        
        i = 0
        while i < len(self.containers):
            f.write(self.school_name[i] + "," + self.program_language[i] + "," + self.program_type[i] + "\n")
            i += 1
    else:
        filename = "exchange programs.csv"
        f = open(filename,"w")
        headers = "school name, program language, program type\n"
        f.write(headers)
        
        i = 0
        while i < len(self.containers):
            f.write(self.school_name[i] + "," + self.program_language[i] + "," + self.program_type[i] + "\n")
            i += 1
             
    f.close()

            
def scicom(self):

    """
    Load elements of each page into dataframe.
    Count elements.
    """

    # Load data into DataFrame.
    d1 = {'school name' : self.school_name,  
        'program language': self.program_language,
        'program type' : self.program_type}
    df = pd.DataFrame(d1)
    
    # Count elements.
    lan = Counter(self.program_language)
    prty = Counter(self.program_type)
    print(df,"\n\n\n", prty,"\n",lan,"\n")
    
    
def readcsv(self):

    """
    Load the whole csv file and make bar charts for language prevalence and program type.
    
    Codes for making bar chat came from here:
    https://stackoverflow.com/questions/19198920/using-counter-in-python-to-build-histogram
    """

    # Load the whole csv file.
    df = pd.read_csv('exchange programs.csv', sep=',')
    print("           " + 'Waseda University -- exchange programs\n')
    a = df.values
    
    # Take languages as labels and then make a bar chart.
    labels, values = zip(*Counter(a[:,1]).items())
    indexes = np.arange(len(labels))
    width = 1
    plt.bar(indexes, values, width = 0.7)
    plt.xticks(indexes + width * 0.1, labels)
    plt.show()
    print("           " + "The number of exchange programs by language")
    
     # Take program types as labels and then make a bar chart.
    labels, values = zip(*Counter(a[:,2]).items())
    indexes = np.arange(len(labels))
    width = 1
    plt.bar(indexes, values, width = 0.5)
    plt.xticks(indexes + width * 0.04, labels)
    plt.show()
    print("           "+ "The number of exchange programs by program type")
    
   
    
   