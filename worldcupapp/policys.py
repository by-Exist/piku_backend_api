from worldcupapp.models import Worldcup
from rest_access_policy import AccessPolicy


class WorldcupViewSetAccessPolicy(AccessPolicy):

    statements = [
        {
            "principal": "*",
            "action": ["<method:options>", "<method:head>"],
            "effect": "allow",
        },
        {
            "principal": "*",
            "action": ["list", "retrieve", "play_counts", "view_counts"],
            "effect": "allow",
        },
        {
            "principal": "authenticated",
            "action": ["create"],
            "effect": "allow",
        },
        {
            "principal": "authenticated",
            "action": ["partial_update", "destroy"],
            "condition": "is_creator",
            "effect": "allow",
        },
    ]

    def is_creator(self, request, view, action) -> bool:
        user = request.user
        worldcup = view.get_object()
        return user == worldcup.creator


# class MediaViewSetAccessPolicy(AccessPolicy):

#     statements = [
#         {
#             "principal": "*",
#             "action": ["<method:options>", "<method:head>"],
#             "effect": "allow",
#         },
#         {
#             "principal": "*",
#             "action": ["list", "retrieve"],
#             "effect": "allow",
#         },
#         {
#             "principal": "authenticated",
#             "action": ["create", "partial_update", "destroy"],
#             "condition": "is_worldcup_creator",
#             "effect": "allow",
#         },
#     ]

#     def is_worldcup_creator(self, request, view, action) -> bool:
#         user = request.user
#         worldcup_pk = view.kwargs["worldcup_pk"]
#         worldcup = Worldcup.objects.get(pk=worldcup_pk)
#         return worldcup.creator == user


# # list create partial_update destroy
# class CommentViewSetAccessPolicy(AccessPolicy):

#     statements = [
#         {
#             "principal": "*",
#             "action": ["<method:options>", "<method:head>"],
#             "effect": "allow",
#         },
#         {
#             "principal": "*",
#             "action": ["list", "create", "check_writer"],
#             "effect": "allow",
#         },
#         {
#             "principal": "authenticated",
#             "action": ["partial_update", "destroy"],
#             "condition": "is_writer",
#             "effect": "allow",
#         },
#         {
#             "principal": "anonymous",
#             "action": ["partial_update", "destroy"],
#             "effect": "allow",
#         },
#     ]

#     def is_writer(self, request, view, action) -> bool:
#         user = request.user
#         comment = view.get_object()
#         return comment.writer == user
