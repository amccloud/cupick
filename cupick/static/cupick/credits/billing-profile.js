(function($, Stripe) {
    'use strict';
    
    $(function() {
        (function() {
            var $form = $('form#billing-profile'),
                $tokenInput = $form.find('#id_stripe_token'),
                $last4Input = $form.find('#id_card_last4'),
                $cardType = $form.find('#id_card_type'),
                $numberInput = $form.find('#id_card_number');

            $form.on('submit', function(event) {
                var $errorList = $form.find('ul.errorlist'),
                    cardNumber = $numberInput.val();

                $errorList.remove();

                if (cardNumber) {
                    event.preventDefault();

                    Stripe.createToken({
                        number: cardNumber,
                        expMonth: $form.find('#id_card_exp_month').val(),
                        expYear: $form.find('#id_card_exp_year').val(),
                        cvc: $form.find('#id_card_cvc').val() || null,
                        address_line1: $form.find('#id_card_address_line1').val() || null,
                        address_zip: $form.find('#id_card_address_zip').val() || null,
                        name: $form.find('#id_card_name').val() || null,
                        address_line2: $form.find('#id_card_address_line2').val() || null,
                        address_state: $form.find('#id_card_address_state').val() || null,
                        address_country: $form.find('#id_card_address_country').val() || null
                    }, function(status, response) {
                        if (status !== 200) {
                            if (status === 402 || status === 400) {
                                var field = $form.find('#id_card_' + response.error.param),
                                    message = response.error.message;

                                fieldValidationError(field, message);
                            }

                            return;
                        }

                        $tokenInput.val(response.id);
                        $last4Input.val(response.card.last4);
                        $cardType.val(response.card.type);

                        $form.unbind('submit').trigger('submit');
                    });
                }
            });

            function fieldValidationError(input, message) {
                var $errorList = $('<ul class="errorlist"></ul>');

                $errorList.append('<li>' + message + '</li>');
                $(input).parent().before($errorList);
            }
        })();
    });
})(jQuery, Stripe);
