from flask import (
    Blueprint,
    render_template
)


from flask_login import login_required


from models.umkm import UMKM

from models.kegiatan import Kegiatan

from models.galeri import Galeri

from models.profil import ProfilDesa



dashboard_admin_bp = Blueprint(

    "dashboard_admin",

    __name__,

    url_prefix="/admin"

)



@dashboard_admin_bp.route("/")

@login_required
def index():


    jumlah_umkm = UMKM.query.count()


    jumlah_kegiatan = Kegiatan.query.count()


    jumlah_galeri = Galeri.query.count()


    profil = ProfilDesa.query.first()



    return render_template(

        "admin/dashboard.html",

        jumlah_umkm=jumlah_umkm,

        jumlah_kegiatan=jumlah_kegiatan,

        jumlah_galeri=jumlah_galeri,

        profil=profil

    )