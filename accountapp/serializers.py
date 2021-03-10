from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accountapp.models import Profile

# ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "avatar", "email")
        extra_kwargs = {"email": {"read_only": True}}


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ("url", "nickname", "avatar", "email")


# UserSerializer
class UserSerializer(serializers.ModelSerializer):
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
        pw = validated_data.pop("password")
        instance.set_password(pw)
        instance.save()
        return instance


class UserListSerializer(serializers.HyperlinkedModelSerializer):

    _profile_nickname_validators = [
        *Profile._meta.get_field("nickname").validators,
        UniqueValidator(Profile.objects.all(), message="이미 사용중인 닉네임입니다."),
    ]
    _profile_email_validators = [
        *Profile._meta.get_field("email").validators,
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
        email = validated_data.pop("email")
        nickname = validated_data.pop("nickname")
        user = get_user_model().objects.create_user(**validated_data, is_active=False)
        Profile.objects.create(user=user, nickname=nickname, email=email)
        return user


class PasswordChangeSerializer(serializers.Serializer):

    _password_validators = get_user_model()._meta.get_field("password").validators

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


# Token Serializer
# https://github.com/axnsan12/drf-yasg/issues/407
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
