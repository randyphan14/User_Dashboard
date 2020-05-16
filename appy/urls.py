from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
    path('signin', views.showSignin),
    path('register', views.showRegister),
    path('new_user', views.addUser),
    path('old_user', views.checkOldUser),
    path('dashboard', views.successful),
    path('dashboard/admin', views.successful1),
    path('clear', views.clear),
    path('users/new', views.showNewUserPage),
    path('create_user', views.createUser),
    path('user_dashboard', views.showDashboard),
    path('users/edit/<int:val>', views.showEditUserPage),
    path('update_user/<int:val>', views.updateUser),
    path('update_user1/<int:val>', views.updateUser1),
    path('update_password/<int:val>', views.updatePassword),
    path('update_desc/<int:val>', views.updateDesc),
    path('users/show/<int:val>', views.showUserPage),
    path('post_message/<int:val>', views.postMessage), 
    path('comment/<int:val>', views.postComment),
    path('users/edit', views.showEditPage),
    path('users/delete/<int:val>', views.deleteUser),
]