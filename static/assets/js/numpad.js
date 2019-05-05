$(document).ready(function() {
    console.log("numpad.js");
});

$(document).on('click', '.letter', function() {
    console.log("click letter");
    var letter = $(this);
    var str = letter.text();
    var amountInput = $("#amount");
    amountInput.val(amountInput.val() + str);
});

$(document).on('click', '.delete', function() {
    console.log("click delete");
    var amountInput = $("#amount");
    var text = amountInput.val();
    amountInput.val(text.slice(0, -1));
});
