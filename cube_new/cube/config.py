import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    UPLOAD_FOLDER = '/tmp/cube-server'
    WORk_FOLDER = "public"
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
