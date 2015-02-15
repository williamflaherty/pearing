import datetime
from django.utils import timezone
from dateme_app.models import Person, Gender


def create_fake_gender(gender):
    g = Gender(name=gender)
    g.save()
    return g

def create_fake_person(username, gender, orientation, handle=None, token="Fake token", token_expiration=None, tagline="Fake tagline",
                        birthday="1900-01-01", age_start=18, age_end=50, age=116):
    if not handle:
        handle=username

    if not token_expiration:
        token_expiration = timezone.now() + datetime.timedelta(days=1)

    p = Person(
        username=username,
        handle=handle, 
        token=token,
        token_expiration=token_expiration,
        tagline=tagline,
        birthday=birthday,
        age_start=age_start,
        age_end=age_end,
        gender=gender,
        orientation=orientation,
        age=age
    )

    p.save()
    return p
	
def create_fake_person_from_json(json):
    # would be nice to be able to load up fixtures from json
    raise NotImplementedError()