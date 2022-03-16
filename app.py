from flask import Flask, request
from flask import render_template
import json
import csv
import requests

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

data_from_json = json.loads(json.dumps(data))

rates = data_from_json[0].get('rates')

table = data_from_json[0].get('no')

with open('nbp.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    for currency in rates:
        writer.writerow([currency.get('currency'), currency.get('code'), currency.get('bid'), currency.get('ask')])

@app.route('/', methods=['GET', 'POST'])
def calc():
    if request.method == 'GET':
        price = ''
    elif request.method == 'POST':
        data = request.form
        print(data)
        data_quantity = data.get('quantity')
        data_rate = data.get('currency_rate')
        price_float = float(data_quantity)*float(data_rate)
        price = '%.2f' % price_float + ' PLN'
    return render_template('form.html', price=price, rates=rates, table=table)