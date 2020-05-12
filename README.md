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

Open opgg.py and change this 3 variables:

* server = the accounts server
* players_num = the total number of players you want to scrape
* players = is a list of dictionaries that include the name of each player and his LOL account, so you must create a new entry for each player you want to scrape

Then you can execute the scrapper:

```
python3 opgg.py
```

and the result should be something like:

```
=====  =========  ===============  ==========  ======  =======  ======  ========  =========
  Pos  Player     Account          Elo         LP        Games    Wins    Losses  Winrate
=====  =========  ===============  ==========  ======  =======  ======  ========  =========
    1  Nino       TROPHY WINNER    Platinum 4  0 LP         70      48        22  69%
    2  Ivan       MC Vergote       Gold 1      0 LP         60      39        21  65%
    3  Shaggy     LC Spanish Uzi   Gold 1      0 LP         72      40        32  56%
    4  Miguel     El Pinche Joto   Gold 3      59 LP        80      48        32  60%
    5  Eric       Blackbird SR71   Silver 1    38 LP        69      36        33  52%
    6  Guaye      RobertazpeLkN    Silver 4    100 LP       47      22        25  47%
    7  Igna       MarthaeSoSo      Silver 4    69 LP        33      17        16  52%
    8  Parejo     RITOPLSDONTBAN   Bronze 1    0 LP         15       7         8  47%
    9  Sergi      Papingo Ibaka    Bronze 3    85 LP        16       7         9  44%
   10  Hamza      Kerry Co Boalak  Bronze 3    3 LP         10       4         6  40%
   11  Pol        Topacio Tenorio  Bronze 4    86 LP        12       4         8  33%
   12  Bastardas  r u fine         Unranked    0 LP          0       0         0  0%
=====  =========  ===============  ==========  ======  =======  ======  ========  =========
```



## Known issues

- It doesn't get along very well with unranked accounts, so if a player is unranked it just prints empty data.
- The sorting is done by sort(a,b) based in the League > LeaguePoints > Winratio > Wins, if two or more players have the same data in this four variables it just sort them by alphabetical order.