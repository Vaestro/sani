$(function() {
  $('select#quantity').change(function() {
    var amount;
    var quantity = parseInt($(this).val());
    $('input#subscribe').is(':checked') ? subscription_discount = 0.84 : subscription_discount = 1;

    if (quantity == 7) {
      amount = quantity * 500 * subscription_discount
      $('.order-amount').html("<h1>$" + Math.round(amount * .01) + " monthly</h1>");
    } else if (quantity == 14) {
      amount = quantity * 425 * subscription_discount
      $('.order-amount').html("<h1>$" + Math.round(amount * .01) + " monthly</h1> ");
    } else if (quantity == 21) {
      amount = quantity * 400 * subscription_discount
      $('.order-amount').html("<h1>$" + Math.round(amount * .01) + " monthly</h1>");
    }
    $('input#amount').val(amount)
  });

  // $('input#subscribe').click(function() {
  //
  //   if ($('input#subscribe').is(':checked')) {
  //     $('.order-amount').show();
  //
  //   } else {
  //     $('.order-amount').hide();
  //   }
  // });

  $('button').click(function() {
      alert($('input#amount').val());
  });
});
