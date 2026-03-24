// Load orders when page opens
window.onload = function () {
    displayOrders();
};

// Place Order Function
function placeOrder() {
    let product = document.getElementById("product").value;
    let qty = document.getElementById("qty").value;

    if (!product || !qty) {
        alert("Please enter all details");
        return;
    }

    // Get products (for price)
    let products = JSON.parse(localStorage.getItem("products")) || [];

    let selectedProduct = products.find(p => p.name === product);

    if (!selectedProduct) {
        alert("Product not found");
        return;
    }

    let price = selectedProduct.price;
    let total = qty * price;

    // Get existing orders
    let orders = JSON.parse(localStorage.getItem("orders")) || [];

    let id = orders.length + 1;

    let order = {
        id: id,
        product: product,
        qty: qty,
        total: total
    };

    orders.push(order);

    localStorage.setItem("orders", JSON.stringify(orders));

    displayOrders();
}

// Display Orders
function displayOrders() {
    let orders = JSON.parse(localStorage.getItem("orders")) || [];

    let table = document.getElementById("orderTable");

    table.innerHTML = "";

    orders.forEach(order => {
        let row = `
            <tr>
                <td>${order.id}</td>
                <td>${order.product}</td>
                <td>${order.qty}</td>
                <td>${order.total}</td>
            </tr>
        `;

        table.innerHTML += row;
    });
}