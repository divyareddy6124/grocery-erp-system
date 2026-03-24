// ---------------- API URLs ---------------- //

var productListApiUrl = "http://127.0.0.1:5000/getProducts";
var productSaveApiUrl = "http://127.0.0.1:5000/insertProduct";
var productDeleteApiUrl = "http://127.0.0.1:5000/deleteProduct";

var uomListApiUrl = "http://127.0.0.1:5000/getUOM";

// ---------------- ON LOAD ---------------- //

$(document).ready(function () {
    loadProducts();
    loadUOM();
});

// ---------------- LOAD PRODUCTS ---------------- //

function loadProducts() {
    $.ajax({
        url: productListApiUrl,
        type: 'GET',
        success: function (response) {
            var table = $("#productTableBody");
            table.empty();

            response.forEach(function (product) {
                var row = `
                    <tr>
                        <td>${product.product_id}</td>
                        <td>${product.name}</td>
                        <td>${product.uom_name}</td>
                        <td>${product.price_per_unit}</td>
                        <td>
                            <button onclick="deleteProduct(${product.product_id})" class="btn btn-danger btn-sm">
                                Delete
                            </button>
                        </td>
                    </tr>
                `;
                table.append(row);
            });
        },
        error: function (err) {
            console.error("Error loading products:", err);
        }
    });
}

// ---------------- LOAD UOM ---------------- //

function loadUOM() {
    $.ajax({
        url: uomListApiUrl,
        type: 'GET',
        success: function (response) {
            var dropdown = $("#uom");
            dropdown.empty();

            response.forEach(function (uom) {
                dropdown.append(`<option value="${uom.uom_id}">${uom.uom_name}</option>`);
            });
        }
    });
}

// ---------------- SAVE PRODUCT ---------------- //

function saveProduct() {
    var data = {
        name: $("#productName").val(),
        uom_id: $("#uom").val(),
        price_per_unit: $("#price").val()
    };

    $.ajax({
        url: productSaveApiUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function () {
            alert("Product added successfully!");
            loadProducts();
        },
        error: function (err) {
            console.error("Error saving product:", err);
        }
    });
}

// ---------------- DELETE PRODUCT ---------------- //

function deleteProduct(productId) {
    $.ajax({
        url: productDeleteApiUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId }),
        success: function () {
            alert("Product deleted!");
            loadProducts();
        },
        error: function (err) {
            console.error("Error deleting product:", err);
        }
    });
}