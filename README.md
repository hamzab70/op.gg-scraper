# LOLPlayerAnalysisTool

A tool that utilizes web scraping and calls to Riot Games' APIs to gather, compile, and assist in analysis of any number of league of legends accounts

Forked from: https://github.com/hamzab70/op.gg-scraper

## Requirements

You can install all the dependencies using pip3 and the requirements.txt, just execute:

```
pip3 install -r requirements.txt 
```

# Running the Script

To run the entire program, you should input your own player names and IGNs into the dictionary at the top of the program, you can then simply run dataWriter.py, then wait roughly 2 minutes per person (to be improved upon) and the files will be created in a folder in the root directory.

```
python3 dataWriter.py
```

You can run only the op.gg web scraping portion by putting the IGN of the account in the 'main' call in opggWebScraper.py (currently line 91)
```
if __name__ == "__main__":
	main("yourIGNhere")
```

```
python3 opggWebScraper.py 
```

You can run only the riot api portion by calling any function on someone's IGN and other necessary parameters in riotApi.py (currently lines 145+)
NOTE: you will have to input your own riot API key at the top where there's a variable for it. Google it if you don't know how to find it.
```
getPlayerData("yourIGNhere")
get_puuid("yourIGNhere", "na")
```

```
python3 riotApi.py 
```

## Known issues

```
Todo
```
