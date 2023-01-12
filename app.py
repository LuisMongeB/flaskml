#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request, url_for, flash, redirect


# At this point of the project I won't be using a db for two reasons:
# first, I won't be saving the images that users send as a matter of respect to privacy 
# and second, I will implement the registration in another moment
# the db will be added then.
# This project will focus on how to use a deep learning model such as Deep Dream
# to interact with users that will be able to transform their images into psychedelic ones. 

# Creating instance of the class
app=Flask(__name__)
app.config['SECRET_KEY'] = '592716490af3ccea41cbc1e68e1fc7e3d6f0656d3990af9f'


#to tell flask what url shoud trigger the function index()
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            pass # do something
        elif  request.form.get('action2') == 'VALUE2':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        pass
         # return render_template('index.html', form=form)
    
    return render_template("index.html")

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Here we get into interesting things
        # we process the images through our model
        # receive the image
        # format it in the way the model wants
        # inference
        # pass it back to create.html
        return render_template('create.html')
        
    else:
        return render_template('create.html')


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