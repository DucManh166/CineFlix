from flask import Flask
from dotenv import load_dotenv
import os

# Webpage dependencies
from . import home
from . import discover
load_dotenv()

def create_webview():
    
# Dynamic path handling
    dir_path = os.path.dirname(os.path.realpath(__file__))
    static_path = os.path.join(dir_path, "assets")

# webview main app
    webview = Flask(__name__, template_folder=dir_path, static_folder=static_path)
    webview.config['SECRET_KEY'] = os.getenv("SECRET_KEY") # Debug env
    
# Webpages
    webview.register_blueprint(home.path)
    webview.register_blueprint(discover.path)
    return webview