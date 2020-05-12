import functools
from requests_html import HTMLSession
from bs4 import *
from operator import itemgetter
from tabulate import tabulate
 
#### VARIABLES ####
players_num = 12
players = [{"name": "Eric","cuenta": "Blackbird+SR71"},{"name": "Nino","cuenta":"TROPHY+WINNER"},{"name": "Igna","cuenta": "MarthaeSoSo"},{"name": "Miguel","cuenta": "El+Pinche+Joto"},{"name": "Hamza","cuenta": "Kerry+Co+Boalak"},{"name": "Bastardas","cuenta": "r+u+fine"},{"name": "Pol","cuenta": "Topacio+Tenorio"},{"name": "Shaggy","cuenta": "LC+Spanish+Uzi"},{"name": "Ivan","cuenta": "MC+Vergote"},{"name": "Guaye","cuenta": "RobertazpeLkN"},{"name": "Parejo","cuenta": "RITOPLSDONTBAN"},{"name": "Sergi","cuenta": "Papingo+Ibaka"}]
ranks = ["Challenger","Grandmaster","Master","Diamond 1","Diamond 2","Diamond 3","Diamond 4","Platinum 1","Platinum 2","Platinum 3","Platinum 4","Gold 1","Gold 2","Gold 3","Gold 4","Silver 1","Silver 2","Silver 3","Silver 4","Bronze 1","Bronze 2","Bronze 3","Bronze 4","Iron 1","Iron 2","Iron 3", "Iron 4","Unranked"]
place = list(range(1,players_num+1))
printable_list = []

print("```# ----------------------- SOLOQ CHALLENGE 2020 LaC0lla & Co Edition ----------------------- #")

session = HTMLSession()

for name in players:
	
	player = name["name"]
	name = name["cuenta"]

	page = 'https://euw.op.gg/summoner/userName=' + name
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
		liga = rank
	else:
		liga = "Unranked"

	if wins is not None:
		games = wins+losses

	name = name.replace("+"," ")

	printable_list.append({"player": player ,"name": name, "liga": liga, "LP": LP, "games": games, "wins": wins, "losses": losses, "winratio": winratio})

def sort(a,b):
	if a["liga"] == b["liga"]:
		if int(a["LP"].split(" ")[0]) > int(b["LP"].split(" ")[0]): 
			return -1
		if int(a["LP"].split(" ")[0]) < int(b["LP"].split(" ")[0]):
			return 1
		if int(a["winratio"].split("%")[0]) > int(b["winratio"].split("%")[0]):
			return -1
		else:
			return 1
		else:
			if a["wins"] > b["wins"]:
				return -1
			else:
				return 1	
	else:
		if ranks.index(a["liga"]) > ranks.index(b["liga"]):
			return 1
		else:
			return -1

cmp = functools.cmp_to_key(sort)
printable_list.sort(key=cmp)

print(tabulate([elem.values() for elem in printable_list], headers=['Pos','Nombre', 'Cuenta', 'Elo', 'LP', 'Partidas', 'Wins', "Losses", "Winrate"], showindex=place, tablefmt="rst", numalign="right", stralign="left"))
print("```") 