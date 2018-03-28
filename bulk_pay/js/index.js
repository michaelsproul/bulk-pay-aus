import Papa from 'papaparse';
import $ from 'jquery';

const csv_headers = ["name", "acct", "bsb", "bankcode", "acpa", "description"];

const empty_account = {name: "", acct: "", bsb: "", bankcode: "", acpa: "", description: ""};

function missingColumns(header) {
    return csv_headers.filter((h) => !header.includes(h));
}

function handlePrefillFile(files) {
    Papa.parse(files[0], {
        header: true,
        skipEmptyLines: true,
        complete: function(results, file) {
            let missingCols = missingColumns(results.meta.fields);
            if (missingCols.length > 0) {
                alert(`Sorry, your prefill CSV is missing the following columns: ${missingCols}`);
                return;
            }

            let select = document.getElementById("account-selector");
            select.options.length = 1;
            select.accountData = results.data;

            results.data.forEach((row, idx) => {
                console.log(row);

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
    // Mapping from HTML field names to account property names
    let fieldMappings = [
        ["sender_name", "name"],
        ["sender_account", "acct"],
        ["sender_bsb", "bsb"],
        ["sender_bank", "bankcode"],
        ["acpa_number", "acpa"],
        ["batch_description", "description"]
    ];
    for (let m of fieldMappings) {
        let htmlField = m[0], propName = m[1];
        let value = account.hasOwnProperty(propName) ? account[propName] : "";
        setField(htmlField, value);
    }
}

// Populate the account selector if the user has an accounts file already loaded
$(window).on("load", () => {
    let accountCsv = $("#prefiller input[name=prefill_csv]")[0];
    if (accountCsv.files.length > 0) {
        handlePrefillFile(accountCsv.files);
    }
});

// Exports
window.handlePrefillFile = handlePrefillFile;
window.handleAccountSelect = handleAccountSelect;
window.$ = $;
