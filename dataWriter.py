import csv
import time
import opggWebScraper
import riotApi


fields = ['Game #', 'Date Played', 'Length', 'Result', 'Champion', 'Matchup', 'KDA', 'KDA Ratio', 'Kill Participation', 'CS', 'CS/min', 'Gold Earned', 'Control Wards Bought', 'Average Rank']

players = [{"name": "Devon","account": "Hdannihilator"},
		   {"name": "Alex M","account":"Crusading Dino"}, 
		   {"name": "Lamont","account":"Arri"},
		   {"name": "Grayson","account":"xGreySwag"},
		   {"name": "Alberto","account":"Defaults01"},
		   {"name": "Matthhew","account":"DryEyesWhiteDrag"},
		   {"name": "Ethan","account":"MAgicdragon0987"},
		   {"name": "Alex G","account":"AlexGdawg"},
           {"name": "Jacob", "account": "Velmas Dumptruck"}]

# Gets one player's data from opgg and Riot's API and writes it to a file given a players name and IGN
def one_person(name, player_ign):
    try:
        opggRows = opggWebScraper.main(player_ign)
        riotapiRows = riotApi.getRemainingData(player_ign)

        # Fill in game number, kill participation, and average rank columns using the opgg data
        for i in range(len(riotapiRows)):
            row = riotapiRows[i]
            row[0] = i
            row[8] = opggRows[i][0]
            row[13] = opggRows[i][1]     

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
            opggRows = opggWebScraper.main(name['account'])
            riotapiRows = riotApi.getRemainingData(name['account'])

            # Fill in game number, kill participation, and average rank columns using the opgg data
            for i in range(len(riotapiRows)):
                row = riotapiRows[i]
                row[0] = i
                row[8] = opggRows[i][0]
                row[13] = opggRows[i][1]

            # Write data to CSV
            fileName = name['name'] + 'GameData.csv'
            with open('data/' + fileName, 'w', newline='') as file:
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

# one_person("Lamont", "Arri")
# one_person("Devin", "Hdannihilator")
# one_person("Alex M", "Crusading Dino")
# one_person("Grayson", "xGreySwag")
# one_person("Alberto", "Defaults01")
# one_person("Alex G", "AlexGdawg")
# one_person("Ethan", "MAgicdragon0987")
# one_person("Ethan", "MAgicdragon0987")           
# one_person("Jacob", "Velmas Dumptruck")
