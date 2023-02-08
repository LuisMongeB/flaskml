# FlaskML

<img width="1509" alt="app_main_page" src="https://user-images.githubusercontent.com/65911072/217524880-85e99bef-0770-4bcb-ae3e-e3330e40c74f.png">

## Project Description

FlaskML is a web application that leverages the Flask framework and the Deep Dream algorithm to provide an interactive and user-friendly experience for exploring the concept of neural network-based image generation.  The application allows users to upload their own images and generate dream-like versions of them using the Deep Dream algorithm.
It also provides a brief explanation of the concepts behind Deep Dream, including the concept of activation maximization through Gradient Ascent.

Deep Dream is a computer vision algorithm that generates highly abstract and dream-like images by amplifying the activations of the neurons in a deep convolutional neural network trained on image classification tasks. For a more detailed explanation visit the original Deep Dream <a href="https://ai.googleblog.com/2015/06/inceptionism-going-deeper-into-neural.html">blogpost</a>.


The application was built to utilize pre-trained deep learning models for the Deep Dream algorithm, implemented by <a href="https://github.com/gordicaleksa/pytorch-deepdream">Aleksa Gordic</a>. The user interface was designed for simplicity and ease of use, allowing users to quickly upload images and view the dreamified results.

It is not anywhere near perfect but I am working (and learning) to improve it while balancing the daily responsibilities I have. 

## Setup
1. `git clone https://github.com/LuisMongeB/flaskml.git`
1. Open Anaconda Prompt and navigate into project directory `cd path_to_repo`
2a.Run `conda env create -f environment.yml` from project directory (this will create a brand new conda environment).
2b.Create your own environment using Python version 3.9.15 and run `pip install -r requirements.txt`
3. Activate your environment with `conda activate flaskml' or `conda activate YOUR_ENV_NAME' if you chose to create your own environment. 

## Built with
- Python 3.9.15
- PyTorch 1.13.1+cpu (CPU only version to reduce size of image to be deployed to Heroku)
- Torchvision 0.14.1+cpu
- Flask (with Bootstrap and Jinja2 templating)
- Sqlite3 (with SQLAlchemy)

## Future Updates
- [] Migration to more scalable database // this is pending
- [] Deployment on cloud services (AWS or Azure) // this is pending 

## Contribution
Contributions, issues, and feature requests are welcome!
Give a ⭐️ if you like this project!

[@LuisMongeB](https://github.com/LuisMongeB) on Github
[@luis-diego-monge-bolanos](https://www.linkedin.com/in/luis-diego-monge-bolanos/) on LinkedIn