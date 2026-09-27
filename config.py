import os


BASE_DIR=os.path.abspath(
    os.path.dirname(__file__)
)

class Config:

    SECRET_KEY="portal_desa_secret"

    SQLALCHEMY_DATABASE_URI=(
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "instance",
            "desa.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS=False

    UPLOAD_FOLDER=os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp"
    }

    NAMA_DESA = "Desa Siomanuru"