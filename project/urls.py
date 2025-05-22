from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('asistent.urls')),
    path('admin/', admin.site.urls),
]

handler400 = 'asistent.views.error_400'
handler401 = 'asistent.views.error_401'
handler403 = 'asistent.views.error_403'
handler404 = 'asistent.views.error_404'
handler405 = 'asistent.views.error_405'
handler408 = 'asistent.views.error_408'
handler429 = 'asistent.views.error_429'
handler500 = 'asistent.views.error_500'
handler502 = 'asistent.views.error_502'
handler503 = 'asistent.views.error_503'
handler504 = 'asistent.views.error_504'