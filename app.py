from flask import Flask, request, jsonify, render_template
import boto3

app = Flask(__name__)
s3 = boto3.client('s3')

BUCKET_NAME = 'my-app-bucket-afhoasihgoiahsgd035526asgtqt4625w'

@app.route('/')
def home():
    return render_template("logIn.html")

@app.route('/signUp.html')
def signup():
    return render_template("signUp.html")

@app.route('/logIn.html')
def logInpage():
    return render_template("logIn.html")

@app.route('/MainPage.html')
def main():
    return render_template("MainPage.html")

@app.route('/login')
def logIn():
    data = request.json
    username = data['usernaem']
    password = data['password']
    folder_key = f'{username}/'
    password_key = f'{username}/password.txt'


    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_key)
    if 'Contents' in response:
        try:
            stored_obj = s3.get_object(Bucket=BUCKET_NAME, Key=password_key)
            stored_password = stored_obj['Body'].read().decode('utf-8')
            if stored_password == password:
                return jsonify({'authenticated': True}), 200
            else:
                return jsonify({'authenticated': False}), 401
        except s3.exceptions.NoSuchKey:
            return jsonify({'authenticated': False}), 404
    else:
        return jsonify({'error': 'no User with this name'}), 401



@app.route('/SignUp')
def signUp():
    data = request.json
    username = data['username']
    password= data['password']

    folder_key=f'{username}/'
    password_key = f'{username}/password.txt'

    UserFolder = s3.put_object(Bucket=BUCKET_NAME, Key=folder_key)
    UserPassword = s3.put_object(Bucket=BUCKET_NAME, Key=password_key, Body=password)

    if UserPassword['ResponseMetadata']['HTTPStatusCode'] == 200 or UserFolder['ResponseMetadata']['HTTPStatusCode'] == 200:
        return jsonify({'SignedUp': True}), 200
    else:
        return jsonify({'SignedUp': False}), 401



@app.route('/list_files')
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' not in response:
            return jsonify({"message": "No files found"}), 200
        
        files_details = []
        for obj in response['Contents']:
            file_details = {
                "filename": obj['Key'],
                "last_modified": obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                "size": obj['Size'],
                "storage_class": obj['StorageClass']
            }
            files_details.append(file_details)
        
        return jsonify({"files": files_details}), 200
    except Exception as e:
        return jsonify({"error": "no files found"}), 500



@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return jsonify({"message": f"File {filename} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/share/<filename>')
def share_file(filename):
    try:
        url = s3.generate_presigned_url('get_object',
                                               Params={'Bucket': BUCKET_NAME, 'Key': filename},
                                               ExpiresIn=3600)
        return jsonify({"url": url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/upload')
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = file.filename
    
    try:
        s3.upload_fileobj(file, BUCKET_NAME, filename)
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
