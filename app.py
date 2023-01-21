#importing libraries
from io import BytesIO
import base64
import os
import numpy as np
import pickle
import os
# Flask
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

# Models
from models.definitions.resnets import ResNet50
from deepdream import gradient_ascent, deep_dream_static_image
from utils.constants import *
from utils.utils import *
from flask_sqlalchemy import SQLAlchemy

# from db import db_init, db
# from db_models import Img, Upload


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

class Generate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.String(20))

#to tell flask what url shoud trigger the function index()
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        pass
    else:
        return render_template("index.html")

@app.route('/create', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']
        # validate upload mimetype
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        # If file already exists do not commit uploaded file, just extract its id and redirect
        if Upload.query.filter_by(filename=file.filename).first():
            image = Upload.query.filter_by(filename=file.filename).first()
            return redirect(url_for('to_generate', upload_id=image.id))

        upload = Upload(filename=file.filename, data=file.read(), mimetype=file.mimetype)
        db.session.add(upload)
        db.session.commit()

        return redirect(url_for('to_generate', upload_id=upload.id))

    return render_template('create_with_db.html')

@app.route('/generate/<int:upload_id>')
def to_generate(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    # decode image data
    base64_encoded_image = base64.b64encode(upload.data).decode("utf-8")

    return render_template('generate.html', to_generate=base64_encoded_image)


@app.route('/generate/', methods=['GET', 'POST'])
def display_image():
    '''
            # User Generating
        if genform.validate_on_submit():
            # Where we will read image
            filename = photos.load(upform.photo.id)
            file_url =  url_for('get_file', filename=filename)
            # DL stuff happens here
            # Model Parameters (a dictionary for now)
            model_config = {'input': f"{os.getcwd()}/static/{file_url}",
                            'img_width': 600,
                            'layers_to_use': ['relu4_3'],
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
                            'dump_dir': OUT_IMAGES_PATH, 
                            'input_name': file_url.split('/')[-1]}
            # Wrapping configuration into a dictionary
            print(model_config)
            print(file_url)
            generated_image = deep_dream_static_image(model_config, img=None)
            dump_path = save_and_maybe_display_image(model_config, generated_image)
            file_url = dump_path

            return render_template('create.html', form=genform, file_url=file_url, generate=None)
    '''
    pass

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


'''
if __name__ == "__main__":
    app.run(debug=True)
'''