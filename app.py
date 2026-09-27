from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from flask_login import current_user
from extensions import db, login_manager

import calendar

# db = SQLAlchemy()
from routes.admin import admin_bp
from routes.umkm_admin import umkm_admin_bp
from routes.kegiatan_admin import kegiatan_admin_bp
from routes.profil_admin import profil_admin_bp
from routes.galeri_admin import galeri_admin_bp
from routes.dashboard_admin import dashboard_admin_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "admin.login"

    return app


app=create_app()

from models.user import User
from models.profil import ProfilDesa
from models.umkm import UMKM
from models.kegiatan import Kegiatan
from models.dokumentasi import Dokumentasi
from models.galeri import Galeri
from models.pengaturan import Pengaturan


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

with app.app_context():

    db.create_all()

    if User.query.count() == 0:

        admin = User(
            username="admin",
            password="admin123"
        )

        db.session.add(admin)

        db.session.commit()

    if ProfilDesa.query.count()==0:

        profil = ProfilDesa(

            nama_desa="Desa Siomanuru",

            deskripsi="",

            sejarah="",

            visi="",

            misi="",

            kepala_desa="",

            alamat="",

            maps="",

            jumlah_penduduk=0,

            jumlah_kk=0,

            luas_wilayah="",

            jumlah_dusun=0
        )


        db.session.add(
            profil
        )


        db.session.commit()

app.register_blueprint(admin_bp)

app.register_blueprint(
    umkm_admin_bp
)

app.register_blueprint(
    kegiatan_admin_bp
)

app.register_blueprint(
    profil_admin_bp
)

app.register_blueprint(
    galeri_admin_bp
)

app.register_blueprint(
    dashboard_admin_bp
)

@app.route("/")
def home():


    profil = ProfilDesa.query.first()



    umkm = UMKM.query.limit(3).all()



    kegiatan = Kegiatan.query.order_by(

        Kegiatan.tanggal.desc()

    ).limit(3).all()



    galeri = Galeri.query.limit(6).all()



    return render_template(

        "index.html",

        profil=profil,

        umkm=umkm,

        kegiatan=kegiatan,

        galeri=galeri

    )



@app.route("/profil")
def profil():


    data = ProfilDesa.query.first()



    return render_template(

        "profil.html",

        profil=data

    )



@app.route("/umkm")
def umkm():

    data = UMKM.query.all()


    return render_template(
        "umkm.html",
        data=data
    )



@app.route("/kegiatan")
def kegiatan():


    sekarang = datetime.now()


    bulan = request.args.get(
        "bulan",
        default=sekarang.month,
        type=int
    )


    tahun = request.args.get(
        "tahun",
        default=sekarang.year,
        type=int
    )


    kalender = calendar.monthcalendar(
        tahun,
        bulan
    )



    kegiatan = Kegiatan.query.filter(
        db.extract(
            "month",
            Kegiatan.tanggal
        ) == bulan
    ).filter(
        db.extract(
            "year",
            Kegiatan.tanggal
        ) == tahun
    ).order_by(
        Kegiatan.tanggal.asc()
    ).all()



    return render_template(
        "kegiatan.html",

        kalender=kalender,

        kegiatan=kegiatan,

        bulan=bulan,

        tahun=tahun

    )


@app.route("/kegiatan/bulan/<int:tahun>/<int:bulan>")
def kegiatan_bulan(tahun, bulan):

    return redirect(
        url_for(
            "kegiatan",
            tahun=tahun,
            bulan=bulan
        )
    )


def pindah_bulan(bulan, tahun, arah):

    bulan += arah


    if bulan < 1:
        bulan = 12
        tahun -= 1


    elif bulan > 12:
        bulan = 1
        tahun += 1


    return bulan, tahun


@app.context_processor
def utility_processor():

    def nama_bulan(bulan):

        daftar = [
            "",
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni",
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember"
        ]

        return daftar[bulan]



    def pindah(bulan,tahun,arah):

        bulan += arah


        if bulan < 1:

            bulan = 12
            tahun -= 1


        if bulan > 12:

            bulan = 1
            tahun += 1


        return {
            "bulan":bulan,
            "tahun":tahun
        }



    return dict(
        nama_bulan=nama_bulan,
        pindah=pindah
    )


@app.errorhandler(
    RequestEntityTooLarge
)
def file_too_large(error):

    return """
    <h3>
    File terlalu besar
    </h3>

    <p>
    Maksimal upload adalah 5 MB.
    </p>
    """, 413


@app.route("/galeri")
def galeri():


    data = Galeri.query.all()


    return render_template(
        "galeri.html",
        data=data
    )


if __name__=="__main__":

    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)