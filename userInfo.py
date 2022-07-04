import sqlite3 as sql

class UserInfo:
    DB_FILE = './user_info.db'
    TABLE_NAME= 'user_info'
    DATA_ARR = ['ID', 'STATE', 'GAME', 'PLAYER']
    TABLE_CONFIG = """
    (ID TEXT PRIMARY KEY NOT NULL,
    STATE INT NOT NULL,
    GAME TEXT NOT NULL,
    PLAYER TEXT NOT NULL)
    """

    @classmethod
    def createTable(cls) -> None:
        if not cls.isTableExist():
            with sql.connect(cls.DB_FILE) as db:
                db.cursor().execute(f'create table {cls.TABLE_NAME} {cls.TABLE_CONFIG};')
                db.commit()

    @classmethod
    def isTableExist(cls) -> bool:
        with sql.connect(cls.DB_FILE) as db:
            cursor = db.cursor()
            result = cursor.execute(f'select count(*) from sqlite_master where type = "table" and name = "{cls.TABLE_NAME}"').fetchone()
            db.commit()
            return True if result[0] == 1 else False

    @classmethod
    def isUserExist(cls, user_id: str) -> bool:
        return cls.getInfo(user_id) != ()

    @classmethod
    def saveInfo(cls, *args, **kwargs) -> None:
        # merge args and kwargs
        insert_data = {}
        if len(args) == 1 and isinstance(args[0], dict):
            for key, val in args[0].items():
                insert_data[key.upper()] = val
        else:
            for key, val in zip(cls.DATA_ARR, args):
                insert_data[key] = val
            for key, val in kwargs.items():
                insert_data[key.upper()] = val
        
        # check args
        missing_args = []
        for key in cls.DATA_ARR:
            if key not in insert_data:
                missing_args.append(key)
        if len(missing_args) > 1:
            last_args = missing_args[-1]
            missing_args.pop()
            if len(missing_args):
                error_str = ', '.join(["'" + key + "'" for key in missing_args]) + f', and "{last_args}"'
            else:
                error_str = "'" + last_args + "'"
            raise TypeError(f'UserInfo.saveInfo() missing {len(missing_args) + 1} requied positional arguments: {error_str}')

        with sql.connect(cls.DB_FILE) as db:
            cursor = db.cursor()
            if cls.isUserExist(insert_data['ID']):
                cls.delInfo(insert_data['ID'])

            cursor.execute(f'insert into {cls.TABLE_NAME} (ID, STATE, GAME, PLAYER) values(:ID, :STATE, :GAME, :PLAYER)', insert_data)
            db.commit()            

    @classmethod
    def getInfo(cls, user_id: str) -> tuple:
        with sql.connect(cls.DB_FILE) as db:
            cursor = db.cursor()
            result = cursor.execute(f'select * from {cls.TABLE_NAME} where ID = :ID', {'ID': user_id}).fetchone()
            db.commit()
            return () if result == None else result

    @classmethod
    def delInfo(cls, user_id: str) -> None:
        with sql.connect(cls.DB_FILE) as db:
            cursor = db.cursor()
            cursor.execute(f'delete from {cls.TABLE_NAME} where ID = ?', (user_id,))
            db.commit()
