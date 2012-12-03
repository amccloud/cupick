from .settings import STRIPE_PUBLISHABLE_KEY

def stripejs(request):
    return {
        'STRIPE_PUBLISHABLE_KEY': STRIPE_PUBLISHABLE_KEY,
    }
