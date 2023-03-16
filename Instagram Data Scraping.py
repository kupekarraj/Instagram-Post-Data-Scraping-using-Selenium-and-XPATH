#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing the required libraires
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re as re
import datetime
from dateutil.relativedelta import relativedelta
from tkinter import Tk
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[ ]:


#initialise the web driver
browser = webdriver.Chrome(ChromeDriverManager().install())


# In[ ]:


#creating an empty list to append the scraped outputs
Post_Text=[]
Post_Like=[]
Post_Link=[]
media_links=[]
Post_Date=[]
i=0


# In[ ]:


#importing the input csv file
linkedIn_urls = pd.read_csv(r"/Users/rajkupekar/Desktop/Raj/Tourism_Board_LinkedIn_Accounts.csv")
tourism_urls=linkedIn_urls["LinkedIn URL"].tolist()


# In[ ]:


#looping through to fetch the particular insta page and then calculating its desired scroll length
for url in tourism_urls:
    #browser.get("https://www.instagram.com/abpfoods/?hl=en")
    browser.get(url)
    time.sleep(3)
    last_height = browser.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(4)
        
        #Check out page source code
        company_page=browser.page_source
    
        #Use Beautiful Soup to get access tags
        insta_soup=bs(company_page,'lxml')
    
        #Find the post blocks
        containers = insta_soup.find_all("div",{"class":"_aabd _aa8k _aanf"})
        print("The length of the total posts is:",len(containers))
    
        for container in range(len(containers)):
            post_link_ = containers[j].find('a', href=True)
            media_links.append(post_link_['href'])
            print(media_links)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height ==last_height:
            print("Scrolling Done")
            break
        last_height = new_height


# In[ ]:


#looping through to pull all the required information
for url in urls_listed:
    browser.get(url)
    time.sleep(9)
    
    try:
        post_text=browser.find_element(By.XPATH,"//div[@class='_a9zs']").text
        Post_Text.append(post_text)
    except:
        Post_Text.append("error")
                    
    try:
        post_likes=browser.find_element(By.XPATH,"//div[@class='_aacl _aaco _aacw _aacx _aada _aade']").text
        Post_Like.append(post_likes)
    except:
        Post_Like.append("error")

    try:
        post_date=browser.find_element(By.XPATH,"//time[@class='_aaqe']").get_attribute('datetime')
        Post_Date.append(post_date)
    except:
        Post_Date.append("error")
    
    print("Finished copy for post",i, " is the",url)
    print(post_text," ",post_likes," ", post_date)
    i=i+1


# In[ ]:


#creating a dataframe to 
data = {
    "Date Posted": Post_Date,
    "Post Text": Post_Text,
    "Post Likes": Post_Like,
}

df = pd.DataFrame(data)


# In[ ]:


#printing the top head of the dataframe
df.head(30)


# In[ ]:


#exporting the data to the local machine
df.to_csv(r'your desired path goes here', index=False)

