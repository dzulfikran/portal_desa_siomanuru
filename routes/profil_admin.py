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


from models.profil import ProfilDesa


from helpers.upload import save_file



profil_admin_bp = Blueprint(
    "profil_admin",
    __name__,
    url_prefix="/admin/profil"
)



# ==========================
# EDIT PROFIL DESA
# ==========================

@profil_admin_bp.route(
    "/",
    methods=["GET", "POST"]
)
@login_required
def index():


    profil = ProfilDesa.query.first()



    # Jika belum ada data
    if profil is None:


        profil = ProfilDesa(

            nama_desa="",

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




    if request.method == "POST":


        profil.nama_desa = request.form["nama_desa"]


        profil.deskripsi = request.form["deskripsi"]


        profil.sejarah = request.form["sejarah"]


        profil.visi = request.form["visi"]


        profil.misi = request.form["misi"]


        profil.kepala_desa = request.form["kepala_desa"]


        profil.alamat = request.form["alamat"]


        profil.maps = request.form["maps"]




        profil.jumlah_penduduk = request.form["jumlah_penduduk"]


        profil.jumlah_kk = request.form["jumlah_kk"]


        profil.luas_wilayah = request.form["luas_wilayah"]


        profil.jumlah_dusun = request.form["jumlah_dusun"]





        # ======================
        # Ganti Foto Profil
        # ======================

        foto = request.files.get(
            "foto"
        )



        if foto and foto.filename:


            foto_baru = save_file(

                foto,

                "profil"

            )



            if foto_baru:


                # hapus foto lama

                if profil.foto:


                    lokasi_lama = os.path.join(

                        current_app.config["UPLOAD_FOLDER"],

                        "profil",

                        profil.foto

                    )


                    if os.path.exists(
                        lokasi_lama
                    ):

                        os.remove(
                            lokasi_lama
                        )



                profil.foto = foto_baru




        db.session.commit()



        return redirect(
            url_for(
                "profil_admin.index"
            )
        )




    return render_template(
        "admin/profil/index.html",
        profil=profil
    )