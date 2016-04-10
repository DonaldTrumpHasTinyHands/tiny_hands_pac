$(document).foundation();

 $(document).ready(function(){

    $('.testimonials').bxSlider({
      auto: true,
      mode: 'vertical',
      pager: false,
      controls: false,
      slideMargin:3,
     });

    $('.adverts').bxSlider({
      minSlides: 3,
      maxSlides: 3,
      slideWidth: 210,
      slideMargin: 15
    });

    $('.menu-icon').on('click', function(e) {
      $(this).toggleClass("active");
    });

    // Close Checkout on page navigation
    $(window).on('popstate', function() {
      handler.close();
    });

    $('#step-one').on('click', function(e) {
      $("#donation-widget").removeClass('info-active')
      $("#donation-widget input#amount_input").attr("value","")
    });

    donationAmount = parseInt(window.location.hash.substr(1));

    if (donationAmount) {
      $("#donation-custom-value").focus().val(donationAmount)
    }


 });

 function promptInfo(amount) {
   ga('send', 'event', 'Donate', 'Step 1');
   $("#donation-widget").addClass('info-active')
   $("#donation-widget input#amount_input").attr("value",amount)
 }

 function customValue() {
   var amount = $("#donation-custom-value").val() * 100
   if (amount > 0) {
     $("#donation-custom-value").css("outline-color","default")
     promptInfo(amount)
   } else {
     $("#donation-custom-value").css("outline-color","#c44042")
     $("#donation-custom-value").focus()
   }
 }

 function postForm(token) {
   var req = new XMLHttpRequest();
   req.open("POST", "https://docs.google.com/forms/d/1KNysJvq_3J_hsWRPSAFZ_U8B-xtGfi_XJqXtBBYmBLY/formResponse", true);
   req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
   var data = {
     'entry.617638349': name_input.value,
     'entry.1335579254': employer_input.value,
     'entry.2019488712': city_input.value,
     'entry.2018513609': state_input.value,
     'entry.1093280422': email_input.value,
     'entry.796202537': token,
     'entry.1778107293': (amount_input.value/100).toString()
   }
   var request = ''
   for(var i in data)  {
     request += i + '=' + data[i] + '&'
   }
   req.send(request);
 }

 function nextDonate() {
   ga('send', 'event', 'Donate', 'Step 2');
   var handler = StripeCheckout.configure({
     key: 'pk_live_A2kJcpYemgN9x0yBwLyUzUxy',
     image: 'https://www.donaldtrumphastinyhands.com/share-preview.jpg',
     locale: 'auto',
     token: function(token) {
       postForm(token.id);
       $("#donation-widget").addClass('donation-thanks')
       ga('send', 'event', 'Donate', 'Donation');
     },
   });
   var errored = false,
       inputs = event.target.querySelectorAll('input, select')
   Array.prototype.forEach.call(inputs, function(input) {
     if( input.value.length < 1 ) {
       errored = true
       input.style.borderColor = 'red'
     } else input.style.borderColor = 'white'
   })
   if( !errored ) {
     var dollars = amount_input.value / 100;
     handler.open({
       image: 'https://www.donaldtrumphastinyhands.com/share-preview.jpg',
       name: 'Americans Against Insecure Billionaires with Tiny Hands PAC',
       description: '$'+ dollars +' Donation',
       email: email_input.value,
       stripeEmail: email_input.value,
       amount: amount_input.value,
       'panel-label': 'Donate',
     });
     e.preventDefault();
   }
   return false
 }
