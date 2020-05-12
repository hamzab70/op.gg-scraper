import functools
from requests_html import HTMLSession
from bs4 import *
from tabulate import tabulate

############################ VARIABLES ########################################
server = "euw"
players_num = 12
players = [{"name": "Eric","account": "Blackbird SR71"},{"name": "Nino","account":"TROPHY WINNER"},{"name": "Igna","account": "MarthaeSoSo"},
	   {"name": "Miguel","account": "El Pinche Joto"},{"name": "Hamza","account": "Kerry Co Boalak"},{"name": "Bastardas","account": "r u fine"},
	   {"name": "Pol","account": "Topacio Tenorio"},{"name": "Shaggy","account": "LC Spanish Uzi"},{"name": "Ivan","account": "MC Vergote"},
	   {"name": "Guaye","account": "RobertazpeLkN"},{"name": "Parejo","account": "RITOPLSDONTBAN"},{"name": "Sergi","account": "Papingo Ibaka"}]
################################################################################

ranks = ["Challenger","Grandmaster","Master","Diamond 1","Diamond 2","Diamond 3","Diamond 4","Platinum 1","Platinum 2","Platinum 3","Platinum 4","Gold 1","Gold 2","Gold 3","Gold 4","Silver 1","Silver 2","Silver 3","Silver 4","Bronze 1","Bronze 2","Bronze 3","Bronze 4","Iron 1","Iron 2","Iron 3", "Iron 4","Unranked"]
place = list(range(1,players_num+1))
printable_list = []

session = HTMLSession()

for name in players:

	player = name["name"]
	account = name["account"].replace(" ","+")

	page = 'https://' + server + '.op.gg/summoner/userName=' + account
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
		wins = wins.string
		wins = wins.replace("W","")
		wins = int(wins)
	else:
		wins = 0

	losses = soup.find("span", {"class": "losses"})
	if losses is not None:
		losses = losses.string
		losses = losses.replace("L","")
		losses = int(losses)
	else:
		losses = 0

	winratio = soup.find("span", {"class": "winratio"})
	if winratio is not None:
		winratio = winratio.string
		winratio = winratio.replace("Win Ratio ","")
	else:
		winratio = "0%"

	if LP is not None:
		league = rank
	else:
		league = "Unranked"

	if wins is not None:
		games = wins+losses

	name = name["account"]

	printable_list.append({"player": player ,"name": name, "league": league, "LP": LP, "games": games, "wins": wins, "losses": losses, "winratio": winratio})

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

for player in printable_list:

	player["league"] = player["league"] + ' (' + player["LP"] + ')'
	del player['LP']

print(tabulate([elem.values() for elem in printable_list], headers=['Pos','Player', 'Account', 'Elo', 'Games', 'Wins', "Losses", "Winrate"], showindex=place, tablefmt="rst", numalign="right", stralign="left"))