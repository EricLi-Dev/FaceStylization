import os
from flask import Flask, flash, request, render_template, send_file
from numpy import who
from werkzeug.utils import secure_filename
from stylizer import generatePretrainedStyle, generateCustomStyle
from flask_cors import CORS

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} # not currently used
ALLOWED_MODELS = ["disney", "arcane_jinx", "jojo", "jojo_yasuho"]

# Init Flask App
app = Flask(__name__)

# Add CORS middleware for Cross-Origin-Resource-Sharing
CORS(app)

# Add Upload Folder for uploaded images
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

@app.route("/")
def hello_world():
    return f"Hello from Stylizer!"

@app.route('/upload', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        # check if the post request has the image part
        if 'image' in request.files and 'style' in request.form:
            # grab image from request
            file = request.files['image']
            filename = secure_filename(file.filename)
            
            # save file to disk
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            input_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Stylize image
            try:
                model = request.form['style']
                res = generatePretrainedStyle(file.filename, input_img_path, app.config['UPLOAD_FOLDER'], model)

                # send result back to client
                return send_file(res["results"], mimetype='image/jpg')
            except AssertionError as error:
                print(error)
                return str(error), 400
            
    return render_template('index.html')

@app.route('/generateCustomStyle', methods=['POST'])
def generateCustom():
    print(request.files)
    # check if the post request has the image part
    if 'image' in request.files and 'custom' in request.files:
        # grab image from request
        file = request.files['image']
        filename = secure_filename(file.filename)
        customFile = request.files['custom']
        customFilename = secure_filename(customFile.filename)
        
        # save file to disk
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        input_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        customFile.save(os.path.join(app.config['UPLOAD_FOLDER'], customFilename))
        input_custom_path = os.path.join(app.config['UPLOAD_FOLDER'], customFilename)
        
        print(input_img_path, input_custom_path)
        # Stylize image
        try:
            res = generateCustomStyle(file.filename, input_img_path, customFile.filename, input_custom_path, app.config["UPLOAD_FOLDER"])

            # send result back to client
            return send_file(res["results"], mimetype='image/jpg')
        except AssertionError as error:
            print(error)
            return str(error), 400

    return "Invalid Arguments", 400
            
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))
