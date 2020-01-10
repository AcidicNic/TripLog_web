function textAreaAdjust(text) {
    var notes = document.getElementById('note_container');
    text.style.height = 'auto';
    notes.style.marginBottom = text.scrollHeight + 20 + "px";
    text.style.height = text.scrollHeight+'px';
    window.scrollTo(0,document.body.scrollHeight);
}

$("#note_input").keydown(function(e){
    if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault();
        $('#add_note').submit();
    }
});
function showDoses() {
    var dose_wrapper = document.getElementById('dose_wrapper');
    if (dose_wrapper.style.display === 'none') {
        dose_wrapper.style.display = 'inline';
    }
    else {
        dose_wrapper.style.display = 'none';
    }
}

function addDose() {
    dose_divs = document.getElementsByClassName("dose_div");
    if (dose_divs.length >= 6) {
        for (var i = 0; i < dose_divs.length; i++) {
            var dose_input = dose_divs[i];
            if (dose_input.style.display === 'none') {
                dose_input.style.display = 'flex';
                break;
            }
        }
    }
}

function rmDose() {
    dose_divs = document.getElementsByClassName("dose_div");
    if (dose_divs.length > 1) {
        for (var i = dose_divs.length - 1; i >= 0; i--) {
            var dose_input = dose_divs[i];
            if (dose_input.style.display !== 'none') {
                dose_input.style.display = 'none';
                break;
            }
        }
    }
}

var drugs = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: drug_list
});
drugs.initialize();

$('.drug_dropdown').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'drugs',
        source: drugs
    }
);