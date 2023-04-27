import base64
from flask import Flask, request, send_file
from colorCorrection import Main

app = Flask(__name__)

#testing the server
@app.route("/")
def index():
    return "testing color bliss server"

@app.route('/api/upload', methods=['POST'])
def upload():
    # Decode the base64-encoded photo

    photo = request.json['photo']
    option = request.json['option']

    #save photo
    
    # option = "Deutranopia"
    photo = base64.b64decode(photo)

    IMG_DIR = 'decoded_image.jpg'
 
    with open(IMG_DIR, 'wb') as f:
        f.write(photo)

    #IMG_DIR = photo.filename
    
    print(option)

    if option == "Protanopia":
         Main.correctImage(get_path=IMG_DIR,
                            return_type_image='save',
                            save_path ='correctedImage.png',
                            degree_of_protanopia=0.9,
                            degree_of_deutranopia=0.0)
    elif option == "Deuteranophia":
        Main.correctImage(get_path=IMG_DIR,
                          return_type_image='save',
                          save_path='correctedImage.png',
                          degree_of_protanopia=0.0,
                          degree_of_deutranopia=1.0)

    
    ## get corrected image

    return 'success'

@app.route('/api/recieve', methods=['GET'])
def recieve():
    
    return send_file('correctedImage.png' , mimetype='image/png')



if __name__ == "__main__":
    app.run(debug=True , port=8000, host='0.0.0.0')