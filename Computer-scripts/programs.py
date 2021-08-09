import os
import subprocess
import sys
from getmac import get_mac_address as gma
import requests
import psycopg2 as psycopg2
import json

WOL_PASSWORD = "12345"
WOL_USER = "postgres"
WOL_DB_NAME = "wakeonlan"
WOL_PORT = 5432
WOL_HOST = "192.168.0.19"
API_URL = "http://192.168.0.28:6001/api/v1/"
con = psycopg2.connect(dbname=WOL_DB_NAME,user=WOL_USER,password=WOL_PASSWORD,host=WOL_HOST)

def logWakeUp(user,mac):
    cur = con.cursor()
    query = "select id from public.computers where mac = %s"
    cur.execute(query,(mac,))
    id = cur.fetchone()
    try:
        query = "INSERT INTO bootup_log (username,computer_id) VALUES (%s,%s)"
        cur.execute(query,(user,id))
        con.commit()
    except Exception as e:
        con.rollback()
        return -1
    return 0

def getProgramsToLaunch(mac):
    r = requests.get(API_URL + "macs/programs/launch/" + mac)
    return r.text

mac = gma()
mac = "FF:FF:FF:FF:FF:FF"
print(mac)
logWakeUp(os.getlogin(),mac)
programs = getProgramsToLaunch(mac)
for program in json.loads(programs):
    try:
        print("Trying to launch " + program)
        subprocess.Popen([program])
    except:
        raise Exception()

sys.exit(0)




    