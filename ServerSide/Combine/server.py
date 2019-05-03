from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from Main import Detection

# Initialize the Flask application
app = Flask(__name__)
plate_detection = Detection()

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    number_plate, color = plate_detection.detect_car(img)

    # build a response dict to send back to client
    response = {'message': number_plate,
                'color': color}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)