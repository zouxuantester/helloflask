__author__ = 'zouxuan'
__date__ = '2019/5/7 11:49 AM'

from jinja2.utils import generate_lorem_ipsum
import os
import uuid


def random_file(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename
