import csv
import aba.records
from datetime import datetime
from aba.generator import AbaFile
from aba.fields import RemitterName, PayeeName

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

def validate_record(rec, message):
    try:
        rec.render_to_string()
    except aba.exceptions.ValidationError:
        raise ValidationError(message)

# headers: bsb, account number, name, amount in cents, comment
def convert_csv_to_aba(csv_data, sender_name, sender_account, sender_bsb, sender_bank,
                       batch_description=""):
    reader = csv.reader(csv_data)
    records = []

    # TODO: tell the user if their name is truncated
    sender_name = sender_name[:RemitterName.length]

    for [bsb, account_num, name, amount, txn_reference] in reader:
        print("Processing {}, {}, {}, {}".format(bsb, account_num, name, amount))

        # TODO: tell the user
        if len(name) > PayeeName.length:
            print("WARNING: truncating name: {}".format(name))
            name = name[:PayeeName.length]

        rec = aba.records.DetailRecord(
            bsb=bsb,
            account_number=account_num,
            txn_code='53', # some magic number
            amount=amount,
            payee_name=name,
            lodgment_ref=txn_reference,
            sender_bsb=sender_bsb,
            sender_account=sender_account,
            remitter_name=sender_name
        )

        # Validate the record.
        validate_record(
            rec, "Record not valid: {}, {}, {}, {}".format(bsb, account_num, name, amount)
        )

        records.append(rec)

    header = aba.records.DescriptiveRecord(
        user_bank=sender_bank,
        user_name=sender_name,
        user_number=0, # No ACPA number
        description=batch_description,
        date=datetime.now().date()
    )

    validate_record(header, "Header not valid")

    aba_file = AbaFile(header)
    for record in records:
        aba_file.add_record(record)

    try:
        return aba_file.render_to_string()
    except aba.exceptions.ValidationError:
        raise ValidationError("Unable to create ABA file")
