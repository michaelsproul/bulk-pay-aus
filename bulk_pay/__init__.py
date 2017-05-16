import os
import io
import flask
from aba.fields import AccountNumber, BSB, Description, RemitterName, UserBank, UserNumber
from flask import Flask, request, redirect, url_for, Response, render_template

from .csv_parse import convert_csv_to_aba, ValidationError
from .util import MissingFields, get_form_fields
from .encoding import decode_file

app = Flask(__name__)
# app.debug = True

FILE_FIELD = 'csv_file'

# Length limits for fields (injected into the HTML).
class LengthLimits:
    sender_name = RemitterName.length
    account_num = AccountNumber.length
    bsb = BSB.length
    bank_code = UserBank.length
    acpa_number = UserNumber.length
    description = Description.length

def error(message):
    return render_template("error.html", message=message), 400

@app.route("/", methods=['GET', 'POST'])
def csv_to_aba():
    if request.method == 'POST':
        # Check if the post request has the file part
        if FILE_FIELD not in request.files:
            return error("No file uploaded")

        csv_file = request.files[FILE_FIELD]

        # Check that the user selected a file
        if csv_file.filename == '':
            return error("No file selected")

        # Grab the other form parameters
        try:
            fields = get_form_fields(request, [
                    "sender_name", "sender_account", "sender_bsb", "sender_bank",
                    "acpa_number", "batch_description"
            ])
            [sender_name, sender_account, sender_bsb, sender_bank,
             acpa_number, batch_description] = fields
        except MissingFields as ex:
            return error(ex.message)

        # Extract strict mode bool
        strict_mode = True if request.form.get("strict_mode") == "on" else False

        # Convert uploaded byte-stream to a Python string (not very efficient, but hey).
        csv_stream = io.StringIO(decode_file(csv_file.read()))

        try:
            result = convert_csv_to_aba(
                csv_stream,
                sender_name=sender_name, sender_account=sender_account,
                sender_bsb=sender_bsb, sender_bank=sender_bank,
                acpa_number=acpa_number,
                batch_description=batch_description, strict=strict_mode
            )
        except ValidationError as ex:
            return error(ex.message)

        # Use the uploaded file's name with an ABA extension for the result.
        basename, _ = os.path.splitext(csv_file.filename)
        result_filename = basename + ".aba"

        response = Response(result, mimetype="text/plain")
        response.headers["Content-Disposition"] = 'attachment; filename="{}"'.format(result_filename)
        return response

    return render_template("index.html", limits=LengthLimits)
