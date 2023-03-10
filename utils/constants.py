import enum
import os


import numpy as np
import torch


IMAGENET_MEAN_1 = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD_1 = np.array([0.229, 0.224, 0.225], dtype=np.float32)


DEVICE = torch.device("cpu")  # MPS still hasnt implemented all of it for use with Metal Performance Shaders (MPS)


LOWER_IMAGE_BOUND = torch.tensor((-IMAGENET_MEAN_1 / IMAGENET_STD_1).reshape(1, -1, 1, 1)).to(DEVICE)
UPPER_IMAGE_BOUND = torch.tensor(((1 - IMAGENET_MEAN_1) / IMAGENET_STD_1).reshape(1, -1, 1, 1)).to(DEVICE)


class TRANSFORMS(enum.Enum):
    ZOOM = 0
    ZOOM_ROTATE = 1
    TRANSLATE = 2


class SupportedModels(enum.Enum):
    VGG16 = 0
    VGG16_EXPERIMENTAL = 1
    GOOGLENET = 2
    RESNET50 = 3
    ALEXNET = 4


class SupportedPretrainedWeights(enum.Enum):
    IMAGENET = 0
    PLACES_365 = 1


SUPPORTED_VIDEO_FORMATS = ['.mp4']
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']

BINARIES_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'models', 'binaries')
DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'static')

INPUT_DATA_PATH = os.path.join(DATA_DIR_PATH, 'uploads')
OUT_IMAGES_PATH = os.path.join(DATA_DIR_PATH, 'generated')
# OUT_VIDEOS_PATH = os.path.join(DATA_DIR_PATH, 'out-videos')
# OUT_GIF_PATH = os.path.join(OUT_VIDEOS_PATH, 'GIFS')

# Make sure these exist as the rest of the code relies on it
os.makedirs(BINARIES_PATH, exist_ok=True)
os.makedirs(OUT_IMAGES_PATH, exist_ok=True)
# os.makedirs(OUT_VIDEOS_PATH, exist_ok=True)
# os.makedirs(OUT_GIF_PATH, exist_ok=True)

model_config = {'input': '', # {os.getcwd()}/static/{file_url}
                'img_width': 300,
                'layers_to_use': ['relu3_3'],
                'model_name': 'VGG16_EXPERIMENTAL',
                'pretrained_weights': 'IMAGENET',
                'pyramid_size': 5,
                'pyramid_ratio': 1.5,
                'num_gradient_ascent_iterations': 1,
                'lr': 0.09,
                'create_ouroboros': False,
                'ouroboros_length': 30,
                'fps': 30,
                'frame_transform': 'ZOOM_ROTATE',
                'blend': 0.5,
                'should_display': False,
                'spatial_shift_size': 32,
                'smoothing_coefficient': 0.8,
                'use_noise': False,
                'dump_dir': '',
                'input_name': ''} 
