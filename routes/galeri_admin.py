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


from models.galeri import Galeri


from helpers.upload import save_file



galeri_admin_bp = Blueprint(

    "galeri_admin",

    __name__,

    url_prefix="/admin/galeri"

)


@galeri_admin_bp.route("/")
@login_required
def index():


    data = Galeri.query.all()


    return render_template(
        "admin/galeri/index.html",
        data=data
    )


@galeri_admin_bp.route(
    "/tambah",
    methods=["GET","POST"]
)
@login_required
def tambah():


    if request.method=="POST":


        foto = request.files.get(
            "foto"
        )


        nama_file = save_file(

            foto,

            "galeri"

        )



        galeri = Galeri(

            judul=request.form["judul"],

            deskripsi=request.form["deskripsi"],

            kategori=request.form["kategori"],

            foto=nama_file

        )



        db.session.add(
            galeri
        )


        db.session.commit()



        return redirect(
            url_for(
                "galeri_admin.index"
            )
        )



    return render_template(
        "admin/galeri/tambah.html"
    )


@galeri_admin_bp.route(
    "/hapus/<int:id>"
)
@login_required
def hapus(id):


    galeri = Galeri.query.get_or_404(
        id
    )


    import os


    lokasi = os.path.join(

        current_app.config["UPLOAD_FOLDER"],

        "galeri",

        galeri.foto

    )


    if os.path.exists(lokasi):

        os.remove(lokasi)



    db.session.delete(
        galeri
    )


    db.session.commit()



    return redirect(
        url_for(
            "galeri_admin.index"
        )
    )