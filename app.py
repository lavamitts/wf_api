# app.py
from flask import Flask, request
from flask_cors import CORS
from classes.controller import Controller


app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return "<h1>Windsor Framework Green Lanes Prototype API</h1>"


@app.route('/subheadings/<goods_nomenclature_item_id>')
def get_commodity(goods_nomenclature_item_id):
    controller = Controller()
    commodity = controller.get_commodity(goods_nomenclature_item_id)
    return commodity


@app.route('/subheadings/<goods_nomenclature_item_id>/<geographical_area_id>')
def get_commodity_with_geo(goods_nomenclature_item_id, geographical_area_id):
    args = request.args
    controller = Controller()
    commodity = controller.get_commodity(
        goods_nomenclature_item_id, geographical_area_id, args)
    return commodity


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
    # app.run(threaded=True, port=5000)
