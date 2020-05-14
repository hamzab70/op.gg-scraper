import functools
from requests_html import HTMLSession
from bs4 import *
from tabulate import tabulate

############################ VARIABLES ########################################
server = "euw"
players = [{"name": "","account": ""},{"name": "","account":""}...]
################################################################################
ranks = ["Challenger","Grandmaster","Master","Diamond 1","Diamond 2","Diamond 3","Diamond 4","Platinum 1","Platinum 2","Platinum 3","Platinum 4","Gold 1","Gold 2","Gold 3","Gold 4","Silver 1","Silver 2","Silver 3","Silver 4","Bronze 1","Bronze 2","Bronze 3","Bronze 4","Iron 1","Iron 2","Iron 3", "Iron 4","Unranked"]
printable_list = []

session = HTMLSession()

for name in players:

	page = 'https://' + server + '.op.gg/summoner/userName=' + name["account"].replace(" ","+")
	html = session.get(page)
	soup = BeautifulSoup(html.content, 'html.parser')

	rank = soup.find("div", {"class": "TierRank"}).string.strip()

	LP = soup.find("span", {"class": "LeaguePoints"})
	if LP is not None:
		LP = LP.string.strip()
	else:
		LP = "0 LP"

	wins = soup.find("span", {"class": "wins"})
	if wins is not None:
		wins = int(wins.string.replace("W",""))
	else:
		wins = 0

	losses = soup.find("span", {"class": "losses"})
	if losses is not None:
		losses = int(losses.string.replace("L",""))
	else:
		losses = 0

	winratio = soup.find("span", {"class": "winratio"})
	if winratio is not None:
		winratio = winratio.string.replace("Win Ratio ","")
	else:
		winratio = "0%"

	if LP is not None:
		league = rank
	else:
		league = "Unranked"

	if wins is not None:
		games = wins+losses

	promo = ""
	if LP == "100 LP":
		promo = str(soup.find("ol", {"class": "SeriesResults"}))

		promow = promo.count('__spSite __spSite-156')
		promol = promo.count('__spSite __spSite-154')

		promo = str(promow) + 'W-' + str(promol) + 'L'

	printable_list.append({"pos": 0, "player": name["name"] ,"name": name["account"], "league": league, "LP": LP, "promo": promo, "games": games, "wins": wins, "losses": losses, "winratio": winratio})

def sort(a,b):
	if a["league"] == b["league"]:
		if int(a["LP"].split(" ")[0]) > int(b["LP"].split(" ")[0]):
			return -1
		elif int(a["LP"].split(" ")[0]) < int(b["LP"].split(" ")[0]):
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
