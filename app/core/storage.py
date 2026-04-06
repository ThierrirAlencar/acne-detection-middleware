from minio import Minio
import uuid
from app.core.env import MINIO_PASS, MINIO_PATH, MINIO_USER

client = Minio(
    MINIO_PATH,
    access_key=MINIO_USER,
    secret_key=MINIO_PASS,
    secure=False  # True se usar HTTPS
)

# Nome do nosso bucket padrão
BUCKET_NAME = "images"

def create_bucket():
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)


#função padrão de upload
def upload_file(file):
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"

    client.put_object(
        BUCKET_NAME,
        filename,
        file.stream,
        length=-1,
        part_size=10*1024*1024,
        content_type=file.content_type
    )

    url = f"http://localhost:9000/{BUCKET_NAME}/{filename}"

    return filename, url