import functools
from requests_html import HTMLSession
from bs4 import *
from tabulate import tabulate

import time
import csv
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

############################ VARIABLES ########################################
server = "na"
players = [{"name": "Devon","account": "Hdannihilator"},
		   {"name": "Alex M","account":"Crusading Dino"}, 
		   {"name": "Lamont","account":"Arri"},
		   {"name": "Grayson","account":"xGreySwag"},
		   {"name": "Alberto","account":"Defaults01"},
		   {"name": "Matthhew","account":"DryEyesWhiteDrag"},
		   {"name": "Ethan","account":"MAgicdragon0987"},
		   {"name": "Alex G","account":"AlexGdawg"},
           {"name": "Jacob", "account": "Velmas Dumptruck"}]

ranks = ["challenger","grandmaster","master",
		 "diamond1","diamond2","diamond3","diamond4",
		 "emerald1","emerald2","emerald3","emerald4",
		 "platinum1","platinum2","platinum3","platinum4",
		 "gold1","gold2","gold3","gold4",
		 "silver1","silver2","silver3","silver4",
		 "bronze1","bronze2","bronze3","bronze4",
		 "iron1","iron2","iron3", "iron4",
		 "unranked"]

chromedriver_path = "chromedriver"

################################################################################


def main(player_ign):

	options = Options()
	# Uncomment to not have it open a browser when you run
	options.add_argument('--headless')
	options.add_argument('--log-level=3')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

	# Go to page 
	url = 'https://' + server + '.op.gg/summoner/userName=' + player_ign.replace(" ","+")
	driver.get(url)
	time.sleep(3)

	# Click the update button to get most recent games
	try:
		updateButton = driver.find_element(By.CSS_SELECTOR, '#content-header > div.css-24wmel.ebkoxbx0 > div > div.header-profile-info > div.info > div.buttons > button.css-1ki6o6m.e18vylim0')
		updateButton.click()
		time.sleep(10)
	except:
		pass

	# Filter by ranked solo games
	ranked_solo_button = driver.find_element(By.CSS_SELECTOR, '#content-container > div.css-1s9fubg.e1jlljr10 > div.css-inknuf.e1htfwqw0 > ul > li:nth-child(2) > button')
	ranked_solo_button.click()
	time.sleep(3)

	preclicked_page = driver.page_source

	# Expand most recent 20 games for access to in depth game info
	for i in range(1,21):
		expand_button = driver.find_element(By.CSS_SELECTOR , '#content-container > div.css-1s9fubg.e1jlljr10 > div.css-164r41r.e17ux5u10 > li:nth-child(' + str(i) + ') > div > div.action > button')
		driver.execute_script("arguments[0].click();", expand_button)
		time.sleep(3)

	# Get the whole page's html
	page = driver.page_source

	# Stop chromedriver
	driver.quit()
	
	# Now unused, potentially useful later
	preclicked_soup = BeautifulSoup(preclicked_page, 'html.parser')

	# BS html parser object
	soup = BeautifulSoup(page, 'html.parser')
	
	# Lists of kill participation percents and average ranks for the past 20 games
	kps = [x.getText(strip=True)[7:] for x in soup.findAll('div', attrs={'class': 'p-kill'})]
	avg_ranks = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'average-tier'})]

	# print("KPs: ", kps, "[",len(kps), "]")
	# print("Average Rank: ", avg_ranks, "[", len(avg_ranks), "]")

	new_array= []
	for i in range(len(kps)):
		new_array.append([kps[i],avg_ranks[i]])
	
	return new_array


if __name__ == "__main__":
	main("Arri")