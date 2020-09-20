
$('.add_order').on("click", function (e) {
    order_session = document.getElementById('text_order').value;
    url = document.getElementById('text_order').getAttribute('link');
    console.log(order_session, url);
    data = {
        order_session: order_session
    };
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        success: function (data) {
            var confirmBox = $("#confirm");
            var order_table = $(".order_table");
            if (data.add_order == true ){
                confirmBox.find(".message").text('Success! You added order');
                console.log(order_session, url);
                confirmBox.show();
                order_table.find(".item_id").text(data.id);
                order_table.find(".item_date").text(data.date);
                order_table.find(".item_status").text(data.status);
                order_table.find(".item_total").text(data.total);
                order_table.show();
            }else{
                confirmBox.find(".message").text('Failed');
                confirmBox.show();
            }
        }
    });
});