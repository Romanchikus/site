$(document).ready(function () {
    $('.add_to_cart').on("click", function (e) {
        e.preventDefault()
        product_slug = $(this).attr('data-slug')
        data = {
            product_slug: product_slug
        }
        $.ajax({
            type: "GET",
            url: '{% url "add_to_cart" %}',
            data: data,
            success: function (data) {
                $('#cart_count').html(data.cart_total)
            }
        })
    })
})