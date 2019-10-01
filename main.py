from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

base_url = "https://en.wikipedia.org/wiki/World_Soccer_(magazine)"

# Send get http request
page = requests.get(base_url)

# Parse webpage for scraping
bs = BeautifulSoup(page.text, 'lxml')

# Find data points in the html
all_players = bs.find('table', class_='multicol').find('ul').find_all('li')
last_ten_players = all_players[-10:]

# Holds the data collected 
data = {
    'Year': [],
    'Country': [],
    'Player': [],
    'Team': [],
}

# Scrape all players in the top 10 list
for list_item in last_ten_players:

    # Get each item and save in data dictionary
    year = list_item.find('span').previousSibling.split()[0]
    if year:
        data['Year'].append(year)
    else:
        data['Year'].append('NA')

    country = list_item.find('a')['title']
    if country:
        data['Country'].append(country)
    else:
        data['Country'].append('NA')

    player_name = list_item.find_all('a')[1].text
    if player_name:
        data['Player'].append(player_name)
    else:
        data["Player"].append('NA')

    team = list_item.find_all('a')[2].text
    if team:
        data['Team'].append(team)
    else:
        data['Team'].append('NA')

# Format data dictionary with pandas
final = pd.DataFrame(data, columns=['Year', 'Country', 'Player', 'Team'])

# Starts dictionary list from # 1
final.index = final.index + 1

# Write panda dictionary to csv file
final.to_csv('top_ten_players.csv', index=False, sep=',', encoding='utf-8')

print(final)
