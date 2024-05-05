import stripe
from decimal import Decimal
from django.conf import settings
from nxtbn.payment.base_payment_getway import BasePaymentGateway, PaymentResponse


stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

class StripePaymentGateway(BasePaymentGateway):
    """Stripe payment gateway implementation."""

    def authorize(self, amount: Decimal, order_id: str, **kwargs):
        """Authorize a payment with Stripe."""
        try:
            # Create a PaymentIntent for authorization
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe expects the amount in cents
                currency='usd',  # or any other currency
                payment_method=kwargs.get("payment_method_id"),  # Stripe payment method ID
                confirmation_method='manual',  # authorize but don't capture
                confirm=True,
                metadata={'order_id': order_id},
            )
            return self.normalize_response(intent)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def capture(self, amount: Decimal, order_id: str, **kwargs):
        """Capture a previously authorized payment."""
        payment_intent_id = kwargs.get("payment_intent_id")
        try:
            # Capture the authorized payment
            intent = stripe.PaymentIntent.capture(payment_intent_id)
            return self.normalize_response(intent)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def cancel(self, order_id: str, **kwargs):
        """Cancel an authorized payment."""
        payment_intent_id = kwargs.get("payment_intent_id")
        try:
            # Cancel the authorized payment
            intent = stripe.PaymentIntent.cancel(payment_intent_id)
            return self.normalize_response(intent)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def refund(self, amount: Decimal, order_id: str, **kwargs):
        """Refund a captured payment."""
        charge_id = kwargs.get("charge_id")
        try:
            # Create a refund for the charge
            refund = stripe.Refund.create(
                charge=charge_id,
                amount=int(amount * 100),  # Stripe expects the amount in cents
            )
            return self.normalize_response(refund)
        except stripe.error.StripeError as e:
            return PaymentResponse(success=False, message=str(e))

    def normalize_response(self, raw_response):
        """Normalize the Stripe response to a consistent PaymentResponse."""
        return PaymentResponse(
            success=raw_response.get("status") in ["succeeded", "canceled", "refunded"],
            transaction_id=raw_response.get("id"),
            message=raw_response.get("status"),
            raw_data=raw_response,
        )
