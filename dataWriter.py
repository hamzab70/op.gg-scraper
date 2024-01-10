import csv, time, riotApi, opggWebScraper

fields = ['Game #', 'Date Played', 'Length', 'Result', 'Champion', 'Matchup', 'KDA', 'KDA Ratio', 'Kill Participation', 'CS', 'CS/min', 'Gold Earned', 'Gold/Min', 'Control Wards Bought', 'Vision Score']

players = [{"name": "Devin","account": "HdFrost", "tag": "6706"},
		   {"name": "AlexM","account":"Crusading Dino", "tag": "NA1"}, 
		   {"name": "Lamont","account":"Arri", "tag": "NA1"},
		   {"name": "Greyson","account":"GreySwag", "tag": "6877"},
		   {"name": "Alberto","account":"Defaults01", "tag": "NA1"},
           {"name": "Jacob", "account": "Velmas Dumptruck", "tag": "NA1"}]

# Gets one player's data from opgg and Riot's API and writes it to a file given a players name and IGN
def one_person(name, player_ign, tag):
    try:
        # opggRows = opggWebScraper.main(player_ign)
        riotapiRows = riotApi.getPlayerData(player_ign, tag)

        # Fill in game number, kill participation, and average rank columns using the opgg data
        for i in range(len(riotapiRows)):
            row = riotapiRows[i]
            row[0] = i
  
        # Write data to CSV
        fileName = name + 'GameData.csv'
        with open('data/' + fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            writer.writerows(riotapiRows)

    except Exception as e:
        print("Error", e)
        print("Name: ", name)
        print("IGN: ", player_ign)
        return

# Gets everyone's data from opgg and Riot's API and writes them to individual files
def everyone():

    # Gets the start time when this is called
    start = time.time()

    for name in players:
        try:
            # opggRows = opggWebScraper.main(name['account'])
            riotapiRows = riotApi.getPlayerData(name['account'], name['tag'])

            # Add game numbers
            for i in range(len(riotapiRows)):
                row = riotapiRows[i]
                row[0] = i

            # Write data to CSV
            fileName = name['name'] + 'GameData.csv'
            with open('data/' + fileName, 'w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(fields)
                writer.writerows(riotapiRows)

        except Exception as e:
            print("Error", e)
            print("Name: ", name)
            print("IGN: ", name['account'])            
            continue

    # Prints the elapsed time of the program running
    print(time.time() - start)

everyone()

# one_person("Lamont", "Arri", "NA1")
# one_person("Devin", "Hdannihilator")
# one_person("Alex M", "Crusading Dino")
# one_person("Grayson", "xGreySwag")
# one_person("Alberto", "Defaults01")
# one_person("Jacob", "Velmas Dumptruck")
