from random import choice
from django.db import transaction
from django.core.management.base import BaseCommand
from accountapp.models import CustomUser, Profile
from worldcupapp.models import Worldcup
from ...factories.accountapp import UserFactory, ProfileFactory
from ...factories.worldcupapp import (
    WorldcupFactory,
    TextMediaFactory,
    ImageMediaFactory,
    GifMediaFactory,
    VideoMediaFactory,
)


model_factory_mapping = {
    CustomUser: UserFactory,
    Profile: ProfileFactory,
    Worldcup: WorldcupFactory,
}

NUM_USERS = 50
NUM_WORLDCUPS = 50
RANGE_WORLDCUPS_MEDIA = range(2, 50)
RANGE_WORLDCUPS_COMMENT = range(0, 50)


class Command(BaseCommand):

    help = "User 더미 데이터 생성"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # delete...
        self.stdout.write("Deleting old data...")

        for model in model_factory_mapping.keys():
            model.objects.all().delete()

        # create...
        self.stdout.write("Creating new data...")

        users = []

        for _ in range(NUM_USERS):
            user = UserFactory()
            ProfileFactory(user=user)
            users.append(user)

        media_type_mapping = {
            "Text": TextMediaFactory,
            "Image": ImageMediaFactory,
            "Gif": GifMediaFactory,
            "Video": VideoMediaFactory,
        }

        for _ in range(NUM_WORLDCUPS):
            worldcup = WorldcupFactory(creator=choice(users))
            media_factory = media_type_mapping[worldcup.media_type]

            for _ in range(choice(RANGE_WORLDCUPS_MEDIA)):
                media_factory(worldcup=worldcup)
