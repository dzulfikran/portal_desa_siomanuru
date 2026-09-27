# from app import db
from extensions import db


class UMKM(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    nama_produk = db.Column(
        db.String(150)
    )


    deskripsi = db.Column(
        db.Text
    )


    harga = db.Column(
        db.String(100)
    )


    nama_pemilik = db.Column(
        db.String(150)
    )


    alamat = db.Column(
        db.Text
    )


    nomor_hp = db.Column(
        db.String(20)
    )


    foto = db.Column(
        db.String(200)
    )