from bs4 import BeautifulSoup
import requests
import pandas as pd


# Fetching Wikipedia Page using requests
url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'
response = requests.get(url)

# Beautiful Soup object
soup = BeautifulSoup(response.text, 'lxml')


# Getting Superbowl Championships table 
tables = soup.find_all('table')

req_table_pos = 0
for i in range(len(tables)):
    info = tables[i].contents
    for j in range(len(info)):
        if "<class 'bs4.element.Tag'>" in str(type(tables[i].contents[j])):
            try:
                if 'Super Bowl championships' in tables[i].contents[j].text:
                    req_table_pos = i
            except:
                continue
                
superbowl_table = tables[req_table_pos]

table_rows = superbowl_table.find('tbody').find_all('tr')

# Parsing each table row
file = open('rows.txt', 'w', encoding='utf-8')

for row in table_rows:
    line = ''
    
    # looping through each column in a row
    for index, item in enumerate(row.find_all('td')):
        if index in [0,1,2,3,4,5]:    # considering only required output columns
            # process each column corresponding to index nos.
            if index == 0:
                line += item.find('a').text.strip() + '|'
            elif index == 1:
                line += item.find('span').text.strip().split(', ')[1] + '|'    # split on ',' to only get year
            elif index == 2:
                line += item.find('a').text.strip() + '$'    # added '$' for future processing
                # last few rows in table are future games so 'small' tag is absent for these rows
                try:
                    line += item.find('small').text.strip() + '|'
                # break out of the loop since we don't want to consider games that are not played yet
                except:
                    break                    
            elif index == 4:
                line += item.find('a').text.strip() + '$'   
                line += item.find('small').text.strip() + '|'
            elif index == 5:
                line += item.find('span').text.strip().split('[')[0]    # split on '[' to avoid reding references part 
            else:    # handles case when index=3
                line += item.text.strip() + '|'
    
    # logic to avoid considering rows for future games that haven't been played yet
    if line.count('|') == 5:
        file.write(line+'\n')    # write to csv file
        
file.close()    

# Create DataFrame from rows.csv
df = pd.read_csv('rows.txt', names=['Game','Year','Winning team','Score','Losing team','Venue'],sep='|')

# Process team and venue columns to get desired output format
def parse_team(s):
    a = s.split('$')
    s_1 = a[0]
    s_2 = a[1]
    
    return s_1 + ' ' + s_2[1].zfill(2)
    
def parse_venue(s):
    a = s.split('(')
    s_1 = a[0]
    try:
        s_2 = a[1]
        return s_1 + s_2[0].zfill(2)
    except:
        return s_1 + ' ' + '01'
        

df['Winning team'] = df['Winning team'].apply(parse_team)
df['Losing team'] = df['Losing team'].apply(parse_team)
df['Venue'] = df['Venue'].apply(parse_venue)


# Write final results to transformed.csv
df.to_csv('transformed.csv', index=False)