import os
import sqlite3
from flask import abort, Flask, jsonify, request
from random import choice

app = Flask(__name__)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']
    return is_token_valid and is_team_id_valid

@app.route('/lixi', methods=['POST'])
def lixi():
    if not is_request_valid(request):
        abort(400)
    stk = request.form['text']
    user_name = request.form['user_name']
    list_id = []
    con = sqlite3.connect('lixi.db')
    cur = con.cursor()
    for id in cur.execute('SELECT id FROM lixi where stk = "0"'):
        list_id.append(id[0])
    id = choice(list_id)
    query = 'SELECT menhgia FROM lixi where id = ' + str(id)
    for menhgia in cur.execute(query):
        m = menhgia[0]
    q_update = "update lixi set stk = '" + str(stk) + "' , user_name = '" + user_name + "' where id = " + str(id)
    print(q_update)
    cur.execute(q_update)
    con.commit()
    cur.close()
    t = 'Chúc mừng ' + user_name + ' nhận được lì xì ' + str(m)
    return jsonify(
        response_type='in_channel',
        text= t,
    )
@app.route('/danhsach', methods=['POST'])
def danhsach():
    if not is_request_valid(request):
        abort(400)
    mess = ''
    con = sqlite3.connect('lixi.db')
    cur = con.cursor()
    q = 'SELECT user_name, menhgia, stk FROM lixi where stk != "0"'
    for id in cur.execute(q):
        m = str(id[0]) + " đã nhận được lì xì " + str(id[1]) +", số tài khoản là " + str(id[2]) + "\n"
        mess += m
    cur.close()
    return jsonify(
        response_type='in_channel',
        text= mess,
    )
