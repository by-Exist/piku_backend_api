from rest_access_policy import AccessPolicy


class ProfileViewSetPolicy(AccessPolicy):

    statements = [
        {
            "principal": "*",
            "action": ["<method:options>", "<method:head>"],
            "effect": "allow",
        },
        {
            "principal": "authenticated",
            "action": ["retrieve", "partial_update"],
            "condition": "is_self",
            "effect": "allow",
        },
    ]

    def is_self(self, request, view, action) -> bool:
        user = request.user
        profile_user = view.get_object().user
        return user == profile_user
