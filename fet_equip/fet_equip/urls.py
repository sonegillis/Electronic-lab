"""fet_equip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mainapp.views import (
                            loginView, homeView, logoutView, 
                            borrowEquipmentView, processBorrowTransaction,
                            searchBorrowTransaction, returnEquipment,
                            searchEquipment, testView)


urlpatterns = [
    url(r'^test/', testView),
    url(r'^admin/', admin.site.urls),
    url(r'^$', loginView, name="login"),
    url(r'^user/welcome/$', homeView, name="home"),
    url(r'^logout/user/$', logoutView, name="logout_user"),
    url(r'^search-borrow-transaction/$', searchBorrowTransaction, name="search-borrow-transaction"),
    url(r'^search-equipment/$', searchEquipment, name="search-equipment"),
    url(r'^return-equipment/$', returnEquipment, name="return-equipment"),
    url(r'^borrow-equipment/$', borrowEquipmentView, name="borrow_equipment"),
    url(r'^confirm-equipment-borrow/$', processBorrowTransaction)
    # url(r'^$', include('mainapp.urls', namespace="main")),
]
