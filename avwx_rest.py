#!/usr/bin/env python
import json
import requests
import sqlite3
from flask import Flask
from flask import request

app = Flask(__name__)

def airport_name(airport_code):
    conn = sqlite3.connect('aiport_db')
    c = conn.cursor()
    query = "select name from airport_info where ident = '{}'".format(airport_code.upper())
    c.execute(query)
    airport_name = c.fetchone()[0]
    return airport_name

@app.route('/<airport_code>')
def metar(airport_code):
    metaruri = 'http://avwx.rest/api/metar.php?station={}&options=summary&format=JSON'.format(airport_code)
    m = requests.get(metaruri)
    metar = json.loads(m.text)
    if 'summary' in request.args:
        try:
            output = 'Metar Summary for {0}:<br>{1}<br>{3}<br><br>{2}'.format(airport_name(airport_code),'=='*8, metar['Raw-Report'], metar['Summary'])
            return output
        except:
            return 'METAR for {} not available.'.format(airport_code)
    else:
        try:
            output = 'Metar for {0}:<br>{1}<br>{2}<br>'.format(airport_name(airport_code),'=='*8, metar['Raw-Report'])
   	    return output
        except:
    	    return 'METAR for {} not available.'.format(airport_code)

@app.route('/<airport_code>/taf')
def get_taf(airport_code):
    tafuri = 'http://avwx.rest/api/taf.php?station={}&options=summary&format=json'.format(airport_code)
    t = requests.get(tafuri)
    taf = json.loads(t.text)
    taf_output = 'TAF for {0}:<br>{1}<br>TAF issued at {2}<br>'.format(airport_name(airport_code),'=='*8, taf['Time'])
    forecast = []
    if 'summary' in request.args:
        for line in taf['Forecast']:
            forecast.append(line['Summary'])
            forecast_clean = json.dumps(forecast).replace('", "','<br>').strip('[').strip(']').strip('"')
    else:
        for line in taf['Forecast']:
            forecast.append(line['Raw-Line'])
            forecast_clean = json.dumps(forecast).strip('[').strip(']').replace(',','<br>').replace('"','')
    return '{}<br>{}<br>Flight Rules: {}'.format(taf_output, forecast_clean, taf['Forecast'][0]['Flight-Rules'])

if __name__ == '__main__':
    app.run(debug=True)
