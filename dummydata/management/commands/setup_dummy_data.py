from django.db import transaction
from django.core.management.base import BaseCommand
from accountapp.models import CustomUser, Profile
from ...factories.accountapp import UserFactory, ProfileFactory


model_factory_mapping = {
    CustomUser: UserFactory,
    Profile: ProfileFactory,
}

NUM_USERS = 50


class Command(BaseCommand):

    help = "User 더미 데이터 생성"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        for model in model_factory_mapping.keys():
            model.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_USERS):
            user = UserFactory()
            ProfileFactory(user=user)
