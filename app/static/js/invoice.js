document.addEventListener("DOMContentLoaded", function () {

    const body = document.getElementById("invoice-body");
    const addButton = document.getElementById("add-row");

    function bindRow(row) {

        const product = row.querySelector(".product");
        const qty = row.querySelector(".qty");
        const price = row.querySelector(".price");
        const gst = row.querySelector(".gst");
        const remove = row.querySelector(".remove-row");

        function calculateRow() {

            const q = parseFloat(qty.value) || 0;
            const p = parseFloat(price.value) || 0;
            const g = parseFloat(gst.value) || 0;

            const subtotal = q * p;
            const total = subtotal + subtotal * g / 100;

            row.querySelector(".total").value =
                total.toFixed(2);

            calculateInvoice();
        }

        product.addEventListener("change", function () {

            const option =
                product.options[product.selectedIndex];

            price.value =
                option.dataset.price || 0;

            calculateRow();

        });

        qty.addEventListener("input", calculateRow);
        price.addEventListener("input", calculateRow);
        gst.addEventListener("input", calculateRow);

        remove.addEventListener("click", function () {

            if (
                document.querySelectorAll(".invoice-row").length > 1
            ) {
                row.remove();
                calculateInvoice();
            }

        });

    }

    function calculateInvoice() {

        let subtotal = 0;
        let gst = 0;

        document.querySelectorAll(".invoice-row")
            .forEach(function (row) {

                const q =
                    parseFloat(
                        row.querySelector(".qty").value
                    ) || 0;

                const p =
                    parseFloat(
                        row.querySelector(".price").value
                    ) || 0;

                const g =
                    parseFloat(
                        row.querySelector(".gst").value
                    ) || 0;

                subtotal += q * p;

                gst += q * p * g / 100;

            });

        document.getElementById("subtotal").value =
            subtotal.toFixed(2);

        document.getElementById("gst_total").value =
            gst.toFixed(2);

        document.getElementById("grand_total").value =
            (subtotal + gst).toFixed(2);

    }

    bindRow(document.querySelector(".invoice-row"));

    addButton.addEventListener("click", function () {

        const row =
            document.querySelector(".invoice-row");

        const clone =
            row.cloneNode(true);

        clone.querySelector(".product").selectedIndex = 0;
        clone.querySelector(".qty").value = 1;
        clone.querySelector(".price").value = 0;
        clone.querySelector(".gst").value = 18;
        clone.querySelector(".total").value = "0.00";

        body.appendChild(clone);

        bindRow(clone);

    });

});
document
.getElementById("invoice-form")
.addEventListener("submit", function () {

    const items = [];

    document
        .querySelectorAll(".invoice-row")
        .forEach(function (row) {

            const product =
                row.querySelector(".product");

            if (!product.value)
                return;

            items.push({

                product_id:
                    Number(product.value),

                quantity:
                    Number(
                        row.querySelector(".qty").value
                    ),

                unit_price:
                    Number(
                        row.querySelector(".price").value
                    ),

                gst_percent:
                    Number(
                        row.querySelector(".gst").value
                    ),

                line_total:
                    Number(
                        row.querySelector(".total").value
                    )

            });

        });

    document
        .getElementById("items-json")
        .value = JSON.stringify(items);

});