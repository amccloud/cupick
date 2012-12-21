def sync_facebook_profile(request, response, user=None, is_new=False, *args, **kwargs):
    user.load_facebook(**response)
