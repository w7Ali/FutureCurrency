from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('user/',include('user.urls')),
    path('home/', include('core.urls')),
    path('income/', include('income.urls')),
    path('expenses/', include('expenses.urls')),
    path('account/', include('account.urls'))


]
