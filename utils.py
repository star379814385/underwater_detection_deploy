import cv2
from pathlib import Path
import numpy as np

def read_image(img_path, cv2_imread_flag=cv2.IMREAD_COLOR):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), flags=cv2_imread_flag)
    return img

def save_image(img, save_path):
    cv2.imencode(str(Path(save_path).suffix), img)[1].tofile(save_path)