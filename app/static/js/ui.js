$(function() {
  $('input#name').change(function(){
    if($('input#name').val()) {
      var name = $(this).val();
      $('.message').html("<h3>Hey " + name + ", Using USDA approved guidelines we will calculate your ideal caloric intake. From there, we will use the most recent medical research to figure out how much protein, carbs & fats you need.</h3>");
      $('.message').show();
    } else {
      $('.message').hide();
    }
    
  })
  $('select#quantity').change(function() {
    var amount;
    var quantity = parseInt($(this).val());
    $('input#subscribe').is(':checked') ? subscription_discount = 0.85 : subscription_discount = 1;

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

  $('button').click(function() {
      alert($('input#amount').val());
  });
});
