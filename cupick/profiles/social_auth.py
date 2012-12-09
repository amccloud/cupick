import logging, datetime
from cupick.profiles.models import Profile

logger = logging.getLogger(__name__)

def pick(value, options):
    return options.get(value, None)

def sync_facebook_profile(request, response, user=None, is_new=False, *args, **kwargs):
    if not user:
        return

    if 'first_name' in response:
        user.profile.first_name = response['first_name']

    if 'last_name' in response:
        user.profile.last_name = response['last_name']

    if 'gender' in response:
        user.profile.gender = pick(response['gender'], {
            'male': Profile.GENDER_MALE,
            'female': Profile.GENDER_FEMALE,
        })

    if 'interested_in' in response:
        if len(response['interested_in']) > 1:
            user.profile.orientation = Profile.ORIENTATION_BISEXUAL
        else:
            interested_in = pick(response['interested_in'][0], {
                'male': Profile.GENDER_MALE,
                'female': Profile.GENDER_FEMALE,
            })

            if user.profile.gender == interested_in:
                user.profile.orientation = Profile.ORIENTATION_GAY
            else:
                user.profile.orientation = Profile.ORIENTATION_STRAIGHT

    if 'birthday' in response:
        try:
            # Example birthday: "06/22/1990"
            user.profile.birthday = datetime.datetime.strptime(response['birthday'], '%m/%d/%Y').date()
        except ValueError:
            logger.warning("Could not parse Facebook profile's birthday.")

    if 'location' in response:
        user.profile.location_name = response['location']['name']

    user.profile.save()
