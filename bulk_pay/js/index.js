import Papa from 'papaparse';
import $ from 'jquery';

const csv_headers = ["name", "acct", "bsb", "bankcode", "acpa", "description"];

const empty_account = {name: "", acct: "", bsb: "", bankcode: "", acpa: "", description: ""}

function rowOk(row) {
    return csv_headers.every((header) => row.hasOwnProperty(header));
}

function handlePrefillFile(files) {
    Papa.parse(files[0], {
        header: true,
        skipEmptyLines: true,
        complete: function(results, file) {
            let select = document.getElementById("account-selector");
            select.accountData = results.data;

            results.data.forEach((row, idx) => {
                console.log(row);

                if (!rowOk(row)) {
                    // FIXME: error message
                    alert(`Row ${idx} is invalid`);
                    return;
                }

                // Add to the select
                let option = document.createElement("option");
                option.text = `${row.name} | ${row.acct}`;
                option.value = idx;
                select.add(option);
            });
        },
        error: function(err, file) {
            window.alert("Sorry but the prefill file you've uploaded is invalid");
            console.log("Error at row {}: {}", err.row, err.message);
        }
    });
}

function handleAccountSelect(select) {
    let idx = select.value;
    let account = (idx == -1) ? empty_account : select.accountData[idx];
    prefillForm(account);
}

function prefillForm(account) {
    let form = $("#main-form");
    let setField = (fieldName, value) => {
        form.find(`input[name=${fieldName}]`)[0].value = value;
    };
    setField("sender_name", account.name);
    setField("sender_account", account.acct);
    setField("sender_bsb", account.bsb);
    setField("sender_bank", account.bankcode);
    setField("acpa_number", account.acpa);
    setField("batch_description", account.description);
}

// Populate the account selector if the user has an accounts file already loaded
$(document).ready(() => {
    let accountCsv = $("#prefiller input[name=prefill_csv]");
    if (accountCsv.files.length > 0) {
        handlePrefillFile(accountCsv.files);
    }
});

// Exports
window.handlePrefillFile = handlePrefillFile;
window.handleAccountSelect = handleAccountSelect;
// window.jQuery = $;
