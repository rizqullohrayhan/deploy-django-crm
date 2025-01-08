from django.urls import path

from . import views

app_name = "webapp"
urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.my_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('create-record', views.create_record, name="create-record"),
    path('update-record/<int:record_id>', views.update_record, name="update-record"),
    path('record/<int:record_id>', views.singular_record, name="record"),
    path('delete-record/<int:record_id>', views.delete_record, name="delete-record")
]
