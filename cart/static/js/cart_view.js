{/* <script>

    $(document).on('click', '.delete-button', function(e){
        e.preventDefault();

    $.ajax({
        type: 'POST',
    url: '{% url "cart:delete-to-cart" %}',
    data: {
        product_id: $(this).data('index'),
    csrfmiddlewaretoken: '{{ csrf_token }}',
    action: 'post'
            },
    success: function(response){
        document.getElementById('lblCartCount').textContent = response.qty
                document.getElementById('total').textContent = response.total

    location.reload()
            },
    error: function(error, status){
        console.log(error)
    }
        })
    });

    $(document).on('click', '.update-button', function(e){
        e.preventDefault();

    var product_id = $(this).data('index')

    $.ajax({
        type: 'POST',
    url: '{% url "cart:update-to-cart" %}',
    data: {
        product_id: $(this).data('index'),
    product_qty: $('#select'+product_id+ ' option:selected').text(),
    csrfmiddlewaretoken: '{{ csrf_token }}',
    action: 'post'
            },
    success: function(response){
        document.getElementById('lblCartCount').textContent = response.qty
                document.getElementById('total').textContent = response.total

    location.reload()
            },
    error: function(error, status){
        console.log(error)
    }
        })
    });
</script> */}