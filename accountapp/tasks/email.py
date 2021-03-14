from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


JOIN_EMAIL_SETTINGS = {
    "TITLE": "{}님, 이메일 인증을 완료해주세요.",
    "DEFAULT_USER_NAME": "회원",
    "MESSAGE": "아래 링크를 클릭하면 회원가입이 완료됩니다.\nLink : {}",
    # TODO: 적절한 이메일로 변경한다.
    "FROM": "admin@gmail.com",
}

FIND_USERNAME_SETTINGS = {
    "TITLE": "아이디 찾기 결과입니다.",
    "MESSAGE": "고객님께서 찾으시는 ID는 다음과 같은 형식으로 구성되어 있습니다.\nID: {}",
}

FIND_PASSWORD_SETTINGS = {
    "TITLE": "새로운 비밀번호 입니다.",
    "MESSAGE": "변경된 비밀번호는 다음과 같습니다.\nPW: {}\n로그인 후 반드시 비밀번호를 변경해주세요.\n만약 본인이 비밀번호 재발급을 요청한 것이 아니라면 즉시 계정을 확인해주세요.",
}


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


account_activation_token = AccountActivationTokenGenerator()


def user_pk_urlsafe_encode(user_pk):
    """user의 pk를 받아 url-safe한 방식으로 인코딩"""
    return urlsafe_base64_encode(force_bytes(user_pk))


def user_pk_urlsafe_decode(user_pk_base64_str):
    """인코딩된 문자열을 user의 pk로 디코딩"""
    return force_str(urlsafe_base64_decode(user_pk_base64_str))


# TODO: 추후 django 템플릿을 활용하여 body를 구현하도록 변경한다.
def send_mail_to_join_user(request, user, user_name, user_email, view_name):
    """
    user의 이메일에 해당 유저의 is_active를 True로 변경할 수 있는 url을 전송한다.
    """
    token = account_activation_token.make_token(user)
    rel_url = reverse(view_name, args=[user_pk_urlsafe_encode(user.pk), token])
    abs_url = request.build_absolute_uri(rel_url)
    send_mail(
        subject=JOIN_EMAIL_SETTINGS["TITLE"].format(user_name),
        message=JOIN_EMAIL_SETTINGS["MESSAGE"].format(abs_url),
        from_email=JOIN_EMAIL_SETTINGS["FROM"],
        recipient_list=[user_email],
    )


def is_join_sended_token(user, token):
    """
    token이 회원가입 시 이메일로 전달된 것과 동일한지 확인한다.
    """
    return account_activation_token.check_token(user, token)


def send_mail_to_find_username(email, half_username):
    """
    유저가 자신의 아이디를 잊어버렸을 경우 이메일로 일부분만 드러난 username을 보낸다.
    """
    print("아이디 찾기를 시도했어요!")
    print(f"{email}로 {half_username}을 보냈어요!")


def send_mail_to_find_password(username, new_password):
    """
    유저가 자신의 패스워드를 잊어버렸을 경우 이메일로 변경된 password를 보낸다.
    """
    print("비밀번호 찾기를 시도했어요!")
    print(f"{username}님에게 새로운 비밀번호 {new_password}를 보냈어요!")
