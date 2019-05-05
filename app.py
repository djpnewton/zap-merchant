#!/usr/bin/python3
import os
import logging
import secrets
import time
import sys

from flask import Flask, request, jsonify, abort, render_template
from flask_qrcode import QRcode
import pywaves as pw

#from database import db_session, init_db
#from models import KycRequest

#init_db()
# testnet node
#TESTNET_WAVES_NODE='https://testnode1.wavesnodes.com'
#pw.setNode(TESTNET_WAVES_NODE, 'testnet')
# mainnet node
WAVES_NODE='https://nodes.wavesnodes.com'
pw.setNode(WAVES_NODE, 'mainnet')
pw.setOnline()
logger = logging.getLogger(__name__)
app = Flask(__name__)
qrcode = QRcode(app)

# testnet asset id
#ASSET_ID='CgUrFtinLXEbJwJVjwwcppk4Vpz1nMmR3H5cQaDcUcfe'
# mainnet asset id
ASSET_ID='9R3iLi4qGLVWKc16Tg98gmRvgg1usGEYd7SgC1W5D6HB'
asset = pw.Asset(ASSET_ID)
if asset.status() != 'Issued':
    print("ERROR: could not load asset")
    sys.exit(1)
if asset.decimals == 0:
    print("ERROR: asset decimals is 0")
    sys.exit(2)

def setup_logging(level):
    # setup logging
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('[%(name)s %(levelname)s] %(message)s'))
    logger.addHandler(ch)
    # clear loggers set by any imported modules
    logging.getLogger().handlers.clear()

@app.route('/')
def hello():
    #request_count = KycRequest.count(db_session)
    #return 'Hello World! %d requests created' % request_count
    return 'boo'

@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get('data', '')
    return send_file(qrcode(data, mode='raw'), mimetype='image/png')

@app.route('/req/<addr>', methods=['GET'])
def req(addr=None):
    if not pw.validateAddress(addr):
        return abort(400, 'invalid address')
    invoice_id = int(time.time())
    return render_template('addr.html', addr=addr, invoice_id=invoice_id, qrcode_data=None)

@app.route('/check/<addr>', methods=['GET'])
def check(addr=None):
    if not pw.validateAddress(addr):
        return abort(400, 'invalid address')
    amount = request.args.get('amount')
    try:
        amount = float(amount)
    except:
        abort(400, f'invalid amount "{amount}"')
    amount_int = int(round(amount * 10**asset.decimals))
    invoice_id = request.args.get('invoice_id')
    qrcode_data = f'waves://{addr}?asset={ASSET_ID}&amount={amount_int}&attachment={{"invoice_id":"{invoice_id}"}}'
    return render_template('addr.html', addr=addr, invoice_id=invoice_id, qrcode_data=qrcode_data, asset_id=ASSET_ID, amount=amount_int, node=WAVES_NODE)


if __name__ == '__main__':
    setup_logging(logging.DEBUG)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
