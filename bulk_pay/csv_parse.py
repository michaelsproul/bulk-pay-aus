import csv
import aba.records
from datetime import datetime
from aba.generator import AbaFile
from aba.fields import RemitterName, PayeeName, LodgmentRef

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

def validate_record(rec, message):
    try:
        rec.render_to_string()
    except aba.exceptions.ValidationError:
        raise ValidationError(message)

def check_field(field_name, field_value, length_limit, strict):
    """Check that a field's value fits within the length limit. Return the updated field value.

    In strict mode, an exception will be raised if the field is too long.
    In non-strict mode, the field will be truncated.
    """
    if strict:
        if len(field_value) > length_limit:
            raise ValidationError(
                "{} is too long: {}, length is {}, max length is {}".format(
                    field_name, repr(field_value), len(field_value), length_limit
                )
            )
        else:
            return field_value

    return field_value[:length_limit]

# headers: bsb, account number, name, amount in cents, comment
def convert_csv_to_aba(csv_data, sender_name, sender_account, sender_bsb, sender_bank,
                       batch_description="", strict=True):
    reader = csv.reader(csv_data)
    records = []

    sender_name = check_field("Sender name", sender_name, RemitterName.length, strict)

    for row in reader:
        if len(row) != 5:
            raise ValidationError("Wrong number of columns in row: {}, expected 5".format(row))
        [bsb, account_num, name, amount, txn_reference] = row

        print("Processing {}".format(row))

        # Check/truncate the recipient name
        name = check_field("Recipient name", name, PayeeName.length, strict)

        txn_reference = check_field(
            "Transaction reference", txn_reference, LodgmentRef.length, strict
        )

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
        validate_record(rec, "Record not valid: {}".format(row))

        records.append(rec)

    header = aba.records.DescriptiveRecord(
        user_bank=sender_bank,
        user_name=sender_name,
        user_number=0, # No ACPA number
        description=batch_description,
        date=datetime.now().date()
    )

    validate_record(
        header, "Sender information not valid, name: {}, bank: {}, description: {}".format(
            sender_name, sender_bank, batch_description
        )
    )

    aba_file = AbaFile(header)
    for record in records:
        aba_file.add_record(record)

    try:
        return aba_file.render_to_string()
    except aba.exceptions.ValidationError:
        raise ValidationError("Unable to format records into ABA file")
