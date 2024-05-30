import os
import sys
import csv
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'controllers'))

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from tree_controller import TreeController

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

tree_controller = TreeController()

class TotitoApi:

    @app.route('/add_movement', methods=['POST'])
    @cross_origin()
    def add_movement():
        tree_controller.init_game()
        tree_controller.getGraph("tree.dot")

        data = request.json
        cell = int(data.get('cell'))
        cpu_first_player = data.get('cpu_first_player')

        results = tree_controller.get_cpu_movement(cell, cpu_first_player)
        tree_controller.getGraph("tree.dot")
        url = tree_controller.upload_images("tree.dot.png")

        return jsonify({
                'isWinner': results[0],
                'cpu_movement': results[1],
                "tree_url": url
            })

    @app.route('/reset_game', methods=['GET'])
    @cross_origin()
    def reset_game():
        tree_controller.clear_data()
        tree_controller.getGraph("tree.dot")
        url = tree_controller.upload_images("tree.dot.png")

        return jsonify({
            'message': 'Juego reiniciado correctamente',
            'tree_url': url
        })

    @app.route('/format_game', methods=['GET'])
    @cross_origin()
    def format_game():
        tree_controller.root = None
        tree_controller.clear_data()
        tree_controller.init_game()
        tree_controller.getGraph("tree.dot")
        url = tree_controller.upload_images("tree.dot.png")

        return jsonify({
            'message': 'Juego formateado correctamente',
            'tree_url': url
        })
    
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=3000)
