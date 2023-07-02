from bs4 import BeautifulSoup as bs
import urllib3 as ul
import polars as pl

http = ul.PoolManager()
data = {
        'TeamName':[],
        'Year':[],
        'Win':[],
        'Losses':[],
        'OTLosses':[],
        'WinPercentage':[],
        'GoalsFor(GF)':[],
        'GoalsAgainst(GA)':[],
        'Point(Gained/Loss)':[],
      }
for repeat in range(6):
        url = 'https://www.scrapethissite.com/pages/forms/' + f'?page_num={repeat+1}&per_page=100'
        resp = http.request('GET', url)
        soup = bs(resp.data.decode('utf-8'),'html.parser').findAll('tr', class_='team')
        for team in soup:
                data['TeamName'].append(team.find('td',class_='name').text.strip())
                data['Year'].append(team.find('td',class_='year').text.strip())
                data['Win'].append(team.find('td',class_='wins').text.strip())
                data['Losses'].append(team.find('td',class_='losses').text.strip())
                data['OTLosses'].append(team.find('td',class_='ot-losses').text.strip())
                data['WinPercentage'].append(team.find('td',class_='pct').text.strip())
                data['GoalsFor(GF)'].append(team.find('td',class_='gf').text.strip())
                data['GoalsAgainst(GA)'].append(team.find('td',class_='ga').text.strip())
                data['Point(Gained/Loss)'].append(team.find('td',class_='diff').text.strip())
df = pl.DataFrame(data)
df.write_csv('hockey.csv',separator=',')
test = pl.read_csv('hockey.csv')
pl.Config().set_tbl_cols(10)
print(test.tail())