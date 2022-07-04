# Line Bot for NBA 2021-22 Final

### 請先加入好友

<img src="image/368zfhgn.png" width=300px><br>

### 或是點擊連結 [**加入好友**](https://liff.line.me/1645278921-kWRPP32q/?accountId=368zfhgn)

## Usage

利用 Line Bot 跟使用者互動，可以知道 NBA 2021-22 總決賽比賽詳細數據

- Times: 上場時間
- FGM: 投籃命中數
- FGA: 投籃出手數
- FG%: 投籃命中率
- 3PM: 三分命中數
- 3PA: 三分出手數
- 3P%: 三分命中率
- FTM: 罰球命中數
- FTA: 罰球出手數
- FT%: 罰球命中率
- OREB: 進攻籃板
- DREB: 防守籃板
- REB: 籃板
- AST: 助攻
- STL: 抄截
- BLK: 阻攻
- TO: 失誤
- PF: 犯規
- PTS: 得分
- +/-: 正負值
- GmSc: Game Score
- EFF: Efficiency
- TS: 真實命中率

## Setup

[Getting started with the Messaging API](https://developers.line.biz/en/docs/messaging-api/getting-started/)  
[line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)  
[message-types](https://developers.line.me/en/docs/messaging-api/message-types/)

### Line Developer

Use webhooks ```Enable```<br>
Webhook URL ```https://line-bot-nba2022-final.herokuapp.com/```

### Download Access Token

```python
# config.py
line_channel_access_token = 'your-access-token'
line_channel_secret = 'channel-secret'
```

### HeroKu

```shell
$ heroku login
$ heroku create line-bot-nba2022-final
$ heroku git:remote -a line-bot-nba2022-final
```

```
$ git add .
$ git commit -m "commit message"
$ git push heroku master
```

## Environment

- heroku-22
- Python3.10.5
- SQLite
- flask

## Reference

[Heroku | 搭配 Git 在 Heroku 上部署網站的手把手教學](https://medium.com/enjoy-life-enjoy-coding/heroku-%E6%90%AD%E9%85%8D-git-%E5%9C%A8-heroku-%E4%B8%8A%E9%83%A8%E7%BD%B2%E7%B6%B2%E7%AB%99%E7%9A%84%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8-bf4fd6f998b8)
