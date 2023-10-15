import functools
from requests_html import HTMLSession
from bs4 import *
from tabulate import tabulate
import pprint

############################ VARIABLES ########################################
server = "na"
players = [{"name": "Devon","account": "Hdannihilator"},
		   {"name": "Alex G","account":"Crusading Dino"}, 
		   {"name": "Lamont","account":"Arri"},
		   {"name": "Grayson","account":"xGreySwag"},
		   {"name": "Alberto","account":"Defaults01"},
		   {"name": "Matthew","account":"DryEyesWhiteDrag"},
		   {"name": "Ethan","account":"MAgicdragon0987"},
		   {"name": "Alex M","account":"AlexGdawg"}]
################################################################################
ranks = ["challenger","grandmaster","master",
		 "diamond1","diamond2","diamond3","diamond4",
		 "emerald1","emerald2","emerald3","emerald4",
		 "platinum1","platinum2","platinum3","platinum4",
		 "gold1","gold2","gold3","gold4",
		 "silver1","silver2","silver3","silver4",
		 "bronze1","bronze2","bronze3","bronze4",
		 "iron1","iron2","iron3", "iron4",
		 "unranked"]


printable_list = []

session = HTMLSession()

for name in players:

	page = 'https://' + server + '.op.gg/summoner/userName=' + name["account"].replace(" ","+")
	html = session.get(page)
	soup = BeautifulSoup(html.content, 'html.parser')


	htmll = soup.prettify()  #bs is your BeautifulSoup object


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

def sort(a,b):
	if a["league"] == b["league"]:
		# if int(a["LP"].split(" ")[0]) > int(b["LP"].split(" ")[0]):
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
