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

  $('select#act').click(function(){
    $('.message').empty();
    $('.message').html("<h3><strong>Active:</strong> Little or No Exercise, Moderate Walking, Desk Job (Away from Home) </br><strong>Lightly Active:</strong>, Exercise or Mdoerate Sports 2 to 3 days a Week, Light Jogging or Walking 5 to 7 Days a Week </br><strong>Moderately Active:</strong> Physical Work, Exercise, or Sports 4 to 5 Days a Week, Construction Laborer</br><strong>Very Active:</strong> Heavy Physical work, Exercise, or Sports 6 to 7 Days a Week, Hard Laborer</h3>");
    $('.message').show();
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
});
