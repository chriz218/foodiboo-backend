import boto3, botocore
from config import S3_BUCKET_NAME,S3_LOCATION, S3_SECRET_ACCESS_KEY, S3_ACCESS_KEY_ID
from app import app
from models.food import Food
from datetime import *

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_ACCESS_KEY_ID,
   aws_secret_access_key=S3_SECRET_ACCESS_KEY
)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
def upload_file_to_s3(file, bucket_name, acl="public-read"):
    now = datetime.now()
    date_string = now.strftime("%Y%m%d%H%M%S")
    file.filename = f"{date_string}{file.filename}"
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return file.filename 
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 