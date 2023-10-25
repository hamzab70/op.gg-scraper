import requests
import time
import datetime

#https://developer.riotgames.com/
#https://developer.riotgames.com/apis#match-v5/GET_getMatch

region = "na1"
mass_region = "americas"
api_key = ""

players = [{"name": "Devon","account": "Hdannihilator"},
		   {"name": "Alex M","account":"Crusading Dino"}, 
		   {"name": "Lamont","account":"Arri"},
		   {"name": "Grayson","account":"xGreySwag"},
		   {"name": "Alberto","account":"Defaults01"},
		   {"name": "Matthhew","account":"DryEyesWhiteDrag"},
		   {"name": "Ethan","account":"MAgicdragon0987"},
		   {"name": "Alex G","account":"AlexGdawg"},
           {"name": "Jacob", "account": "Velmas Dumptruck"}]

# Gets the puuid, given a summoner name and region
def get_puuid(summoner_name, region):
    api_url = (
        "https://" + 
        region +
        ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        summoner_name +
        "?api_key=" +
        api_key
    )
    
    resp = requests.get(api_url)
    
    player_info = resp.json()
    print(player_info)
    puuid = player_info['puuid']
    return puuid  


# Gets a list of all the match IDs given a players puuid and mass region
def get_match_ids(puuid, mass_region, api_key):
    api_url = (
        "https://" +
        mass_region +
        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        puuid + 
        "/ids?queue=420&start=0&count=20" + 
        "&api_key=" + 
        api_key
    )
        
    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids      


# Gets the match data given a match_id and region
def get_match_data(match_id, mass_region):
    api_url = (
        "https://" + 
        mass_region + 
        ".api.riotgames.com/lol/match/v5/matches/" +
        match_id + 
        "?api_key=" + 
        api_key
    )
    
    # Makes sure we get match data if we go over api call limits
    while True:
        resp = requests.get(api_url)
        
        # If we go over rate limit, we sleep for 10 seconds and then restart from the top of the "while" loop
        if resp.status_code == 429:
            print("Rate Limit hit, sleeping for 10 seconds")
            time.sleep(10)
            continue

        match_data = resp.json()
        return match_data      


# Given the match data and a players puuid, return the data about just them
def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    return player_data


# Takes in a unix timestamp and converts to month and day
def timestamp_to_datetime(timestamp):
    dtobj = datetime.datetime.fromtimestamp(timestamp)
    formatted = dtobj.strftime('%m-%d')
    return formatted


# Gets the name of the champion the given player was playing against in the given match
def get_opposing_champ(match_id, player_ign, our_role):
    data = []
    match_data = get_match_data(match_id, mass_region, api_key)
    this_players_puuid = get_puuid(player_ign, region, api_key)
    participant_puuids = match_data['metadata']['participants']
    for puuid in participant_puuids:
        pd = find_player_data(match_data, puuid)

        if puuid != this_players_puuid and pd['teamPosition'] == our_role:
            matchup = pd['championName']
            return matchup
        

# Calls all other functions to get all of a player's data given their ign
def getPlayerData(player_ign):
    data = []
    puuid = get_puuid(player_ign, region, api_key)
    match_ids = get_match_ids(puuid, mass_region, api_key)
    for id in match_ids:
        match_data = get_match_data(id, mass_region, api_key)
        player_match_data = find_player_data(match_data, puuid)

        game_created = timestamp_to_datetime(int(str(match_data['info']['gameCreation'])[:-3]))
        gold_earned = player_match_data['goldEarned']
        champ_played = player_match_data['championName']
        kills = player_match_data['kills']
        deaths = player_match_data['deaths']
        assists = player_match_data['assists']
        wards_bought = player_match_data['visionWardsBoughtInGame']
        minions_killed = player_match_data['totalMinionsKilled']
        cs_min = round((minions_killed / mins),2)

        result = 'Win' if player_match_data['win'] == True else 'Loss'

        seconds = match_data['info']['gameDuration']
        mins = seconds // 60
        seconds %= 60
        game_duration = str(mins) + 'm ' + str(seconds) +'s'

        role = player_match_data['teamPosition']
        matchup = get_opposing_champ(id, player_ign, role)

        kda_string = ' ' + str(kills) + '/' + str(deaths) + '/' + str(assists)
        
        if deaths == 0:
            ratio = kills + assists
        else:
            ratio = round(((kills + assists) / deaths), 2)
        
        ratio_string = str(ratio) + ':1'

	    # fields = ['Game #', 'Date Played', 'Length', 'Result', 'Champion', 'Matchup', 'KDA', 'KDA Ratio', 'Kill Participation', 'CS', 'CS/min', 'Gold Earned', 'Control Wards Bought', 'Average Rank']
        data.append(['#', game_created, game_duration, result, champ_played, matchup, kda_string, ratio_string, 'kp', minions_killed, cs_min, gold_earned, wards_bought, 'avg rank'])
    return data


get_puuid("EnDoubleU", region)