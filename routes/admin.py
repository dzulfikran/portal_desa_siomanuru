from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from models.user import User

from extensions import db


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)



@admin_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        user = User.query.filter_by(
            username=username
        ).first()


        if user and user.password == password:

            login_user(user)

            return redirect(
                url_for("admin.dashboard")
            )


        flash(
            "Username atau password salah"
        )


    return render_template(
        "admin/login.html"
    )




@admin_bp.route("/dashboard")
@login_required
def dashboard():


    return render_template(
        "admin/dashboard.html"
    )



@admin_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("admin.login")
    )




@admin_bp.route(
    "/pengaturan",
    methods=["GET","POST"]
)
@login_required
def pengaturan():


    user = current_user



    if request.method == "POST":


        username_baru = request.form["username"]


        password_lama = request.form["password_lama"]


        password_baru = request.form["password_baru"]




        # cek password lama

        if password_lama != user.password:


            flash(
                "Password lama tidak sesuai"
            )


            return redirect(
                url_for(
                    "admin.pengaturan"
                )
            )




        # cek username

        username_cek = User.query.filter(

            User.username == username_baru,

            User.id != user.id

        ).first()



        if username_cek:


            flash(
                "Username sudah digunakan"
            )


            return redirect(
                url_for(
                    "admin.pengaturan"
                )
            )




        user.username = username_baru



        if password_baru:


            user.password = password_baru



        db.session.commit()



        flash(
            "Data akun berhasil diperbarui"
        )


        return redirect(
            url_for(
                "admin.pengaturan"
            )
        )



    return render_template(
        "admin/pengaturan.html",
        user=user
    )