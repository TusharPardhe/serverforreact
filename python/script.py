import requests
from bs4 import BeautifulSoup
import re
import json


pageUrl = "https://www.mohfw.gov.in/"
statesDataUrl = "https://www.mohfw.gov.in/data/datanew.json"

page = requests.get(pageUrl)
statesData = requests.get(statesDataUrl).text

soup = BeautifulSoup(page.content, "html.parser")
website_header = soup.find(id="site-dashboard")
dataset = {}


def casesUpOrDown(data):
    if(data):
        if(data.find(class_="fa-arrow-down")):
            return "down"
        if(data.find(class_="fa-arrow-up")):
            return "up"
    return ""


def getNumbers(data):
    if(data):
        data = data.replace(',', '')
        return re.findall(r'\d+', data)
    return 0


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


total_active_cases = getTotalCasesObject(
    website_header.find("li", class_="bg-blue"))
total_discharged = getTotalCasesObject(
    website_header.find("li", class_="bg-green"))
total_death_cases = getTotalCasesObject(
    website_header.find("li", class_="bg-red"))

dataset["activeCases"] = total_active_cases
dataset["dischargedCases"] = total_discharged
dataset["deathCases"] = total_death_cases


total_vaccinated = getNumbers(website_header.find(class_="coviddata").text)[0]
vacc_number = getNumbers(website_header.find(class_="coviddataval").text)[0]
up_or_down = casesUpOrDown(website_header.find(class_="coviddataval"))

dataset["vaccinationDetails"] = {
    "total": total_vaccinated, "change": vacc_number, "direction": up_or_down}

dataset["statesData"] = json.loads(statesData)
dataset["statesData"][len(dataset["statesData"]) - 1]["state_name"] = "Total"

jsonData = json.dumps(dataset, sort_keys=False, indent=4)

# write json data to file
with open("../vaccineData.json", "w") as outfile:
    outfile.write(jsonData)
