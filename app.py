from flask import Flask,jsonify,request,send_file
import boto3
import os
from botocore.exceptions import ClientError
from random import randint
from PIL import Image
import json
import base64
app = Flask(__name__)

BUCKET_NAME = "promanageimages"

#Delete all csv files
def remove_images():
    for folder, subfolders, files in os.walk('images/'):            
        for file in files:            
            # checking if file is  
            # of .txt type  
            if file.endswith('.jpg'):  
                path = os.path.join(folder, file)                    
                # printing the path of the file  
                # to be deleted  
                print('deleted : ', path )                
                # deleting the csv file  
                os.remove(path)
    return "done"
'''
Writing base64 encoded string to image
image = base64.b64decode(data)
with open('images/testimage.jpg', mode='wb') as file:
    file.write(image)
'''
#Convert to jpg
def convert_and_save(imageData):
    try:
        im = Image.open(imageData)
        jpg_convert = im.convert("RGB")
        jpg_convert.save("images/testimage.jpg")
        return "success"
    except:
        return "failure"

@app.route("/",methods=["GET"])
def index():
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET_NAME)
        company_ls = []
        for value in bucket.objects.filter(Prefix=''):
            company_ls.append(value.key)
        return jsonify({"message":"success","success":company_ls})
    except:
        return jsonify({'message':'error', 'error': 'Unable to connect to backend server'})

@app.route("/upload",methods=['POST'])
def upload():
    try:
        s3 = boto3.client('s3')
        imageData = request.files['image_file']
        msg = convert_and_save(imageData)
        if msg == "failure":
            return jsonify({'message':'error', 'error': 'file format not supported'})
        company_name = request.form['company_name']
        _id = randint(1,1000000)
        file_name = company_name+"/%s.jpg" % _id
        s3.upload_file('images/testimage.jpg',BUCKET_NAME,file_name)
        remove_images()
        return jsonify({'message':'success'})
    except Exception as e:
        print(e)
        return jsonify({'message':'error', 'error': 'Unable to save'})

@app.route("/delete", methods=["DELETE"])
def delete():
    try:
        data = request.get_json(force=True)
        folder_name = data["company_name"]
        file_name = folder_name + "/" + data["image_name"]
        client = boto3.client("s3")
        client.delete_object(Bucket=BUCKET_NAME,Key=file_name)
        return jsonify({"message":"success"})
    except:
        return jsonify({'message':'error', 'error': 'Unable to delete image'})

@app.route("/getImages",methods=["POST"])
def getImages():
    try:
        data = request.get_json(force=True)
        folder_name = data["company_name"]
        file_name = folder_name + "/" + data["image_name"]
        s3 = boto3.resource("s3")
        obj = s3.Object(BUCKET_NAME,file_name)
        file_stream = obj.get()['Body'].read()
        data = base64.encodebytes(file_stream).decode('utf-8')
        return jsonify({"message":"success","encoded_image":data})
    except Exception as e:
        print(e)
        return jsonify({'message':'error', 'error': 'Unable to find images'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001,debug=True)

