import requests
import time
import datetime

#https://developer.riotgames.com/

region = "na1"
mass_region = "americas"
api_key = "RGAPI-4f0993f5-901f-4cf7-abe1-9b3cae615c07"

# Gets the puuid, given a summoner name and region
def get_puuid(summoner_name, region, tag):
    api_url = (
        "https://" + 
        mass_region +
        ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/" +
        summoner_name + "/" +
        tag + 
        "?api_key=" +
        api_key
    )

    resp = requests.get(api_url)

    player_info = resp.json()
    print(player_info)
    puuid = player_info['puuid']
    return puuid  


# Gets a list of all the match IDs given a players puuid and mass region
def get_match_ids(puuid, mass_region):
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
def get_opposing_champ(match_id, player_ign, our_role, tag):
    data = []
    match_data = get_match_data(match_id, mass_region)
    this_players_puuid = get_puuid(player_ign, region, tag)
    participant_puuids = match_data['metadata']['participants']
    for puuid in participant_puuids:
        pd = find_player_data(match_data, puuid)

        if puuid != this_players_puuid and pd['teamPosition'] == our_role:
            matchup = pd['championName']
            return matchup


# Calls all other functions to get all of a player's data given their ign
def getPlayerData(player_ign, tag):
    data = []
    puuid = get_puuid(player_ign, region, tag)
    match_ids = get_match_ids(puuid, mass_region)


#(["Averages:", "N/A", "N/A", "Winrate: " + str(avg_results), "N/A", "N/A", "N/A", avg_kda_ratio, avg_kp, avg_cs, avg_csmin, avg_goldearned, avg_goldmin, avg_wards, avg_vision_score])

    sum_wins = 0
    sum_kda_ratio = 0
    sum_cs = 0
    sum_csmin = 0
    sum_goldearned = 0
    sum_goldmin = 0
    sum_wards = 0
    sum_visionscore = 0
    sum_kp = 0

    for id in match_ids:
        match_data = get_match_data(id, mass_region)
        player_match_data = find_player_data(match_data, puuid)

        game_created = timestamp_to_datetime(int(str(match_data['info']['gameCreation'])[:-3]))
        gold_earned = player_match_data['goldEarned']
        sum_goldearned += gold_earned
        champ_played = player_match_data['championName']
        kills = player_match_data['kills']
        deaths = player_match_data['deaths']
        assists = player_match_data['assists']
        wards_bought = player_match_data['visionWardsBoughtInGame']
        sum_wards += wards_bought
        vision_score = player_match_data['visionScore']
        sum_visionscore += vision_score

        minions_killed = player_match_data['totalMinionsKilled']
        sum_cs += minions_killed

        result = 'Win' if player_match_data['win'] == True else 'Loss'
        if result == 'Win':
            sum_wins += 1

        seconds = match_data['info']['gameDuration']
        mins = seconds // 60
        seconds %= 60
        game_duration = str(mins) + 'm ' + str(seconds) +'s'

        cs_min = round((minions_killed / mins),2)
        sum_csmin += cs_min
        gold_min = round(gold_earned/mins)
        sum_goldmin += gold_min
        role = player_match_data['teamPosition']
        matchup = get_opposing_champ(id, player_ign, role, tag)

        kda_string = ' ' + str(kills) + '/' + str(deaths) + '/' + str(assists)
        
        if deaths == 0:
            ratio = kills + assists
        else:
            ratio = round(((kills + assists) / deaths), 2)
        
        sum_kda_ratio += ratio
        ratio_string = str(ratio) + ':1'

        participant_puuids = match_data['metadata']['participants']
        kp = getKp(id, puuid, kills + assists, participant_puuids)
        sum_kp += float(kp[:-1])
	    # fields = ['Game #', 'Date Played', 'Length', 'Result', 'Champion', 'Matchup', 'KDA', 'KDA Ratio', 'Kill Participation', 'CS', 'CS/min', 'Gold Earned', 'Gold/Min', 'Control Wards Bought', 'Vision Score']
        data.append(['#', game_created, game_duration, result, champ_played, matchup, kda_string, ratio_string, kp, minions_killed, cs_min, gold_earned, gold_min, wards_bought, vision_score])
    


    data.append(["Averages:", "N/A", "N/A", "Winrate: " + str(round(sum_wins / 20,1)), "N/A", "N/A", "N/A", round(sum_kda_ratio/20,1),round(sum_kp/20,1),round(sum_cs/20,1),round(sum_csmin / 20,1), round(sum_goldearned / 20,1), round(sum_goldmin/20,1), round(sum_wards/20,1), round(sum_visionscore/20,1)])
    return data


# Gets a players IGN from their PUUID
def getIGNfromPuuid(puuid):

    api_url = (
        "https://" + 
        region + 
        ".api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" +
        puuid + 
        "?api_key=" + 
        api_key
    )
        

    resp = requests.get(api_url)
    ign = resp.json()
    return ign['name']  
   
    
# Returns the percent of the teams kills the given player (puuid) participated in during the given game (match_id)
def getKp(match_id, puuid, participation, participants):
        
    match_data = get_match_data(match_id, mass_region)
    participant_puuids = match_data['metadata']['participants']

    blue_team = participant_puuids[:5]
    red_team = participant_puuids[5:]
    
    team = blue_team if puuid in blue_team else red_team
    total_kills = 0

    for id in team:
        player_match_data = find_player_data(match_data, id)
        total_kills += player_match_data['kills'] 

    kp = str(round(((participation / max(total_kills,1)) * 100))) + '%'
    return kp

# getPlayerData("EnDoubleU")