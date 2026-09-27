# from app import db
from extensions import db


class Pengaturan(db.Model):

    id=db.Column(
        db.Integer,
        primary_key=True
    )


    nama_desa=db.Column(
        db.String(100)
    )


    alamat=db.Column(
        db.Text
    )


    google_maps=db.Column(
        db.Text
    )


    whatsapp_umkm=db.Column(
        db.String(20)
    )


    background=db.Column(
        db.String(200)
    )