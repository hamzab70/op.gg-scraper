# op.gg Scraper

Web scrapper that uses op.gg and League Of Legends API to sort a list of players using the same format as https://soloqchallenge.gg/



## Requirements

You can install all the dependencies using pip3 and the requirements.txt, just execute:

```
pip3 install -r requirements.txt 
```



## Usage

Clone the repo:

```
git clone https://github.com/hamzab70/op.gg-Scraper.git
```

Open opgg.py and change the 3 variables (check example.py if you have any doubt):

* server = the accounts server
* players_num = the total number of players you want to scrape
* players = is a list of dictionaries that include the name of each player and his LOL account, so you must create a new entry for each player you want to scrape

Then you can execute the scrapper:

```
python3 opgg.py
```

and the result should be something like:

```
=====  =========  ===============  =================  =======  ======  ========  =========
  Pos  Player     Account          Elo                  Games    Wins    Losses  Winrate
=====  =========  ===============  =================  =======  ======  ========  =========
    1  Nino       TROPHY WINNER    Platinum 4 (0 LP)       70      48        22  69%
    2  Shaggy     LC Spanish Uzi   Gold 1 (2 LP)           74      41        33  55%
    3  Ivan       MC Vergote       Gold 1 (0 LP)           61      39        22  64%
    4  Miguel     El Pinche Joto   Gold 3 (56 LP)          83      49        34  59%
    5  Eric       Blackbird SR71   Silver 1 (58 LP)        70      37        33  53%
    6  Guaye      RobertazpeLkN    Silver 4 (100 LP)       48      22        26  46%
    7  Igna       MarthaeSoSo      Silver 4 (59 LP)        34      17        17  50%
    8  Parejo     RITOPLSDONTBAN   Bronze 1 (0 LP)         15       7         8  47%
    9  Sergi      Papingo Ibaka    Bronze 3 (85 LP)        16       7         9  44%
   10  Hamza      Kerry Co Boalak  Bronze 3 (3 LP)         10       4         6  40%
   11  Pol        Topacio Tenorio  Bronze 4 (86 LP)        12       4         8  33%
   12  Bastardas  r u fine         Bronze 4 (16 LP)        10       2         8  20%
=====  =========  ===============  =================  =======  ======  ========  =========
```



## Known issues

- It doesn't get along very well with unranked accounts, so if a player is unranked it just prints empty data.
- The sorting is done by sort(a,b) based in the League > LeaguePoints > Winratio > Wins, if two or more players have the same data in this four variables it just sort them by alphabetical order.