from rest_access_policy import AccessPolicy


class ReportViewSetAccessPolicy(AccessPolicy):

    statements = [
        {
            "principal": "*",
            "action": ["<method:options>", "<method:head>"],
            "effect": "allow",
        },
        # TODO: admin을 함수를 통해 식별하는 것이 아닌 Group을 활용하여 식별하도록 하자.
        {
            "principal": ["authenticated"],
            "action": ["list", "retrieve", "destroy"],
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
