# Import Library
from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import sqlite3
import pandas as pd

# Import Custom Module
from module.Cleansing import clean
from module.GenerateDB import Generate
from module.Cleansing_Text import Clean_text


app = Flask(__name__)
app.config['DEBUG'] = True
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
app.json_encoder = LazyJSONEncoder


### Swagger ############
swagger_template = dict(
    info = {
        'title' : LazyString(lambda: 'API Documentation for Data Processing and Modelling'),
        'version' : LazyString(lambda: '1.0.0'),
        'description' : LazyString(lambda: "Dokumentasi API untuk pemrosesan dan pemodelan data"),
    },
    host = LazyString(lambda: request.host),
)

swagger_config = {
    'headers' : [],
    'specs' : [
        {
            'endpoint': '/docs',
            'route': '/docs.json',
        }
    ],
    'static_url_path' : '/flasgger_static',
    'swagger_ui' : True,
    'specs_route' : '/docs/',
}

swagger = Swagger(app, template = swagger_template, config = swagger_config)


@app.route('/data')
def index_data():
    return render_template('index_data.html')

@swag_from('docs/data.yml', methods= ['POST'])
@app.route('/data', methods = ['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename !=  '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        Generate(file_path)
        conn = sqlite3.connect('data.db', check_same_thread=False)
        df_main = pd.read_sql('SELECT tweet FROM data', conn)
        df_slang = pd.read_sql('''SELECT * FROM slangwords''', conn)
        df_stop = pd.read_sql('''SELECT * FROM stopwords''', conn)
        conn.close()

    df_clean = clean(df_main, df_slang, df_stop)

    json_response= {
        'status_code': 200,
        'description': 'Data yang sudah dibersihkan',
        'data' : list(df_clean) ,
    }
    return jsonify(json_response)

@app.route('/text')
def index_text():
    return render_template('index_text.html')

@swag_from('docs/text.yml', methods= ['POST'])
@app.route('/text', methods=['POST'])
def text_processing():
    text = request.form['text']

    json_response= {
        'status_code': 200,
        'description': 'Teks yang sudah dibersihkan',
        'data' : Clean_text(text),
    }

    response_data = jsonify(json_response)
    return response_data


if (__name__ == '__main__'):
    app.run(port = 5000)





