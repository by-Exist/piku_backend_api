from rest_access_policy import AccessPolicy


class ReportViewSetAccessPolicy(AccessPolicy):

    statements = [
        {
            "principal": "*",
            "action": ["<method:options>", "<method:head>"],
            "effect": "allow",
        },
        {
            "principal": ["authenticated"],
            "action": ["list", "destroy", "partial_update"],
            # TODO: superuser -> group:manager
            "condition": ["is_superuser"],
            "effect": "allow",
        },
        {
            "principal": "*",
            "action": ["create"],
            "effect": "allow",
        },
    ]

    def is_superuser(self, request, view, action) -> bool:
        return request.user.is_superuser
