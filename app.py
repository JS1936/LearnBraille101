# Goal: Accept .png from user, save it locally, and upload it to Azure blob storage.
# Photo naming style in blob storage: uploaded_photo + <timestamp_ns> + .png
# Status: 
#   - Local run: OK
#   - Remote run: untested

from flask import Flask, request, redirect, send_file
import os

from azure.storage.blob import BlobServiceClient, BlobClient
import time

import shutil

import io
from io import BytesIO

# from <helper> import <helper_method>


app = Flask(__name__)

# Folder to save the uploaded photos
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h2>Download Photo</h2>
            <img src="https://capstonestorage123.blob.core.windows.net/mycontainer/uploaded_photo1728964649459844428.png"/>
            <form action="/download" method="get">
                <button type="submit">Download Photo</button>
            </form>

            <h2>Submit a Photo</h2>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <label for="file">Choose a photo:</label>
                <input type="file" id="file" name="file" accept="image/*">
                <input type="submit" value="Upload Photo">
            </form>
        </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:

        # Save the file locally
        local_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(local_file_path)

        # Connect to Azure Blob Storage
        connection_string = "DefaultEndpointsProtocol=https;AccountName=capstonestorage123;AccountKey=hcpBIufXBfBnGOxPZJlP7TrySHWBvOY8JvdCQLWjh1kUHQHK38HVNCqnU87JeMO0aQrN6zCLZR5n+AStX2g46g==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Specify the container and file
        timestamp_ns = time.time_ns()
        container_name = "mycontainer"
        blob_name = "uploaded_photo" + str(timestamp_ns) + ".png"

        # Upload the file
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data)

        return f"Photo uploaded successfully: {file.filename}"

@app.route('/download', methods=['GET'])
def download_file():

    # Connection string to Azure Blob Storage
    connection_string = "DefaultEndpointsProtocol=https;AccountName=capstonestorage123;AccountKey=hcpBIufXBfBnGOxPZJlP7TrySHWBvOY8JvdCQLWjh1kUHQHK38HVNCqnU87JeMO0aQrN6zCLZR5n+AStX2g46g==;EndpointSuffix=core.windows.net"

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Specify container and blob (file) name
    container_name = "mycontainer"
    blob_name = "uploaded_photo1728964649459844428.png"

    # Get BlobClient
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Download the blob to a local file
    with open("downloaded_example_photo.png", "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    return f"Photo downloaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)


#file_copy = shutil(file, os.path.dirname(os.path.abspath(__file__)) + file.filename)
#file_path =  "/Users/jenniferstibbins/PycharmProjects/example/testHoughCircles/Embossed_Braille_subsection_5to10cells.png"
#os.path.dirname(os.path.abspath(__file__)) + file.filename

#"/Users/jenniferstibbins/PycharmProjects/example/testHoughCircles/Embossed_Braille_subsection_5to10cells.png"

#### Original: ####
#filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#file.save(filepath)
#return f"Photo uploaded successfully: {file.filename}"
