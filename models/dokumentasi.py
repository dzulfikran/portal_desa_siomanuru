from extensions import db


class Dokumentasi(db.Model):

    __tablename__ = "dokumentasi"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    kegiatan_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "kegiatan.id"
        ),
        nullable=False
    )


    foto = db.Column(
        db.String(200),
        nullable=False
    )