import time
from bs4 import *
from tabulate import tabulate
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

############################ VARIABLES ########################################
server = "na"

ranks = {"challenger": 31,
		 "grandmaster": 30,
		 "master": 29,
		 "diamond1": 28,
		 "diamond2": 27,
		 "diamond3": 26,
		 "diamond4": 25,
		 "emerald1": 24,
		 "emerald2": 23,
		 "emerald3": 22,
		 "emerald4": 21,
		 "platinum1": 20,
		 "platinum2": 19,
		 "platinum3": 18,
		 "platinum4": 17,
		 "gold1": 16,
		 "gold2": 15,
		 "gold3": 14,
		 "gold4": 13,
		 "silver1": 12,
		 "silver2": 11,
		 "silver3": 10,
		 "silver4": 9,
		 "bronze1": 8,
		 "bronze2": 7,
		 "bronze3": 6,
		 "bronze4": 5,
		 "iron1": 4,
		 "iron2": 3,
		 "iron3": 2, 
		 "iron4": 1,
		 "unranked": 0}

chromedriver_path = "chromedriver"

################################################################################


def main(player_ign):

	options = Options()
	# Uncomment to not have it open a browser when you run
	options.add_argument('--headless')
	options.add_argument('--log-level=3')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

	# Go to page 
	url = 'https://' + server + '.op.gg/summoner/userName=' + player_ign.replace(" ","+")
	driver.get(url)
	time.sleep(3)

	# Click the update button to get most recent games
	try:
		updateButton = driver.find_element(By.CSS_SELECTOR, '#content-header > div.css-24wmel.ebkoxbx0 > div > div.header-profile-info > div.info > div.buttons > button.css-1ki6o6m.e18vylim0')
		updateButton.click()
		time.sleep(10)
	except:
		pass

	# Filter by ranked solo games
	ranked_solo_button = driver.find_element(By.CSS_SELECTOR, '#content-container > div.css-1s9fubg.e1jlljr10 > div.css-inknuf.e1htfwqw0 > ul > li:nth-child(2) > button')
	ranked_solo_button.click()
	time.sleep(3)

	preclicked_page = driver.page_source

	# Expand most recent 20 games for access to in depth game info
	for i in range(1,21):
		expand_button = driver.find_element(By.CSS_SELECTOR , '#content-container > div.css-1s9fubg.e1jlljr10 > div.css-164r41r.e17ux5u10 > li:nth-child(' + str(i) + ') > div > div.action > button')
		driver.execute_script("arguments[0].click();", expand_button)
		time.sleep(3)

	# Get the whole page's html
	page = driver.page_source

	# Stop chromedriver
	driver.quit()
	
	# Now unused, potentially useful later
	preclicked_soup = BeautifulSoup(preclicked_page, 'html.parser')

	# BS html parser object
	soup = BeautifulSoup(page, 'html.parser')
	
	# Lists of average ranks for the past 20 games
	avg_ranks = [x.getText(strip=True) for x in soup.findAll('div', attrs={'class': 'average-tier'})]
	
	return avg_ranks


if __name__ == "__main__":
	main("yourIGNhere")