import functools
from requests_html import HTMLSession
from bs4 import *
from tabulate import tabulate

import time
import csv
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

chromedriver_path = "C:/Users/nwang/---/Programming/Python/Scripts/chromedriver"
################################################################################


def main(player_ign):

	options = Options()
	# Uncomment to not have it open a browser when you run
	options.add_argument('--headless')
	options.add_argument('--log-level=3')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(options=options)


	# Go to page 
	### TEMP URL HERE ###
	url = 'https://' + server + '.op.gg/summoner/userName=' + player_ign.replace(" ","+")
	driver.get(url)
	time.sleep(3)

	# Update games to riotAPI recency
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
	driver.quit()
	
	preclicked_soup = BeautifulSoup(preclicked_page, 'html.parser')

	soup = BeautifulSoup(page, 'html.parser')
		
	# Grab relevant game info
	game_lengths = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'length'})]

	game_results = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'result'})]
	times_played = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'time-stamp'})]

	kdas = [x.getText(strip=True) for x in preclicked_soup.findAll('div', attrs={'class': 'k-d-a'})]

	ratios = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'ratio'})][-20:]

	kps = [x.getText(strip=True)[7:] for x in soup.findAll('div', attrs={'class': 'p-kill'})]
	pink_wards_bought = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'ward'})]
	minion_kills_and_cs_mins = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'cs'})]
	avg_ranks = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'average-tier'})]

	# Removes 2 unrelated entries
	ratios = ratios[2:]

	# Remove every other element which are blank for some reason
	pink_wards_bought = pink_wards_bought[0::2]

	# Removes the minion info from other page sources
	minion_kills_and_cs_mins = minion_kills_and_cs_mins[-20:]

	# Removes entry from the top banner
	kdas = kdas[1:]
	
	###
	# print("Date Surveyed: ", date.today)
	# print("Lengths: ", game_lengths, "\n")
	# print("Results: ", game_results, "\n")
	# print("Times Played: ", times_played, "\n")
	# print("KDAs: ", kdas, "\n")
	# print("Ratios: ", ratios, "\n")
	# print("kps: ", kps, "\n")
	print("Control Wards Bought: ", pink_wards_bought, "\n")
	# print("Minion Info: ", minion_kills_and_cs_mins, "\n")
	# print("Average Rank: ", avg_ranks, "\n")
	
	# ### Testing for length 20 bc we're pulling past 20 ranked games ###
	print("Lengths: ", len(game_lengths))
	print("Results: ", len(game_results))
	print("Times Played: ", len(times_played))
	print("KDAs: ", len(kdas))
	# print("Ratios: ", len(ratios))
	print("kps: ", len(kps))
	for kp in kps:
		kp = kp[7:]
	print("Control Wards Bought: ", len(pink_wards_bought))
	print("Minion Info: ", len(minion_kills_and_cs_mins))
	print("Average Rank: ", len(avg_ranks))
	###

	new_array= []
	for i in range(len(game_lengths)):
		new_array.append([kps[i],avg_ranks[i]])
	

	return new_array

	

if __name__ == "__main__":
	main("EnDoubleU")