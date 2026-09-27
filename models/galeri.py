from extensions import db



class Galeri(db.Model):


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    judul = db.Column(
        db.String(200),
        nullable=False
    )


    deskripsi = db.Column(
        db.Text
    )


    foto = db.Column(
        db.String(200),
        nullable=False
    )


    kategori = db.Column(
        db.String(100)
    )