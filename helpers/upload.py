import os
import uuid

from flask import current_app



def allowed_file(filename):

    return (
        "."
        in filename
        and
        filename.rsplit(".",1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )



def save_file(file, folder):


    if not file or file.filename == "":

        return None



    if not allowed_file(file.filename):

        return None



    extension = file.filename.rsplit(
        ".",
        1
    )[1].lower()



    filename = (
        str(uuid.uuid4())
        +
        "."
        +
        extension
    )



    folder_path = os.path.join(

        current_app.config["UPLOAD_FOLDER"],

        folder

    )


    os.makedirs(
        folder_path,
        exist_ok=True
    )



    file.save(
        os.path.join(
            folder_path,
            filename
        )
    )


    return filename