from rest_access_policy import AccessPolicy


class UserViewSetAccessPolicy(AccessPolicy):

    statements = [
        {
            "principal": "*",
            "action": ["<method:options>", "<method:head>", "active"],
            "effect": "allow",
        },
        {
            "principal": "*",
            "action": ["list", "retrieve"],
            "effect": "allow",
        },
        {
            "principal": "anonymous",
            "action": ["create"],
            "effect": "allow",
        },
        {
            "principal": "authenticated",
            "action": ["destroy", "password"],
            "condition": "is_self",
            "effect": "allow",
        },
    ]

    def is_self(self, request, view, action) -> bool:
        user = request.user
        view_user = view.get_object()
        return user == view_user
