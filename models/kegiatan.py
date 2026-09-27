from extensions import db


class Kegiatan(db.Model):

    __tablename__ = "kegiatan"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    nama = db.Column(
        db.String(200),
        nullable=False
    )


    tanggal = db.Column(
        db.Date
    )


    kategori = db.Column(
        db.String(50)
    )


    deskripsi = db.Column(
        db.Text
    )


    banner = db.Column(
        db.String(200)
    )


    dokumentasi = db.relationship(
        "Dokumentasi",
        backref="kegiatan",
        cascade="all, delete",
        lazy=True
    )