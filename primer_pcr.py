import requests
from bs4 import BeautifulSoup

url = "https://genome.ucsc.edu/cgi-bin/hgPcr?hgsid=1734037312_Y2jZbmC4oiOUQ4c6D8iuAhkhaHv5&org=Human&db=hg38&wp_target=genome&wp_f=CAGCAAAGAACACGGTGAGC&wp_r=TTGGGTTGCAGACACCTGAG&Submit=submit&wp_size=4000&wp_perfect=15&wp_good=15&boolshad.wp_flipReverse=0&wp_append=on&boolshad.wp_append=0"

page = requests.get(url)

if page.status_code == 200:
    # data = response.json()
    print("data")

else:
    print(f'Failed to retieve data. Status code: {page.status_code}')

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('table', class_='hgInside')
for i in results:
    td = i.find('pre')
print(td.text)
a = td.text
name = a.split(':')
print(name[0][1:])
out = open(name[0][1:]+'_final_primer.txt', 'w')
string = a.strip().split('\n')
line1 = string[0]
edited_textInfo = line1.split(' ')
edited_textInfo[1] = "size:"+edited_textInfo[1]
edited_textInfo[2] = 'FP:'+edited_textInfo[2]
edited_textInfo[3] = 'RP:'+edited_textInfo[3]
edited_textInfo = ' '.join(edited_textInfo)
line = ''.join(string[1:])
final_line = edited_textInfo+'\n'+line
print(edited_textInfo, sep="\n", file=out)
print(line, sep="\n", file=out)
