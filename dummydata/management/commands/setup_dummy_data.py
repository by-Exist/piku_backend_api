import random
from django.db import transaction
from django.core.management.base import BaseCommand
from accountapp.models import CustomUser, Profile
from worldcupapp.models import Worldcup, Media, Comment
from ...factories.accountapp import UserFactory, ProfileFactory
from ...factories.worldcupapp import (
    WorldcupFactory,
    TextMediaFactory,
    ImageMediaFactory,
    GifMediaFactory,
    VideoMediaFactory,
    AuthUserCommentFactory,
    AnonUserCommentFactory,
)


models = [CustomUser, Profile, Worldcup, Media, Comment]

NUM_USERS = 50
NUM_WORLDCUPS = 50
NUM_RANGE_WORLDCUPS_MEDIA = range(0, 50)
NUM_RANGE_WORLDCUPS_COMMENT = range(0, 50)


class Command(BaseCommand):

    help = "User 더미 데이터 생성"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")

        for model in models:
            model.objects.all().delete()

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
            worldcup = WorldcupFactory(creator=random.choice(users))

            media_factory = media_type_mapping[worldcup.media_type]
            medias = []
            for _ in range(random.choice(NUM_RANGE_WORLDCUPS_MEDIA)):
                media = media_factory(worldcup=worldcup)
                medias.append(media)

            comments = []
            for _ in range(random.choice(NUM_RANGE_WORLDCUPS_COMMENT)):
                use_auth = random.choice([True, False])
                use_media = random.choice([True, False])
                data = {"worldcup": worldcup}
                if medias and use_media:
                    media = random.choice(medias)
                    data |= {"media": media}
                if use_auth:
                    writer = random.choice(users)
                    data |= {"writer": writer}
                    comment = AuthUserCommentFactory(**data)
                    comments.append(comment)
                else:
                    comment = AnonUserCommentFactory(**data)
                    comments.append(comment)
