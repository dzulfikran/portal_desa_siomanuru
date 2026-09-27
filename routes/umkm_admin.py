import os


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


from models.umkm import UMKM


from helpers.upload import save_file



umkm_admin_bp = Blueprint(
    "umkm_admin",
    __name__,
    url_prefix="/admin/umkm"
)



# ==========================
# LIST UMKM
# ==========================

@umkm_admin_bp.route("/")
@login_required
def index():


    data = UMKM.query.all()



    return render_template(
        "admin/umkm/index.html",
        data=data
    )



# ==========================
# TAMBAH UMKM
# ==========================

@umkm_admin_bp.route(
    "/tambah",
    methods=["GET","POST"]
)
@login_required
def tambah():


    if request.method == "POST":


        foto = request.files.get(
            "foto"
        )


        nama_foto = save_file(
            foto,
            "umkm"
        )



        umkm = UMKM(

            nama_produk=request.form["nama_produk"],

            deskripsi=request.form["deskripsi"],

            harga=request.form["harga"],

            nama_pemilik=request.form["nama_pemilik"],

            alamat=request.form["alamat"],

            nomor_hp=request.form["nomor_hp"],

            foto=nama_foto

        )



        db.session.add(
            umkm
        )


        db.session.commit()



        return redirect(
            url_for(
                "umkm_admin.index"
            )
        )



    return render_template(
        "admin/umkm/tambah.html"
    )



# ==========================
# EDIT UMKM
# ==========================

@umkm_admin_bp.route(
    "/edit/<int:id>",
    methods=["GET","POST"]
)
@login_required
def edit(id):


    umkm = UMKM.query.get_or_404(
        id
    )



    if request.method == "POST":


        umkm.nama_produk = request.form["nama_produk"]


        umkm.deskripsi = request.form["deskripsi"]


        umkm.harga = request.form["harga"]


        umkm.nama_pemilik = request.form["nama_pemilik"]


        umkm.alamat = request.form["alamat"]


        umkm.nomor_hp = request.form["nomor_hp"]




        # ======================
        # Ganti Foto
        # ======================

        foto = request.files.get(
            "foto"
        )


        if foto and foto.filename:


            foto_baru = save_file(

                foto,

                "umkm"

            )



            if foto_baru:



                # hapus foto lama

                if umkm.foto:


                    foto_lama = os.path.join(

                        current_app.config["UPLOAD_FOLDER"],

                        "umkm",

                        umkm.foto

                    )



                    if os.path.exists(
                        foto_lama
                    ):

                        os.remove(
                            foto_lama
                        )



                umkm.foto = foto_baru




        db.session.commit()



        return redirect(
            url_for(
                "umkm_admin.index"
            )
        )



    return render_template(
        "admin/umkm/edit.html",
        umkm=umkm
    )



# ==========================
# HAPUS UMKM
# ==========================

@umkm_admin_bp.route(
    "/hapus/<int:id>"
)
@login_required
def hapus(id):


    umkm = UMKM.query.get_or_404(
        id
    )



    # hapus file foto

    if umkm.foto:


        file_path = os.path.join(

            current_app.config["UPLOAD_FOLDER"],

            "umkm",

            umkm.foto

        )



        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )



    db.session.delete(
        umkm
    )


    db.session.commit()



    return redirect(
        url_for(
            "umkm_admin.index"
        )
    )