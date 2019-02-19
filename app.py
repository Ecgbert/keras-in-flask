# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:48:16 2019

@author: lisssse14
"""
'''force using cpu inference'''
import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
from keras import backend as K
import numpy as np
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from flask import Flask, redirect, url_for, request, render_template, jsonify, Response, send_file
import cv2
from io import BytesIO
import base64
# from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', "JPG", "PNG", "JPEG", "GIF"])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    data = {'success': False}
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            '''upload and save file to server'''
            # file_path = os.path.join(APP_ROOT, 'uploads', secure_filename(f.filename))
            # f.save(file_path)
            p1 = image.load_img(f, target_size=(224, 224))
            p2 = image_preprocess(p1)
            with graph.as_default():
                global preds
                preds = model.predict(p2)
                pred_class = decode_predictions(preds)
                data["predictions"] = []
                for (id, label, prob) in pred_class[0]:
                    results = {"label": label, "probability": float(prob)}
                    data["predictions"].append(results)
                    data["success"] = True
    return jsonify(data)
            # return redirect(url_for('predict', filename=secure_filename(f.filename)))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def image_preprocess(img):
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


@app.route('/grad-cam', methods=['POST'])
def grad_cam():
    f = request.files['file']
    p1 = image.load_img(f, target_size=(224, 224))
    image_array = image.img_to_array(p1)
    p2 = image_preprocess(p1)
    class_idx = np.argmax(preds[0])
    with graph.as_default():
        class_output = model.output[:, class_idx]
        conv_output = model.get_layer('activation_49').output
        grads = K.gradients(class_output, conv_output)[0]

        gradient_function = K.function([model.input], [conv_output, grads])

        output, grads_val = gradient_function([p2])
        output, grads_val = output[0, :], grads_val[0, :, :, :]

        weights = np.mean(grads_val, axis=(0, 1))
        gradcam = np.dot(output, weights)

        gradcam = cv2.resize(gradcam, (224, 224))
        gradcam = np.maximum(gradcam, 0)
        gradcam = gradcam / gradcam.max()

        jetcam = cv2.applyColorMap(np.uint8(255 * gradcam), cv2.COLORMAP_JET)
        jetcam = (np.float32(jetcam) + image_array / 2)
        jetcam = cv2.cvtColor(jetcam, cv2.COLOR_BGR2RGB)

        final = image.array_to_img(jetcam)
        output_buffer = BytesIO()
        final.save(output_buffer, format='jpeg')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
    return base64_str


# @app.route('/predict', methods=['POST'])
# def predict(filename):
#     img = image.load_img(os.path.join(APP_ROOT, 'uploads/') + filename, target_size=(224, 224))
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     with graph.as_default():
#         preds = model.predict(x)
#         pred_class = decode_predictions(preds)  # ImageNet Decode
#         result = str(pred_class[0][0][1])  # Convert to string
#         return result


if __name__ == "__main__":
    global model
    global graph
    model = ResNet50(weights='imagenet')
    # 初始化 tensorflow graph
    graph = tf.get_default_graph()
    app.run(debug=True, port=5000, use_reloader=False, host="127.0.0.1")
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
