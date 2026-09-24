// ==========================================
// SUPERMART JAVASCRIPT
// ==========================================


// ==========================================
// INCREASE QUANTITY
// ==========================================

function increaseQuantity() {

    const quantityInput =
        document.getElementById("quantity");

    const orderQuantity =
        document.getElementById("order-quantity");


    // Quantity input இல்லையென்றால் stop

    if (!quantityInput) {
        return;
    }


    const currentQuantity =
        parseInt(quantityInput.value) || 1;


    const maxQuantity =
        parseInt(quantityInput.max) || 1;


    // Increase only up to available stock

    if (currentQuantity < maxQuantity) {

        quantityInput.value =
            currentQuantity + 1;


        // Update hidden order quantity if it exists

        if (orderQuantity) {

            orderQuantity.value =
                quantityInput.value;

        }

    }

}


// ==========================================
// DECREASE QUANTITY
// ==========================================

function decreaseQuantity() {

    const quantityInput =
        document.getElementById("quantity");

    const orderQuantity =
        document.getElementById("order-quantity");


    // Quantity input இல்லையென்றால் stop

    if (!quantityInput) {
        return;
    }


    const currentQuantity =
        parseInt(quantityInput.value) || 1;


    // Minimum quantity is 1

    if (currentQuantity > 1) {

        quantityInput.value =
            currentQuantity - 1;


        // Update hidden order quantity if it exists

        if (orderQuantity) {

            orderQuantity.value =
                quantityInput.value;

        }

    }

}


// ==========================================
// DELETE CONFIRMATION
// ==========================================

function confirmDelete(productName) {

    return confirm(
        "Are you sure you want to delete " +
        productName +
        "?"
    );

}