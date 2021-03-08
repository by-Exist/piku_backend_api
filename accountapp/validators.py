from django.contrib.auth.validators import (
    ASCIIUsernameValidator,
    UnicodeUsernameValidator,
)


class CustomASCIIUsernameValidator(ASCIIUsernameValidator):
    regex = r"^[\w-]+\Z"
    message = "영문 소문자, 숫자, 특수기호(_),(-)만 사용 가능합니다."


class CustomUnicodeNicknameValidator(UnicodeUsernameValidator):
    regex = r"^[가-힣a-zA-Z0-9_]+\Z"
    message = "한글(단일 자음, 모음 불가), 알파벳, 숫자, 특수기호(_)만 사용 가능합니다."
