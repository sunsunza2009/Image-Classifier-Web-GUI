Image Classifier Web GUI
================

A Flask Server for Create dataset, Training and Prediction

Requirements
----------

* Python 3

Quick Start
----------
Installing necessary packages
```
pip install -r requirements.txt 
```
You can change these config in "Flask Main Server/app.py"(Optional)
```python
app.config['DEBUG'] #Toggle Debug Mode
app.config['SECRET_KEY'] #Cookie encrypt key
app.config['UPLOAD_FOLDER'] #File Storage folder
app.config['Image_FOLDER'] #User image folder
app.config['Dataset_FOLDER'] #User dataset folder
app.config['Model_FOLDER'] #User model folder
app.config['List_model'] #List API from "Flask Train Server"
app.config['Request_Training'] #Request training API from "Flask Train Server"
app.config['Start_Training'] #Training API from "Flask Train Server"
```
Run server with Waitress
```
python server.py
```
Run server with flask
```
python app.py
```