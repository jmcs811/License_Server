from flask import jsonify
from datetime import datetime, timedelta
import pymysql
import os

# temporaily set secret environ var
# !!!-- REMOVE BEFORE DEPLOYMENT ---!!!
os.environ['secret'] = 'thisisthesecret'

def checkInfo(key, hwid, secret):
    if checkKey(key) is False:
        return {"msg": "INVALID KEY"}
    if checkSecret(secret) == False:
        return {"msg": "INVALID KEY"}
    if checkHwid(hwid, key) is False:
        return {"msg": "INVALID HWID"}
    if checkDates() is False:
        return {"msg": "KEY EXPIRED"}
    return {"msg": "access_granted"}

def checkKey(key):
    global currentRow
    conn = pymysql.connect("localhost", "root", "Musicman123!", "license")
    try:
        with conn.cursor() as cursor:
            cursor.execute("Select * from license_tbl where license_tbl.key = '%s'" % key)
            # check if item exists
            currentRow = cursor.fetchone()
            if currentRow == None:
                return False
            return True
    finally:
        conn.close()

def checkHwid(hwid, key):
    conn = pymysql.connect("localhost", "root", "Musicman123!", "license")

    if (currentRow[3] is None):
        # hwid is empty and date is empty
        try:
            with conn.cursor() as cursor:
            # add hwid and populate expire_date
                setHwidAndDate(cursor, conn, hwid)
        finally:
            cursor.close()
        return True

    else:
        # hwid is populated check against stored one
        if (currentRow[3] == hwid):
            # compare dates
            return True
    return False

def setHwidAndDate(cursor, conn, hwid):
    cursor.execute(f"UPDATE license_tbl SET hwid = '{hwid}' where id = {currentRow[0]}")
    conn.commit()
    if (currentRow[2] == None):
        expireTime = datetime.now() + timedelta(hours=currentRow[4])
        cursor.execute(f"UPDATE license_tbl SET expire_date = '{expireTime}' where id = {currentRow[0]}")
        conn.commit()

def checkDates():
    currentDate = datetime.now()
    futureDate = datetime.strptime(str(currentRow[2]), '%Y-%m-%d %H:%M:%S')
    print(currentDate)
    print(futureDate)
    if currentDate < futureDate:
        return True
    return False

def checkSecret(secret):
    if secret == '4pUAauwutDFvTr9J':
        return True
    return False