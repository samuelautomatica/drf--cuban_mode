from django.urls import path
from .views import *


urlpatterns = [
    # #path('autenticacion/',autenticacion,name="Autenticacion"),
    # path('Authenticated/',VRegister.as_view(), name= "Autenticacion"),
    # path('Close_Session/',Close_Session,name='Close_Session'),
    # path('Authenticated/Login/',Login,name="Login"),
    #path('Authenticated/',Authenticathed,name="Authenticated")
    path('Home/',Home.as_view(),)
]