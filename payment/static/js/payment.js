$(document).on('submit', function (e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '{% url "payment:complete-order" %}',
        data: {
            name: $('#name').val(),
            email: $('#email').val(),
            street_address: $('#address1').val(),
            apartment_address: $('#address2').val(),

            csrfmiddlewaretoken: '{{ csrf_token }}',
            action: 'payment'
        },
        success: function (response) {
            window.location.replace('{% url "payment:payment-success" %}')

        },
        error: function (error) {
            window.location.replace('{% url "payment:payment-failed" %}')
        }
    })

})
