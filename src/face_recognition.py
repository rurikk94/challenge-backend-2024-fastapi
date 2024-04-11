import face_recognition.api as fr
import numpy as np
from PIL import Image


def encode_photo(im: Image.Image) -> list[list[float]]:
    """
    Takes an image from a binary file (PNG, JPG)
    ^ and extract the data required to match faces
    * Returns a list of face-recognition encodings (list of float)
    """
    return [a.tolist() for a in fr.face_encodings(np.array(im), model="large")]


def match(test: list[float], enrollments: list[list[float]]):
    """
    Takes one of the encodings returned by encode_photo
    ^ which represents a single face
    Also takes a list of encodings (enrollments)
    Returns a list of matches (True/False) if the test matches the enrollment
    """
    return [
        bool(x)
        for x in fr.compare_faces(np.array(enrollments), np.array(test), tolerance=0.5)
    ]
