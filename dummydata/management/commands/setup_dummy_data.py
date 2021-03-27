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
from ...factories.reportapp import (
    UserReportFactory,
    WorldcupReportFactory,
    MediaReportFactory,
    CommentReportFactory,
)


models = [CustomUser, Profile, Worldcup, Media, Comment]

NUM_USERS = 50
NUM_WORLDCUPS = 50
NUM_RANGE_WORLDCUPS_MEDIA = range(0, 50)
NUM_RANGE_WORLDCUPS_COMMENT = range(0, 50)
NUM_REPORTS = 100


class Command(BaseCommand):

    help = "User 더미 데이터 생성"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")

        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data...")

        users = []
        worldcups = []
        medias = []
        comments = []
        reports = []

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
            worldcups.append(worldcup)

            media_factory = media_type_mapping[worldcup.media_type]

            for _ in range(random.choice(NUM_RANGE_WORLDCUPS_MEDIA)):
                media = media_factory(worldcup=worldcup)
                medias.append(media)

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

        for _ in range(NUM_REPORTS):
            factory, targets = random.choice(
                [
                    (UserReportFactory, users),
                    (WorldcupReportFactory, worldcups),
                    (MediaReportFactory, medias),
                    (CommentReportFactory, comments),
                ]
            )
            use_reporter = random.choice([True, False])
            data = {}
            if use_reporter:
                data["reporter"] = random.choice(users)
            data["reported"] = random.choice(targets)
            report = factory(**data)
            reports.append(report)
