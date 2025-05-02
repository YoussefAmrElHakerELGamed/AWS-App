from flask import Flask, request, jsonify, render_template
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from werkzeug.utils import secure_filename

app = Flask(__name__)
s3 = boto3.client('s3')

BUCKET_NAME = 'my-app-bucket-afhoasihgoiahsgd035526asgtqt4625w'

@app.route('/')
def home():
    return render_template("MainPage.html")

@app.route('/list_files', methods=['GET'])
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        if 'Contents' not in response:
            return jsonify({"files": []}), 200

        files = [
            {
                "filename": obj['Key'],
                "last_modified": obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                "size": obj['Size'],
                "storage_class": obj['StorageClass']
            }
            for obj in response['Contents']
        ]

        return jsonify({"files": files}), 200

    except (BotoCoreError, ClientError) as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return jsonify({"message": f"File {filename} deleted successfully"}), 200
    except (BotoCoreError, ClientError) as e:
        return jsonify({"error": str(e)}), 500

@app.route('/share/<filename>', methods=['GET'])
def share_file(filename):
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # 1 hour
        )
        return jsonify({"url": url}), 200
    except (BotoCoreError, ClientError) as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)

    try:
        s3.upload_fileobj(file, BUCKET_NAME, filename)
        return jsonify({"message": "File uploaded successfully"}), 200
    except (BotoCoreError, ClientError) as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
