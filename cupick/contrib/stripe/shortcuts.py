import stripe
from cupick.contrib.stripe.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY
