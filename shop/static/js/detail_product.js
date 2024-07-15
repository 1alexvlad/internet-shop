$(document).on('click', '#add-button', function (e) {
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: '{% url "cart:add-to-cart" %}',
        data: {
            product_id: $('#add-button').val(),
            product_qty: $('#select option:selected').text(),
            csrfmiddlewaretoken: '{{ csrf_token }}',
            action: 'post'
        },
        success: function (response) {
            document.getElementById('lblCartCount').textContent = response.qty
        },
        error: function (error) {
            console.log(error)
        }
    })
})