
function updateSubtotal(quantityInput){
    const row=quantityInput.closest('tr');
    const price=parseFloat(row.querySelector('td:nth-child(3)').textContent);
    const quantity=parseInt(quantityInput.value);
    const subtotal=price*quantity;
    row.querySelector('.subtotal').value=subtotal.toFixed(2);
    updateTotal();
}

function updateTotal(){
    let total=0;
    document.querySelectorAll('.subtotal').forEach(function(subtotalInput){
        total+=parseFloat(subtotalInput.value);
    });
    const gst= total * 0.18;
    const invoiceTotal= total + gst;

    document.getElementById('total-value').textContent=total.toFixed(2);
    document.getElementById('gst-value').textContent=gst.toFixed(2);
    document.getElementById('invoice-total-value').textContent=invoiceTotal.toFixed(2);
}

updateTotal();