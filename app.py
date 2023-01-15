#importing libraries
import os
import numpy as np
import pickle
import os
# Flask
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

# Models
from models.definitions.resnets import ResNet50

UPLOAD_FOLDER = os.path.join('static', 'uploads')

# At this point of the project I won't be using a db for two reasons:
# first, I won't be saving the images that users send as a matter of respect to privacy 
# and second, I will implement the registration in another moment
# the db will be added then.
# This project will focus on how to use a deep learning model such as Deep Dream
# to interact with users that will be able to transform their images into psychedelic ones. 

# Creating instance of the class
app = Flask(__name__)
app.config['SECRET_KEY'] = '592716490af3ccea41cbc1e68e1fc7e3d6f0656d3990af9f'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only Images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )

    submit = SubmitField('Upload')

class GenerateForm(FlaskForm):
    # TODO: Add fields for different deep dream parameters
    submit = SubmitField('Generate')

#to tell flask what url shoud trigger the function index()
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
         # return render_template('index.html', form=form)
    
    return render_template("index.html")

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/create/', methods=['GET', 'POST'])
def create():
        # Here we get into interesting things
        # we process the images through our model
        # receive the image
        # format it in the way the model wants
        # inference
        # pass it back to create.html

        upform = UploadForm()
        genform = GenerateForm()

        if upform.validate_on_submit():
            filename = photos.save(upform.photo.data)
            file_url =  url_for('get_file', filename=filename)
        else:
            file_url = None

        if genform.validate_on_submit():
            file_url =  url_for('get_file', filename=filename)
            # DL stuff happens here



            return render_template('create.html', form=genform, file_url=file_url)
        

        return render_template('create.html', form=upform, file_url=file_url)
   


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