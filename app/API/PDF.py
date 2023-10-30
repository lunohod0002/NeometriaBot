from app.config import api_id, api_password
import boto3


class PDF():
    def __init__(self):
        self.aws_access_key_id = api_id
        self.aws_secret_access_key = api_password
        self.endpoint_url = 'https://storage.yandexcloud.net'

    def upload_document(self, telegram_id, file_name,key,catalog) -> bool:
        s3 = boto3.resource(service_name='s3',
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key,
                            region_name="ru-central1")
        bucket = s3.Bucket("neometria-documents")

        return bucket.upload_file(Key=f"{catalog}/[doc]{telegram_id}[doc]{key}", Filename=f"{file_name}")

    def download_document(self, telegram_id,catalog):
        s3 = boto3.resource(service_name='s3',
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key,
                            region_name="ru-central1")
        bucket = s3.Bucket("neometria-documents")
        mas=[]
        for bucket_file in bucket.objects.all():
            try:
                if bucket_file.key.count("[doc]") != 0 and bucket_file.key.split("[doc]")[1] == str(telegram_id) and bucket_file.key.split("[doc]")[0]==(catalog+"/"):
                    file_name = bucket_file.key.split("[doc]")[2]
                    bucket.download_file(Key=f"{catalog}/[doc]{telegram_id}[doc]{file_name}", Filename=file_name)
                    mas.append(bucket_file.key.split("[doc]")[2])
            except Exception as e:
                if e =="An error occurred (404) when calling the HeadObject operation: Not Found":
                    return None
        if len(mas)!=0:
            return mas
        else:
            return None
    def delete_from_ctalog(self, telegram_id,catalog):
        s3 = boto3.resource(service_name='s3',
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key,
                            region_name="ru-central1")
        bucket = s3.Bucket("neometria-documents")
        mas=[]
        bucket = s3.Bucket("neometria-documents")
        for bucket_file in bucket.objects.all():
            if len(bucket_file.key.split("[doc]")) > 1 and bucket_file.key.split("[doc]")[0] == (f"{catalog}" + "/") and \
                    bucket_file.key.split("[doc]")[1] == str(telegram_id):
                bucket_file.delete()