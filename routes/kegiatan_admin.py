import os

from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app
)

from flask_login import login_required

from extensions import db

from models.kegiatan import Kegiatan
from models.dokumentasi import Dokumentasi

from helpers.upload import save_file



kegiatan_admin_bp = Blueprint(
    "kegiatan_admin",
    __name__,
    url_prefix="/admin/kegiatan"
)



# ==============================
# LIST KEGIATAN
# ==============================

@kegiatan_admin_bp.route("/")
@login_required
def index():

    data = Kegiatan.query.order_by(
        Kegiatan.tanggal.desc()
    ).all()


    return render_template(
        "admin/kegiatan/index.html",
        data=data
    )



# ==============================
# TAMBAH KEGIATAN
# ==============================

@kegiatan_admin_bp.route(
    "/tambah",
    methods=["GET", "POST"]
)
@login_required
def tambah():


    if request.method == "POST":


        # ======================
        # Upload Banner
        # ======================

        banner = request.files.get(
            "banner"
        )


        nama_banner = save_file(
            banner,
            "kegiatan"
        )



        # ======================
        # Simpan Kegiatan
        # ======================

        kegiatan = Kegiatan(

            nama=request.form["nama"],


            tanggal=datetime.strptime(

                request.form["tanggal"],

                "%Y-%m-%d"

            ).date(),


            kategori=request.form["kategori"],


            deskripsi=request.form["deskripsi"],


            banner=nama_banner

        )


        db.session.add(
            kegiatan
        )

        db.session.commit()



        # ======================
        # Upload Banyak Foto
        # ======================

        foto_list = request.files.getlist(
            "foto"
        )


        for foto in foto_list:


            nama_foto = save_file(

                foto,

                "kegiatan/dokumentasi"

            )



            if nama_foto:


                dokumentasi = Dokumentasi(

                    kegiatan_id=kegiatan.id,

                    foto=nama_foto

                )


                db.session.add(
                    dokumentasi
                )



        db.session.commit()



        return redirect(
            url_for(
                "kegiatan_admin.index"
            )
        )



    return render_template(
        "admin/kegiatan/tambah.html"
    )



# ==============================
# DETAIL KEGIATAN
# ==============================

@kegiatan_admin_bp.route(
    "/detail/<int:id>"
)
@login_required
def detail(id):


    kegiatan = Kegiatan.query.get_or_404(
        id
    )


    return render_template(
        "admin/kegiatan/detail.html",
        kegiatan=kegiatan
    )



# ==============================
# EDIT KEGIATAN
# ==============================

@kegiatan_admin_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit(id):


    kegiatan = Kegiatan.query.get_or_404(
        id
    )



    if request.method == "POST":


        kegiatan.nama = request.form["nama"]



        kegiatan.tanggal = datetime.strptime(

            request.form["tanggal"],

            "%Y-%m-%d"

        ).date()



        kegiatan.kategori = request.form["kategori"]



        kegiatan.deskripsi = request.form["deskripsi"]




        # ======================
        # Ganti Banner
        # ======================

        banner = request.files.get(
            "banner"
        )


        if banner and banner.filename:


            banner_baru = save_file(

                banner,

                "kegiatan"

            )


            if banner_baru:


                # hapus banner lama

                if kegiatan.banner:


                    file_lama = os.path.join(

                        current_app.config["UPLOAD_FOLDER"],

                        "kegiatan",

                        kegiatan.banner

                    )


                    if os.path.exists(
                        file_lama
                    ):

                        os.remove(
                            file_lama
                        )



                kegiatan.banner = banner_baru




        # ======================
        # Tambah Dokumentasi Baru
        # ======================

        foto_list = request.files.getlist(
            "foto"
        )


        for foto in foto_list:


            nama_foto = save_file(

                foto,

                "kegiatan/dokumentasi"

            )


            if nama_foto:


                dokumentasi = Dokumentasi(

                    kegiatan_id=kegiatan.id,

                    foto=nama_foto

                )


                db.session.add(
                    dokumentasi
                )



        db.session.commit()



        return redirect(
            url_for(
                "kegiatan_admin.detail",
                id=kegiatan.id
            )
        )



    return render_template(
        "admin/kegiatan/edit.html",
        kegiatan=kegiatan
    )



# ==============================
# HAPUS KEGIATAN
# ==============================

@kegiatan_admin_bp.route(
    "/hapus/<int:id>"
)
@login_required
def hapus(id):


    kegiatan = Kegiatan.query.get_or_404(
        id
    )



    # hapus banner

    if kegiatan.banner:


        banner_path = os.path.join(

            current_app.config["UPLOAD_FOLDER"],

            "kegiatan",

            kegiatan.banner

        )


        if os.path.exists(
            banner_path
        ):

            os.remove(
                banner_path
            )



    # hapus semua dokumentasi

    for foto in kegiatan.dokumentasi:


        foto_path = os.path.join(

            current_app.config["UPLOAD_FOLDER"],

            "kegiatan",

            "dokumentasi",

            foto.foto

        )


        if os.path.exists(
            foto_path
        ):

            os.remove(
                foto_path
            )



    db.session.delete(
        kegiatan
    )


    db.session.commit()



    return redirect(
        url_for(
            "kegiatan_admin.index"
        )
    )



# ==============================
# HAPUS SATU FOTO DOKUMENTASI
# ==============================

@kegiatan_admin_bp.route(
    "/hapus-foto/<int:id>"
)
@login_required
def hapus_foto(id):


    foto = Dokumentasi.query.get_or_404(
        id
    )


    file_path = os.path.join(

        current_app.config["UPLOAD_FOLDER"],

        "kegiatan",

        "dokumentasi",

        foto.foto

    )


    if os.path.exists(
        file_path
    ):

        os.remove(
            file_path
        )



    db.session.delete(
        foto
    )


    db.session.commit()



    return redirect(
        request.referrer
    )