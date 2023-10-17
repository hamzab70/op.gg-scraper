import functools
from requests_html import HTMLSession
from bs4 import *
from tabulate import tabulate

import time
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
		   {"name": "Alex G","account":"AlexGdawg"}]
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

### Important Stats
#  date surveyed
#  list of most popular champions (the list of them on the left below rank) and their stats. seems like 7 max champs
#		EX: CS 39.8 (1.3) --> Average CS per game (Average CS / min) for pyke
#		EX: 2.3:1 KDA --> Average 2.3 kills+assists per death for pyke
#		EX: 8.7 / 7.4 / 8.3 --> AVerage of 8.7 kills, 7.4 deaths, 8.3 assists per game for pyke
#
#
#	past 20 games:
#		Game  | Date/Time Played |Time   | Result | Champ| Matchup|  KDA    | Ratio       | Kill parti| pnk wards | CS | CS/min | Avg rank
#		Game 1| Jan 1, 2000, 10pm|28m33s | Loss   | Pyke | Thresh | 4/12/10 | KDA: 1.17:1 |  44%      |   6		  | 32 | 1.1	| Bronze 2
#		ETC.
#
#
#	stats over those 20 games:
#		avg game time
#			avg game time (wins)
#			avg game time (loss)
#		w/l ratio
#		avg kda
#		avg kp
#		avg pink wards
#		avg cs
#		avg cs/min
#		avg avg rank
#		
###

def main():

	printable_list = []

	options = Options()
	# Uncomment to not have it open a browser when you run
	# options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(options=options)

	for name in players:

		# Go to page 
		### TEMP URL HERE ###
		url = 'https://' + server + '.op.gg/summoner/userName=AlexGdawg' #'https://' + server + '.op.gg/summoner/userName=' + name["account"].replace(" ","+")
		driver.get(url)
		time.sleep(3)


		# Filter by ranked solo games
		ranked_solo_button = driver.find_element(By.CSS_SELECTOR, '#content-container > div.css-1s9fubg.e1jlljr10 > div.css-inknuf.e1htfwqw0 > ul > li:nth-child(2) > button')
		ranked_solo_button.click()
		time.sleep(3)

		preclicked_page = driver.page_source
		# Expand most recent 20 games for access to in depth game info
		for i in range(1,21):
			expand_button = driver.find_element(By.CSS_SELECTOR , '#content-container > div.css-1s9fubg.e1jlljr10 > div.css-164r41r.e17ux5u10 > li:nth-child(' + str(i) + ') > div > div.action > button')
			driver.execute_script("arguments[0].click();", expand_button)
			# expand_button.click()
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

		ratios = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'ratio'})]

		kps = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'p-kill'})]
		pink_wards_bought = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'ward'})]
		minion_kills_and_cs_mins = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'cs'})]
		avg_ranks = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'average-tier'})]

		### FIGURE OUT HOW TO GET THESE ###
		# champs_played = soup.findAll('div', attrs={'class': '?'})
		# matchup_champs = soup.findAll('div', attrs={'class': '?'})
		###

		# Removes 2 unrelated entries
		ratios = ratios[2:]

		# Remove every other element which are blank for some reason
		pink_wards_bought = pink_wards_bought[0::2]

		# Removes the minion info from other page sources
		minion_kills_and_cs_mins = minion_kills_and_cs_mins[-20:]

		# Removes entry from the top banner
		kdas = kdas[1:]

		print("Date Surveyed: ", date.today)
		print("Lengths: ", game_lengths, "\n")
		print("Results: ", game_results, "\n")
		print("Times Played: ", times_played, "\n")

		### FIX Gets the kda from the banner above the games, and all teammates kda's from the expanded menu. FIX ###

		# just pull kdas from pre clicked version? 

		print("KDAs: ", kdas, "\n")


		print("Ratios: ", ratios, "\n")
		print("kps: ", kps, "\n")
		print("Control Wards Bought: ", pink_wards_bought, "\n")
		print("Minion Info: ", minion_kills_and_cs_mins, "\n")
		print("Average Rank: ", avg_ranks, "\n")
		

		### Testing for length 20 bc we're pulling past 20 ranked games ###
		print("Lengths: ", len(game_lengths))
		print("Results: ", len(game_results))
		print("Times Played: ", len(times_played))
		print("KDAs: ", len(kdas))
		print("Ratios: ", len(ratios))
		print("kps: ", len(kps))
		print("Control Wards Bought: ", len(pink_wards_bought))
		print("Minion Info: ", len(minion_kills_and_cs_mins))
		print("Average Rank: ", len(avg_ranks))
		###


		return

		try:
			rank = soup.find("div", {"class": "tier"}).getText(strip=True)
			
		except:
			rank = "unranked"

		LP = soup.find("div", {"class": "lp"})
		if LP is not None:
			LP = LP.getText(strip=True)
		else:
			LP = "0 LP"

		wins_losses = soup.find("div", {"class": "win-lose"})
		if wins_losses is not None:
			# wins = int(wins.getText(strip=True).replace("W",""))

			wins, losses = wins_losses.getText(strip=True).replace("W", " ").replace("L", "").split()
		else:
			wins, losses = 0, 0

		if int(wins) + int(losses) == 0:
			winratio = "0%"
		else:
			winratio = str(round((int(wins) / (int(wins) + int(losses))) * 100, 2)) + "%"
			


		if LP is not None:
			league = rank
		else:
			league = "Unranked"

		if wins is not None:
			games = int(wins)+int(losses)

		promo = ""
		if LP == "100 LP":
			promo = str(soup.find("ol", {"class": "SeriesResults"}))

			promow = promo.count('__spSite __spSite-156')
			promol = promo.count('__spSite __spSite-154')

			promo = str(promow) + 'W-' + str(promol) + 'L'

		printable_list.append({"pos": 0, "player": name["name"] ,"name": name["account"], "league": league, "LP": LP, "promo": promo, "games": games, "wins": wins, "losses": losses, "winratio": winratio})
	
	print_list(printable_list)

### SORT PLAYERS BY RANK FOR PRINTING ###
def sort(a,b):
	if a["league"] == b["league"]:
		if int(a["LP"][:-2]) > int(b["LP"][:-2]):
			return -1
		elif int(int(a["LP"][:-2])) < int(b["LP"][:-2]):
			return 1
		elif int(a["winratio"].split("%")[0]) > int(b["winratio"].split("%")[0]):
			return -1
		else:
			if a["wins"] > b["wins"]:
				return -1
			else:
				return 1
	else:
		if ranks.index(a["league"]) > ranks.index(b["league"]):
			return 1
		else:
			return -1

### FORMAT AND PRINT LIST ###
def print_list(printable_list):

	cmp = functools.cmp_to_key(sort)
	printable_list.sort(key=cmp)

	pos = 0
	for player in printable_list:
		pos += 1
		player["pos"] = pos
		if player['LP'] == "100 LP":
			player["league"] = player["league"] + ' (' + player["promo"] + ')'
			del player['LP']
			del player['promo']
		else:
			player["league"] = player["league"] + ' (' + player["LP"] + ')'
			del player['LP']
			del player['promo']

	print(tabulate([elem.values() for elem in printable_list], headers=['Pos','Player', 'Account', 'Elo', 'Games', 'Wins', "Losses", "Winrate"], tablefmt="rst", numalign="right", stralign="left"))



if __name__ == "__main__":
	main()