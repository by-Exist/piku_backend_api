from copy import deepcopy
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accountapp.models import Profile
from accountapp.serializers.profile import ProfileListSerializer


class UserListSerializer(serializers.HyperlinkedModelSerializer):

    _profile_nickname_validators = [
        *deepcopy(Profile._meta.get_field("nickname").validators),
        UniqueValidator(Profile.objects.all(), message="이미 사용중인 닉네임입니다."),
    ]
    _profile_email_validators = [
        *deepcopy(Profile._meta.get_field("email").validators),
        UniqueValidator(Profile.objects.all(), message="이미 사용중인 이메일입니다."),
    ]

    profile = ProfileListSerializer(read_only=True)
    nickname = serializers.CharField(
        write_only=True, validators=_profile_nickname_validators
    )
    email = serializers.EmailField(
        write_only=True, validators=_profile_email_validators
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "url",
            "username",
            "profile",
            "password",
            "nickname",
            "email",
        )
        extra_kwargs = {
            "url": {"view_name": "account-detail"},
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "date_joined": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        user_kwargs = validated_data
        profile_kwargs = {
            "nickname": user_kwargs.pop("nickname"),
            "email": user_kwargs.pop("email"),
        }
        user = get_user_model().objects.create_user_with_profile(
            user_kwargs, profile_kwargs
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
            "profile",
            "is_active",
            "last_login",
            "date_joined",
        )
        extra_kwargs = {
            "username": {"read_only": True},
            "password": {"write_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
        }

    def update(self, instance, validated_data):
        raise NotImplementedError


class PasswordChangeSerializer(serializers.Serializer):

    _password_validators = deepcopy(
        get_user_model()._meta.get_field("password").validators
    )

    old_password = serializers.CharField(validators=_password_validators)
    new_password = serializers.CharField(validators=_password_validators)
    repeat_new_password = serializers.CharField(validators=_password_validators)

    def validate_old_password(self, old_password):
        user = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("잘못 된 비밀번호입니다.")
        return old_password

    def validate(self, attrs):
        new_password = attrs["new_password"]
        repeat_new_password = attrs["repeat_new_password"]
        if new_password != repeat_new_password:
            raise serializers.ValidationError(
                {"repeat_new_password": "새로 입력한 두 비밀번호가 일치하지 않습니다."}
            )
        return attrs


class UsernameFindSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, email):
        if (
            not self.context["view"]
            .get_queryset()
            .filter(profile__email=email)
            .exists()
        ):
            raise serializers.ValidationError("해당 이메일로 가입된 계정이 존재하지 않습니다.")
        return email


class PasswordFindSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        username = attrs["username"]
        email = attrs["email"]
        if (
            not self.context["view"]
            .get_queryset()
            .filter(username=username, profile__email=email)
            .exists()
        ):
            raise serializers.ValidationError("해당 계정이 존재하지 않습니다. ID와 Email을 다시 확인해주세요.")
        return attrs
