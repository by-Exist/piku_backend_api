from rest_framework_simplejwt import views as simplejwt_views


class DecoratedTokenObtainPairView(simplejwt_views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(simplejwt_views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
