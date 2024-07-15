from flask import Flask, render_template, request, session, jsonify
import requests
from flask import redirect, url_for
import json


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        account_number = request.form['account_number']
        password = request.form['password']
        response = requests.post('http://127.0.0.1:8000/authenticate_account/', data={'account_number': account_number, 'password': password})
        if response.status_code != 200:
            try:
                error_message_in_account_auth = response.json()['error']
                return render_template('account_form.html', error_message_in_account_auth=error_message_in_account_auth)
            except:
                error_message_in_account_auth = "No Account with this Account Number exists"
                return render_template('account_form.html', error_message_in_account_auth=error_message_in_account_auth)
        else:
            account_details = response.json()
            bank_name = requests.get(f'http://127.0.0.1:8000/banks/{account_details["bank"]}/').json()['name']
            response = requests.get(f'http://127.0.0.1:8000/transactions/{account_details["account_id"]}')
            if response.status_code != 200:
                pendinglist = []
            else:
                pendinglist = response.json()
                pendinglist = [transaction for transaction in pendinglist if transaction['pending'] == True]
            return render_template('transaction_page.html', account_details=account_details, bank_name=bank_name, pendinglist=pendinglist)
    return render_template('account_form.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post('http://127.0.0.1:8000/login/', data={'username': username, 'password': password})
        if response.status_code != 200:
            return render_template('admin_form.html', error_message=response.json()['error'])
        else:
            response = requests.get('http://127.0.0.1:8000/pendingtransactions/')
            if response.status_code != 200:
                pending_list = [] 
            else:
                pending_list = response.json()    
            return render_template('admin_page.html', pending_list=pending_list)
        
    return render_template('admin_form.html')

