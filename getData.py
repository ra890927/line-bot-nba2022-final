from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import re
import json

class JSexector:
    BROWSER_PATH = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

    @classmethod
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    @classmethod
    def execute(self, url: str, execute_commmad: str) -> str:
        self.driver.get('https://www.nba.com/game/gsw-vs-bos-0042100406/box-score')
        return self.driver.execute_script(execute_commmad)

    @classmethod
    def __del__(self) -> None:
        self.driver.quit()

if __name__ == '__main__':
    jse = JSexector()

    final_info = {
        'data': ['MIN', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', '+/-'],
        'GSW': ['Andrew Wiggins', 'Otto Porter Jr.', 'Draymond Green', 'Klay Thompson', 'Stephen Curry', 'Kevon Looney', 'Gary Payton II', 'Jordan Poole', 'Andre Iguodala', 'Nemanja Bjelica', 'Jonathan Kuminga', 'Damion Lee', 'Moses Moody', 'Juan Toscano-Anderson'],
        'BOS': ['Jayson Tatum', 'Al Horford', 'Robert Williams III', 'Jaylen Brown', 'Marcus Smart', 'Derrick White', 'Payton Pritchard', 'Grant Williams', 'Nik Stauskas', 'Luke Kornet', 'Sam Hauser', 'Aaron Nesmith', 'Juwan Morgan', 'Malik Fitts', 'Daniel Theis']
    }

    for g in range(6):
        url = 'https://www.nba.com/game/'
        if g % 2 == 0:
            url += 'gsw-vs-bos-'
        else:
            url += 'bos-vs-gsw-'
        url += f'004210040{g + 1}/box-score'

        GSW_info = []
        BOS_info = []
        num_player = int(jse.execute(url, 'return document.querySelectorAll(".StatsTableBody_tbody__2eDxB > tr").length'))

        for i in range(num_player):
            res = jse.execute(url, f'return document.querySelectorAll(".StatsTableBody_tbody__2eDxB > tr")[{i}].outerText')
            player_info_list = list(filter(None, re.split('[\n\t]', res)))
            # print(player_info_list)
            
            player_info = {}
            if len(player_info_list) > len(final_info['data']):
                player_info['NAME'] = player_info_list[0]
                player_info_list.pop(0)
                if len(player_info_list) == len(final_info['data']) + 1:
                    player_info['POS'] = player_info_list[0]
                    player_info_list.pop(0)

                for key, val in zip(final_info['data'], player_info_list):
                    player_info[key] = val
            else:
                player_info['NAME'] = player_info_list[0]
                for key in final_info['data']:
                    player_info[key] = 0
            
            if player_info['NAME'] in final_info['GSW']:
                GSW_info.append(player_info)
            else:
                BOS_info.append(player_info)

        with open(f'2021-22-final-g{g + 1}.json', mode='w+', encoding='utf-8') as f:
            all_info = {
                'GSW': GSW_info,
                'BOS': BOS_info
            }
            f.write(json.dumps(all_info, indent=4))

    del jse