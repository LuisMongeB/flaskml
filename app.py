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
from deepdream import gradient_ascent, deep_dream_static_image
from utils.constants import *
from utils.utils import *

import cv2
import numpy as np

os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

model_config = {'input': '', # {os.getcwd()}/static/{file_url}
                'img_width': 300,
                'layers_to_use': ['layer3'],
                'model_name': 'RESNET50',
                'pretrained_weights': 'PLACES_365',
                'pyramid_size': 4,
                'pyramid_ratio': 1.8,
                'num_gradient_ascent_iterations': 10,
                'lr': 0.09,
                'create_ouroboros': False,
                'ouroboros_length': 30,
                'fps': 30,
                'frame_transform': 'ZOOM_ROTATE',
                'blend': 0.85,
                'should_display': False,
                'spatial_shift_size': 32,
                'smoothing_coefficient': 0.5,
                'use_noise': False,
                'dump_dir': '',
                'input_name': ''} # os.path.basename(config['input'])  # handle absolute and relative paths

# At this point of the project I won't be using a db for two reasons:
# first, I won't be saving the images that users send as a matter of respect to privacy 
# and second, I will implement the registration in another moment
# the db will be added then.
# This project will focus on how to use a deep learning model such as Deep Dream
# to interact with users that will be able to transform their images into psychedelic ones. 

# Creating instance of the class
app = Flask(__name__)
app.config['SECRET_KEY'] = '592716490af3ccea41cbc1e68e1fc7e3d6f0656d3990af9f'
# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, server_default=db.func.now())


class Generate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))
    created_on = db.Column(db.DateTime, server_default=db.func.now())


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
            return f"<h1 style='display: flex;justify-content:center;align-items:center;height:100vh;'>Error: Format {file.mimetype} invalid.</h1>"
        
        filename = secure_filename(file.filename)
        # If file already exists do not commit uploaded file, just extract its id and redirect
        if Upload.query.filter_by(filename=file.filename).first():
            image = Upload.query.filter_by(filename=file.filename).first()
            return redirect(url_for('to_generate', upload_id=image.id))

        upload = Upload(filename=file.filename, data=file.read(), mimetype=file.mimetype)
        db.session.add(upload)
        db.session.commit()

        return redirect(url_for('to_generate', upload_id=upload.id))

    return render_template('create.html')

@app.route('/generate/<int:upload_id>', methods=['POST', 'GET'])
def to_generate(upload_id):
    if request.method == 'POST':
        # Query db
        image = Upload.query.filter_by(id=upload_id).first()
        if Generate.query.filter_by(filename=image.filename).first():
            image = Generate.query.filter_by(filename=image.filename).first()
            decoded = cv2.imdecode(np.frombuffer(image.data, np.uint8), -1)
            out_mimetype = f".{image.mimetype.split('/')[1]}"
            img_str = cv2.imencode(out_mimetype, decoded)[1].tostring()
            base64_encoded_image = base64.b64encode(img_str).decode("utf-8")
        
            return render_template('generate.html', to_generate=False, upload_id=upload_id, generated=base64_encoded_image)

        # Decode image for processing
        decoded = cv2.imdecode(np.frombuffer(image.data, np.uint8), -1)
        cv2.imwrite('decoded.jpg', decoded)
        ##### Processing
        # This will later be setup with user input
        user_model_config = model_config.copy()
        # Fill in input and input name keys
        # Instead of dump_dir we will save it in the generate db
        user_model_config['input'] = ''
        user_model_config['input_name'] = ''
        out_image = deep_dream_static_image(user_model_config, decoded)
        # print(user_model_config)
        # print(out_image)
        out_image = out_image * 255.0
        out_image = out_image.astype(np.uint8)
        
        # cv2.imwrite("test_input.jpg", out_image)

        #####
        # Encode in bytes again
        # Base64 encoding to serve in view
        out_mimetype = f".{image.mimetype.split('/')[1]}"
        img_str = cv2.imencode(out_mimetype, out_image)[1].tostring()
        base64_encoded_image = base64.b64encode(img_str).decode("utf-8")
        
        # Save to generate table
        generated = Generate(filename=image.filename, data=img_str, mimetype=image.mimetype)
        db.session.add(generated)
        db.session.commit()
        
        
        # response = current_app.make_response(img_encoded.tobytes())
        # response.headers.set('Content-Type', 'test/jpg')
        # response.headers.set('Content-Disposition', 'attachment', filename='image.jpg')
        # return response
        
        # Return generated image with button to save
        return render_template('generate.html', to_generate=False, upload_id=image.id, generated=base64_encoded_image)
    else:
        upload = Upload.query.filter_by(id=upload_id).first()
        # decode image data
        base64_encoded_image = base64.b64encode(upload.data).decode("utf-8")

        return render_template('generate.html', to_generate=base64_encoded_image, upload_id=upload_id, generated=False)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
