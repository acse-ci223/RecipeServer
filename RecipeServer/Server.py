from flask import Flask, request, jsonify
from flask_cors import CORS

from .Processor import Processor

__all__ = ['Server']


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        self.processor = Processor()

    def setup_routes(self):
        @self.app.route('/recipe', methods=['POST'])
        def handle_recipe():
            data = request.json
            recipe_name = data.get('name')
            if recipe_name:
                res = self.process_recipe(recipe_name)
                return jsonify({"message": res.to_dict()}), 200
            else:
                return jsonify({'error': 'Recipe name is missing'}), 400

    def process_recipe(self, recipe):
        download = self.processor.download_recipe(recipe)
        res = self.processor.process(download)
        return res

    def run(self):
        self.app.run(debug=True)
