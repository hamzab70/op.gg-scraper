# op.gg Scraper

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/hamzab70) 

Web scrapper that uses op.gg anLeague Of Legends API to sort a list of players using the same format as https://soloqchallenge.gg/



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

Open opgg.py and change the variables (check example.py if you have any doubt):

* server = the accounts server (use the op.gg prefixes such as euw, br, kr, na...)
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
    1  Nino       TROPHY WINNER    Platinum 4 (0 LP)       76      49        27  64%
    2  Ivan       MC Vergote       Gold 1 (45 LP)          74      45        29  61%
    3  Miguel     El Pinche Joto   Gold 2 (0W-1L)         104      63        41  61%
    4  Shaggy     LC Spanish Uzi   Gold 2 (56 LP)          83      43        40  52%
    5  Eric       Blackbird SR71   Silver 1 (57 LP)        85      44        41  52%
    6  Igna       MarthaeSoSo      Silver 2 (0 LP)         39      21        18  54%
    7  Guaye      RobertazpeLkN    Silver 3 (23 LP)        62      29        33  47%
    8  Hamza      Kerry Co Boalak  Bronze 1 (30 LP)        16       9         7  56%
    9  Pol        Topacio Tenorio  Bronze 1 (24 LP)        22      10        12  45%
   10  Parejo     RITOPLSDONTBAN   Bronze 1 (0 LP)         15       7         8  47%
   11  Sergi      Papingo Ibaka    Bronze 3 (85 LP)        16       7         9  44%
   12  Bastardas  r u fine         Unranked                 0       0         0  0%
=====  =========  ===============  =================  =======  ======  ========  =========
```



## Known issues

- It doesn't get along very well with unranked accounts, so if a player is unranked it just prints empty data.
- The sorting is done by sort(a,b) based in the League > LeaguePoints > Winratio > Wins, if two or more players have the same data in this four variables it just sort them by alphabetical order.