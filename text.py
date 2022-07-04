HELP = \
"""
輸入英文則可以比較資料
比賽資料類型

(1)進攻類:
PTS 得分
FGA 投籃出手數
FGM 投籃進球數
3PA 三分球出手數
3PM 三分球進球數
3P% 三分球命中率
FTA 罰球數
FTM 罰球進球數
FT% 罰球率
AST 助攻數

(2)防守類:
REB 籃板數
OREB 進攻籃板
DREB 防守籃板
STL 抄截數
BLK 阻攻數

(3)其他類:
TO 失誤
PF 犯規
+/- 正負值
EFF 效率值計算公式
GmSc 效率值計算公式
TS 真實命中率計算
"""

DATA = [
    "MIN", "FGM", "FGA", "FG%", "3PM",
    "3PA", "3P%", "FTM", "FTA", "FT%",
    "OREB", "DREB", "REB", "AST", "STL",
    "BLK", "TO", "PF", "PTS", "+/-",
    "EFF", "GmSc", "TS"
]