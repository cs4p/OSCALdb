import mysql.connector

import secrets


def openDB():
    db = mysql.connector.connect(
        host="localhost",
        user=secrets.db_user,
        passwd=secrets.db_passwd,
        database="ssp"
    )
    return db

def insertFromDict(table, dict):
    """Take dictionary object dict and produce sql for
    inserting it into the named table"""
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join(map(dictValuePad, dict))
    sql += ');'
    return sql

def dictValuePad(key):
    return '%(' + str(key) + ')s'

def UpdateDB(sql,insert_dict,db):
    cursor = db.cursor()
    try:
        cursor.execute(sql, insert_dict)
        db.commit()
    except:
        print("SQL Error: " + sql)
        print(insert_dict)

def createDB(db):
    f = open('createDB.sql')
    sql = f.read()
    sqlStatements = sql.split(';')
    cursor = db.cursor()
    for cmd in sqlStatements:
        if cmd != '\n':
            cursor.execute(cmd)
            print(cursor.statement)
    db.commit()
