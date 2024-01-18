main.js
$(document).ready(function() {
    // Replace this with the actual protein sequence
    var proteinSequence = "MKTVRQERLKSIVRILERSKEPVSGAQDILSIRDQSETEV";

    // Display protein sequence
    $("#protein-sequence").text(proteinSequence);

    // Replace this with the actual Mean Squared Error value
    var mseValue = 0.123; // Example value
    $("#mse").text(mseValue.toFixed(4)); // Display MSE with 4 decimal places
});
