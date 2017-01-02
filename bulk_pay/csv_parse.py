import csv
import aba.records
from datetime import datetime
from aba.generator import AbaFile

# headers: bsb, account number, name, amount in cents, comment
def convert_csv_to_aba(csv_data, sender_name, sender_account, sender_bsb, sender_bank,
                       batch_description="", txn_reference=""):
    reader = csv.reader(csv_data)
    records = []
    for [bsb, account_num, name, amount] in reader:
        print("Processing {}, {}, {}, {}".format(bsb, account_num, name, amount))

        if len(name) > 32:
            print("WARNING: truncating name: {}".format(name))
            name = name[:32]

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
        try:
            rec.render_to_string()
        except aba.exceptions.ValidationError:
            # TODO: propagate this error
            print("Record not valid: {}, {}, {}, {}".format(bsb, account_num, name, amount))

        records.append(rec)

    header = aba.records.DescriptiveRecord(
        user_bank=sender_bank,
        user_name=sender_name,
        user_number=0, # No ACPA number
        description=batch_description,
        date=datetime.now().date()
    )

    aba_file = AbaFile(header)
    for record in records:
        aba_file.add_record(record)

    return aba_file.render_to_string()
