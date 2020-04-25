from flask import jsonify
from datetime import datetime
import pymysql
import os

# temporaily set secret environ var
# !!!-- REMOVE BEFORE DEPLOYMENT ---!!!
os.environ['secret'] = 'thisisthesecret'

def checkInfo(key, hwid, secret):
    if checkKey(key) is False:
        return jsonify({"msg":"INVALID KEY"})
    if checkSecret(secret) == False:
        return jsonify({"msg":"INVALID KEY"})
    if checkHwid(hwid, key) is False:
        return jsonify({"msg":"INVALID HWID"})
    return jsonify({"msg":"access_granted"})

def checkKey(key):
    conn = pymysql.connect("localhost", "root", "Musicman123!", "license")
    try:
        with conn.cursor() as cursor:
            cursor.execute("Select * from license_tbl where license_tbl.key = '%s'" % key)

            # check if item exists
            if (cursor.fetchone()):
                return True
            else:
                return False
    finally:
        conn.close()

def checkHwid(hwid, key):
    currentRow = None
    conn = pymysql.connect("localhost", "root", "Musicman123!", "license")
    try:
        with conn.cursor() as cursor:
            cursor.execute("Select * from license_tbl where license_tbl.key = '%s'" % key)

            currentRow = cursor.fetchone()
    finally:
        cursor.close()

    if (currentRow[3] is None):
        # hwid is empty and date is empty
        try: 
            with conn.cursor() as cursor:
                # add hwid and populate expire_date
                cursor.execute(f"UPDATE license_tbl SET hwid = '{hwid}' where id = {currentRow[0]}")
                conn.commit()
                expire_date = f"{datetime.today().year + 1}-{datetime.today().month}-{datetime.today().day}"
                cursor.execute(f"UPDATE license_tbl SET expire_date = '{expire_date}' where id = {currentRow[0]}")
                conn.commit()
        finally:
            cursor.close()
        return True
    else:
        if (currentRow[3] == hwid):
            # compare dates
            currentDate = datetime.strptime(f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}", '%Y-%m-%d')
            futureDate = datetime.strptime(str(currentRow[2]), '%Y-%m-%d')
            if (currentDate > futureDate):
                return False
            return True

    return False
    

def checkSecret(secret):
    if secret == 'thisisthesecret':
        return True
    return False