import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 

@app.route('/')
def bonjour():
    return "Bonjour"

@app.route('/api/alive',methods=['GET'])
def is_alive():
    return jsonify({"message":"Alive"}),200

@app.route('/api/associations',methods=['GET'])
def liste_assos():
    return jsonify(list(associations_df['id'])),200


@app.route('/api/association/<int:id>',methods=['GET'])
def detail_assos(id):
    assos = associations_df.loc[associations_df["id"] == id]
    if assos.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(assos.iloc[0].to_dict()),200


@app.route('/api/evenements',methods=['GET'])
def liste_even():
    return jsonify(list(evenements_df['id'])), 200


@app.route('/api/evenement/<int:id>',methods=['GET'])
def detail_even(id):
    even = evenements_df.loc[evenements_df["id"] == id]
    if even.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(even.iloc[0].to_dict()), 200


@app.route('/api/association/<int:id>/evenements',methods=['GET'])
def even_assos(id):
    evenassos = evenements_df.loc[evenements_df["association_id"] == id]
    return jsonify(list(evenassos["nom"])), 200


@app.route('/api/associations/type/<type>',methods=['GET'])
def assos_par_type(type):
    assos = associations_df.loc[associations_df["type"] == type]
    return jsonify(list(assos["nom"])), 200


if __name__ == '__main__':
    app.run(debug=False)
