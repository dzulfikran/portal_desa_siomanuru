from extensions import db



class ProfilDesa(db.Model):


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    nama_desa = db.Column(
        db.String(200)
    )


    deskripsi = db.Column(
        db.Text
    )


    sejarah = db.Column(
        db.Text
    )


    visi = db.Column(
        db.Text
    )


    misi = db.Column(
        db.Text
    )


    kepala_desa = db.Column(
        db.String(200)
    )


    alamat = db.Column(
        db.Text
    )


    foto = db.Column(
        db.String(200)
    )


    maps = db.Column(
        db.Text
    )


    jumlah_penduduk = db.Column(
        db.Integer
    )


    jumlah_kk = db.Column(
        db.Integer
    )


    luas_wilayah = db.Column(
        db.String(100)
    )


    jumlah_dusun = db.Column(
        db.Integer
    )