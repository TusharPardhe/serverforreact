#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import json


# In[2]:


pageUrl = "https://www.mohfw.gov.in/"
statesDataUrl = "https://www.mohfw.gov.in/data/datanew.json"

page = requests.get(pageUrl)
statesData = requests.get(statesDataUrl).text

soup = BeautifulSoup(page.content, "html.parser")
website_header = soup.find(id="site-dashboard")
dataset = {}


# In[3]:


def casesUpOrDown(data):
    if(data):
        if(data.find(class_="fa-arrow-down")):
            return "down"
        if(data.find(class_="fa-arrow-up")):
            return "up"
    return ""


# In[4]:


def getNumbers(data):
    if(data):
        data = data.replace(',', '')
        return re.findall(r'\d+', data)
    return 0


# In[5]:


def getTotalCasesObject(data):
    # check whether li tag exists
    if(data):
        data = data.find_all("strong", class_="mob-hide")
        if(data[1]):
            data = data[1]

    # check whether strong tag exists
    if(data):
        arr = getNumbers(data.text)
        arr.append(casesUpOrDown(data))
        return {
            "cases": arr[0],
            "change": arr[1],
            "direction": arr[2]
        }

    return ""


# In[6]:


total_active_cases = getTotalCasesObject(
    website_header.find("li", class_="bg-blue"))
total_discharged = getTotalCasesObject(
    website_header.find("li", class_="bg-green"))
total_death_cases = getTotalCasesObject(
    website_header.find("li", class_="bg-red"))

dataset["activeCases"] = total_active_cases
dataset["dischargedCases"] = total_discharged
dataset["deathCases"] = total_death_cases


# In[7]:


total_vaccinated = getNumbers(website_header.find(class_="coviddata").text)[0]
vacc_number = getNumbers(website_header.find(class_="coviddataval").text)[0]
up_or_down = casesUpOrDown(website_header.find(class_="coviddataval"))

dataset["vaccinationDetails"] = {
    "total": total_vaccinated, "change": vacc_number, "direction": up_or_down}


# In[8]:


dataset["statesData"] = json.loads(statesData)
dataset["statesData"][len(dataset["statesData"]) - 1]["state_name"] = "Total"


# In[9]:


jsonData = json.dumps(dataset, sort_keys=False, indent=4)


# In[10]:


# write json data to file
with open("../vaccineData.json", "w") as outfile:
    outfile.write(jsonData)


# In[ ]:
print("Completed")
