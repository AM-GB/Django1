"use strict";

window.onload = function () {
    console.log('DOM ready');
    $('.basket_record').on('change', "input[type='number']", function (event) {
        let qty = event.target.value;
        let productPk = event.target.name;
        console.log(productPk, qty);
    });
}
