import json
from text import *
from userInfo import UserInfo
from enum import IntEnum, auto

class Bot:
    class State(IntEnum):
        INITIAL         = auto()
        GAME            = auto()
        NUMBER_PLAYER   = auto()
        ONE_PLAYER      = auto()
        TWO_PLAYER      = auto()
        CHOOSE_DATA     = auto()
        EXIT            = auto()
        ERROR           = auto()

    def __init__(self, *args, **kwargs) -> None:
        # using kwargs
        if len(args) == 0:
            if 'user_id' not in kwargs:
                raise TypeError('self.__init__() need attibute "user_id" to construct')

            for key, val in kwargs.items():
                setattr(self, key, val)

            if isinstance(self.state, int):
                self.state = self.State(self.state)
            if isinstance(self.game_data, str):
                self.game_data = json.loads(self.game_data)
            if isinstance(self.player, str):
                self.choosePlayer(self.player)

            if not hasattr(self, 'game_data'):
                self.game_data = {}
            if not hasattr(self, 'state'):
                self.state = self.State.INITIAL
            if not hasattr(self, 'player'):
                self.player = ''
        elif len(args) == 1:
            if isinstance(args[0], str):
                self.user_id = args[0]
                self.state = self.State.INITIAL
                self.game_data = {}
                self.player = ''
            elif isinstance(args[0], tuple):
                data = args[0]
                self.user_id = data[0]
                # using choosePlayer will transfer state
                self.state = self.State.INITIAL
                self.game_data = json.loads(data[2])
                if data[3] == '':
                    self.player = ''
                else:
                    self.choosePlayer(data[3])
                # reset state
                self.state = self.State(int(data[1]))
            else:
                raise TypeError(f'self.__init__() unsupported type {type(args[0])} to construct')
        else:
            raise TypeError(f'self.__init__() takes 1 positional argument but {len(args)} were given')

    def info(self) -> dict:
        player_name = []
        for player in self.player:
            player_name.append(player['NAME'])
            
        return {
            'player': player_name[0] if len(player_name) == 1 \
                else ', '.join(player_name),
            'state': self.state.value,
            'game': json.dumps(self.game_data),
            'id': self.user_id
        }

    def transferState(self, args = None) -> None:
        match self.state:
            case self.State.INITIAL:
                self.state = self.State.GAME
                return
            case self.State.GAME:
                self.state = self.State.NUMBER_PLAYER
                return
            case self.State.NUMBER_PLAYER:
                if args == 1:
                    self.state = self.State.ONE_PLAYER
                    return
                elif args == 2:
                    self.state = self.State.TWO_PLAYER
                    return
                else:
                    self.state = self.State.EXIT
                    return
            case self.State.TWO_PLAYER:
                self.state = self.State.CHOOSE_DATA
                return
            case self.State.ONE_PLAYER | self.State.CHOOSE_DATA:
                self.state = self.State.EXIT
                return
            case self.State.EXIT:
                self.state = self.State.INITIAL
                return
            case default:
                self.state = self.State.ERROR
                return

    def process(self, args = None) -> str:
        match self.state:
            case self.State.INITIAL:
                return self.firstJoin()
            case self.State.GAME:
                return self.chooseGame(args)
            case self.State.NUMBER_PLAYER:
                return self.setPlayerNum(args)
            case self.State.ONE_PLAYER | self.State.TWO_PLAYER:
                return self.choosePlayer(args)
            case self.State.CHOOSE_DATA:
                return self.chooseData(args)
            case self.State.EXIT:
                self.reset()
                return self.process()
            case default:
                pass

    def firstJoin(self) -> str:
        self.transferState()
        return '選擇場次: [1], [2], [3], [4], [5], [6]'

    def reset(self) -> str:
        self.player = ''
        self.state = self.State.INITIAL
        self.game_data = {}

    def chooseGame(self, game: str) -> str:
        try:
            with open(f'./game_data/2021-22-final-g{game}.json', mode='r') as f:
                self.game_data = json.loads(f.read())
        except FileNotFoundError:
            return '沒有這場比賽'

        self.transferState()
        return '[1] 單一球員數據\n[2] 兩位球員比較\n[3] 兩隊數據比較\n[4] 兩隊 leader players'

    def setPlayerNum(self, option: str) -> str:
        option = int(option)
        if option == 1:
            self.transferState(option)
            return '球員名稱 全名:'
        elif option == 2:
            self.transferState(option)
            return '球員名稱 全名 (用 "," 隔開):'
        elif option == 3:
            self.transferState(option)
            return self.game_data['comparison']
        elif option == 4:
            self.transferState(option)
            return self.game_data['leader-players']
        else:
            return '不合法輸入'

    def choosePlayer(self, player: str) -> str:
        if ',' not in player:
            for playerInfo in self.game_data['GSW']:
                if player == playerInfo['NAME']:
                    self.transferState()
                    return self.printData(playerInfo)
            
            for playerInfo in self.game_data['BOS']:
                if player == playerInfo['NAME']:
                    self.transferState()
                    return self.printData(playerInfo)
            
            return f'球員{player}不存在'
        else:
            player1, player2 = player.split(',')
            player1 = player1.strip()
            player2 = player2.strip()

            if player1 == player2:
                return '不可輸入兩個相同的球員'

            player1Info = player2Info = None
            for playerInfo in self.game_data['GSW']:
                if player1 == playerInfo['NAME']:
                    player1Info = playerInfo
                elif player2 == playerInfo['NAME']:
                    player2Info = playerInfo
            
            for playerInfo in self.game_data['BOS']:
                if player1 == playerInfo['NAME']:
                    player1Info = playerInfo
                elif player2 == playerInfo['NAME']:
                    player2Info = playerInfo

            if player1Info != None and player2Info != None:
                self.player = (player1Info, player2Info)
                self.transferState()
                return '請輸入你想要比較的比賽資料(用空格方開)\n輸入 h | H 獲取提示 : '
            elif player1Info == None:
                return f'球員{player1}不存在'
            elif player2Info == None:
                return f'球員{player2}不存在'
            else:
                return '兩個球員都不存在'

    def printData(self, playerData: dict) -> str:
        return \
            f"Player Name: {playerData['NAME']}\n" + \
            f"Times: {playerData['MIN']}\n" + \
            f"FGM: {playerData['FGM']}\n" + \
            f"FGA: {playerData['FGA']}\n" + \
            f"FG%: {playerData['FG%']}\n" + \
            f"3PM: {playerData['3PM']}\n" + \
            f"3PA: {playerData['3PA']}\n" + \
            f"3P%: {playerData['3P%']}\n" + \
            f"FTM: {playerData['FTM']}\n" + \
            f"FTA: {playerData['FTA']}\n" + \
            f"FT%: {playerData['FT%']}\n" + \
            f"OREB: {playerData['OREB']}\n" + \
            f"DREB: {playerData['DREB']}\n" + \
            f"REB: {playerData['REB']}\n" + \
            f"AST: {playerData['AST']}\n" + \
            f"STL: {playerData['STL']}\n" + \
            f"BLK: {playerData['BLK']}\n" + \
            f"TO: {playerData['TO']}\n" + \
            f"PF: {playerData['PF']}\n" + \
            f"PTS: {playerData['PTS']}\n" + \
            f"+/-: {playerData['+/-']}\n" + \
            f"GmSc: {self.CalGmSc(playerData)}\n" + \
            f"EFF: {self.CalEFF(playerData)}\n" + \
            f"TS: {self.CalTS(playerData)}"

    def chooseData(self, dataStr: str) -> str:
        if dataStr == 'h' or dataStr == 'H':
            return HELP
        elif dataStr == 'exit':
            self.transferState()
            return '結束分析'
        elif dataStr in DATA:
            data = []
            for player in self.player:
                if dataStr == 'EFF':
                    data.append(self.CalEFF(player))
                elif dataStr == 'GmSc':
                    data.append(self.CalGmSc(player))
                elif dataStr == 'TS':
                    data.append(self.CalTS(player))
                else:
                    data.append(player[dataStr])

            return f'{self.player[0]["NAME"]} {data[0]}\n{self.player[1]["NAME"]} {data[1]}'
        else:
            return f'{dataStr}是不合法資料'

    @staticmethod
    def CalEFF(PlayerData: dict) -> float:
        PTS = int(PlayerData['PTS'])
        REB = int(PlayerData['REB'])
        AST = int(PlayerData['AST'])
        STL = int(PlayerData['STL'])
        BLK = int(PlayerData['BLK'])
        FGA = int(PlayerData['FGA'])
        FGM = int(PlayerData['FGM'])
        FTA = int(PlayerData['FTA'])
        FTM = int(PlayerData['FTM'])
        TO = int(PlayerData['TO'])
        EFF = (PTS + REB + AST + STL + BLK) - (FGA - FGM) - (FTA - FTM) - TO
        return round(EFF, 2)

    @staticmethod
    def CalGmSc(PlayerData: dict) -> float:
        PTS = int(PlayerData['PTS'])
        REB = int(PlayerData['REB'])
        OREB = int(PlayerData['OREB'])
        DREB = int(PlayerData['DREB'])
        AST = int(PlayerData['AST'])
        STL = int(PlayerData['STL'])
        BLK = int(PlayerData['BLK'])
        FGA = int(PlayerData['FGA'])
        FGM = int(PlayerData['FGM'])
        FTA = int(PlayerData['FTA'])
        FTM = int(PlayerData['FTM'])
        TO = int(PlayerData['TO'])
        PF = int(PlayerData['PF'])
        GmSc = (PTS + 0.7 * OREB + 0.3 * DREB + 0.7 * AST + STL + 0.7 * BLK) + \
            0.4 * FGM - 0.7 * FGA - 0.4 * (FTA - FTM) - TO - 0.4 * PF
        return round(GmSc, 2)

    @staticmethod
    def CalTS(PlayerData: dict) -> float:
        FGA = int(PlayerData['FGA'])
        FTA = int(PlayerData['FTA'])
        PTS = int(PlayerData['PTS'])
        TS = PTS / (2 * (FGA + 0.44 * FTA))
        return round(TS, 2)
