#importing libraries
from io import BytesIO
import base64
from datetime import datetime
import os
import pickle

# Flask
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Models
from models.definitions.resnets import ResNet50
from deepdream import deep_dream_static_image
from utils.constants import *
from utils.utils import *
from db_models.db_models import db, Upload, Generate

import cv2
import numpy as np

os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

# This project will focus on how to use a deep learning model such as Deep Dream
# to interact with users that will be able to transform their images into dreamy looking ones.

# Creating instance of the class
app = Flask(__name__)
# app.config['SECRET_KEY'] = '592716490af3ccea41cbc1e68e1fc7e3d6f0656d3990af9f'
# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#to tell flask what url shoud trigger the function index()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template("index.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        file = request.files['file']
        # validate upload mimetype and empty filename
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            #TODO: return error template with message
            return f"<h1 style='display: flex;justify-content:center;align-items:center;height:100vh;'>Error: Format {file.mimetype} invalid.</h1>"

        filename = secure_filename(file.filename)
        # If file already exists do not commit uploaded file, just extract its id and redirect
        if Upload.query.filter_by(filename=filename).first():
            image = Upload.query.filter_by(filename=filename).first()
            return redirect(url_for('to_generate', upload_id=image.id))

        upload = Upload(filename=filename,
                        data=file.read(),
                        mimetype=file.mimetype)
        db.session.add(upload)
        db.session.commit()

        return redirect(url_for('to_generate', upload_id=upload.id))

    return render_template('create.html')


@app.route('/generate/<int:upload_id>', methods=['POST', 'GET'])
def to_generate(upload_id):
    if request.method == 'POST':
        # Query db
        image = Upload.query.filter_by(id=upload_id).first()

        # Decode image for processing
        decoded = cv2.imdecode(np.frombuffer(image.data, np.uint8), -1)

        # Copy original parameters
        user_model_config = model_config.copy()
        # User choices 
        user_model_config['model_name'] = request.form['model']
        user_model_config['layers_to_use'] = [request.form['layers']]
        user_model_config['num_gradient_ascent_iterations'] = int(request.form['iterations'])
        user_model_config['pyramid_size'] = int(request.form['pyramid_size'])
        # Instead of dump_dir we will save it in the generate db
        # Fill in input and input name keys
        user_model_config['input'] = ''
        user_model_config['input_name'] = ''
        out_image = deep_dream_static_image(user_model_config, decoded)
        # print(user_model_config)

        out_image = out_image * 255.0
        out_image = out_image.astype(np.uint8)

        # Encode in bytes again
        # Base64 encoding to serve in view
        out_mimetype = f".{image.mimetype.split('/')[1]}"
        img_str = cv2.imencode(out_mimetype, out_image)[1].tostring()
        base64_encoded_image = base64.b64encode(img_str).decode("utf-8")
        filename = secure_filename(image.filename)
        # Save to generate table
        generated = Generate(filename=filename,
                             data=img_str,
                             mimetype=image.mimetype,
                             upload_id=upload_id)
        db.session.add(generated)
        db.session.commit()

        # resize image to be displayed


        # Return generated image with button to save
        return render_template('generate.html', to_generate=False, upload_id=image.id, generated=base64_encoded_image, generate_id=generated.id)
    else:
        upload = Upload.query.filter_by(id=upload_id).first()
        # decode image data
        base64_encoded_image = base64.b64encode(upload.data).decode("utf-8")

        return render_template('generate.html', to_generate=base64_encoded_image, upload_id=upload_id, generated=False)

@app.route('/download/<int:generate_id>', methods=['POST', 'GET'])
def download(generate_id):
        generated =  Generate.query.filter_by(id=generate_id).first()
        return send_file(BytesIO(generated.data), mimetype='image/png', as_attachment=True, download_name=f"generated_{generated.filename}")
        
#TODO: add contact information
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)