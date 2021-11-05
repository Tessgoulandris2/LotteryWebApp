// JavaScript function to generate 6 random unique values in order and populate form
function luckyDip() {
    var array = new Uint32Array(6);
    window.crypto.getRandomValues(array);

    let draw = new Set();
    for (var i = 0; i < array.length; i++) {
      draw.add((array[i] % 60) + 1);
    }
    // turn set into an array
    let a = Array.from(draw);

    // sort array into size order
    a.sort(function (a, b) {
        return a - b;
    });

    // add values to fields in create draw form
    for (let i = 0; i < 6; i++) {
        document.getElementById("no" + (i + 1)).value = a[i];
    }
}