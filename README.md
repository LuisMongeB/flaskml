# FlaskML

<img width="1509" alt="app_main_page" src="https://user-images.githubusercontent.com/65911072/217524880-85e99bef-0770-4bcb-ae3e-e3330e40c74f.png">

## Project Description

FlaskML is a web application that leverages the Flask framework and the Deep Dream algorithm to provide an interactive and user-friendly experience for exploring the concept of neural network-based image generation. The application allows users to upload their own images and generate dream-like versions of them using the Deep Dream algorithm. :art: :milky_way:
It also provides a brief explanation of the concepts behind Deep Dream, including the concept of activation maximization through Gradient Ascent.

Deep Dream is a computer vision algorithm that generates highly abstract and dream-like images by amplifying the activations of the neurons in a deep convolutional neural network trained on image classification tasks. For a more detailed explanation visit the original Deep Dream <a href="https://ai.googleblog.com/2015/06/inceptionism-going-deeper-into-neural.html">blogpost</a>.


The application was built to utilize pre-trained deep learning models for the Deep Dream algorithm, implemented by <a href="https://github.com/gordicaleksa/pytorch-deepdream">Aleksa Gordic</a>. The user interface was designed for simplicity and ease of use, allowing users to quickly upload images and view the dreamified results.

It is not anywhere near perfect but I am working (and learning) to improve it while balancing the daily responsibilities I have. 

## Setup
1. `git clone https://github.com/LuisMongeB/flaskml.git`
1. Open Anaconda Prompt and navigate into project directory `cd path_to_repo`
2. Create your own environment using Python version 3.9.15 like this `conda create --name flaskml python=3.9.15` and run `pip install -r requirementstxt`
3. Activate your environment `conda activate YOUR_ENV_NAME` after creating your own environment. 
4. Last we need to create the database models. Open terminal and run `python`. Then, run `from app import app, db` followed by `with app.app_context(): db.create_all()` and then press `CTR-C` to exit the Python interpreter.
5. In the terminal: `flask run` and you're done!

For any issues or comments, reach out please!

## Built with
- Python 3.9.15
- PyTorch 1.13.1
- Torchvision 0.14.1
- Flask (with Bootstrap and Jinja2 templating)
- Sqlite3 (with SQLAlchemy) and DB Browser for SQLite

## Future Updates
- [] Migration to more scalable database // this is pending
- [] Compatibility issues with Windows
- [] Deployment on cloud services (AWS or Azure) // this is pending 

## Contribution
Contributions, issues, and feature requests are welcome!
Give a ⭐️ if you like this project!

## Let's Connect
* On [Github](https://github.com/LuisMongeB) :star:
* On [Linkedin](https://www.linkedin.com/in/luis-diego-monge-bolanos/) :bulb:
