import os
import io
from flask import Flask, request, redirect, url_for, Response

from .csv_parse import convert_csv_to_aba
from .util import MissingFields, get_form_fields

app = Flask(__name__)
# app.debug = True

BAD_REQUEST = 400

FILE_FIELD = 'csv_file'

@app.route("/csv_to_aba", methods=['GET', 'POST'])
def csv_to_aba():
    if request.method == 'POST':
        # Check if the post request has the file part
        if FILE_FIELD not in request.files:
            return "No file uploaded", BAD_REQUEST

        csv_file = request.files[FILE_FIELD]

        # Check that the user selected a file
        if csv_file.filename == '':
            return "No file selected", BAD_REQUEST

        # Grab the other form parameters
        try:
            [sender_name, sender_account, sender_bsb, sender_bank] = get_form_fields(request, [
                "sender_name", "sender_account", "sender_bsb", "sender_bank"
            ])
        except MissingFields as ex:
            return ex.message, BAD_REQUEST

        # Convert uploaded byte-stream to a Python string (not very efficient, but hey).
        csv_stream = io.StringIO(csv_file.read().decode("utf-8-sig"))

        result = convert_csv_to_aba(
            csv_stream,
            sender_name=sender_name, sender_account=sender_account,
            sender_bsb=sender_bsb, sender_bank=sender_bank
        )

        # Use the uploaded file's name with an ABA extension for the result.
        basename, _ = os.path.splitext(csv_file.filename)
        result_filename = basename + ".aba"

        response = Response(result, mimetype="text/plain")
        response.headers["Content-Disposition"] = 'attachment; filename="{}"'.format(result_filename)
        return response

    return '''
    <!doctype html>
    <title>CSV to ABA</title>
    <h1>Convert CSV to ABA</h1>
    <form method=post enctype=multipart/form-data>
      <p>
        Your Name
        <input type=text name="sender_name"><br>
        Your Account Number
        <input type=text name="sender_account"><br>
        Your BSB (xxx-xxx)
        <input type=text name="sender_bsb"><br>
        Your 3 Letter Bank Code, e.g. BEN
        <input type=text name="sender_bank"><br>
        CSV file to convert
        <input type=file name="csv_file"><br>
        <input type=submit value=Convert>
      </p>
    </form>
    '''
