from flask import Flask, request ,send_from_directory
from twilio.rest import Client
from twilio import twiml
import os
from bs4 import BeautifulSoup
import requests
from deta import Deta
from scrape import fetch_grade_card
from notify import send_notification



app=Flask(__name__,static_folder="results")


deta_key=os.environ.get('DETA_KEY')
ktu_id=os.environ.get('KTU_ID')
ktu_pass=os.environ.get('KTU_PASS')
deta = Deta(deta_key)
db = deta.Base("users")

sem=os.environ.get("SEM")

result_checkers=['Result','B.Tech',sem]   

print(result_checkers)   

login_url='https://app.ktu.edu.in/login.jsp'
url = 'https://ktu.edu.in/'
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    'Cache-Control': 'no-cache',
    "Pragma": "no-cache"
}

@app.route('/check',methods=['GET'])
def check_notif():
    global result_checkers
    print(result_checkers)
    req=requests.get(url,headers=headers)
    soup=BeautifulSoup(req.content,'html5lib')

    announcmnt=soup.find(class_="annuncement")
    req = requests.get(url, headers=headers)
    if req.status_code!=200:
        return 'Site Down'
    for notif in announcmnt.find_all('li'):

        if all(x in notif.text for x in result_checkers):
            if db.get(ktu_id)['fetched']==False:

                result=fetch_grade_card(ktu_id,ktu_pass,sem)
                db.update({'fetched':True},ktu_id)
                send_notification()
                return("Result Fetched")
            

    return("No Notifications")

@app.route('/results/<path:filename>')
def result(filename):
    try:
        return send_from_directory(
            os.path.join(app.instance_path, 'results'),
            filename
        )
    except:
        return 'File Not Found'

if __name__ == '__main__':
    app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
