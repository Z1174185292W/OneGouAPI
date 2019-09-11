# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import NavModel


class NavSerrializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NavModel
        fields = ['id', 'nav_child_id', 'name', 'image']


# 用户API接口

from .models import UserModel
from Address.models import AddressModel

class AdderssSeraLizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AddressModel
        fields = ('id', 'addresses')


class UserSeraLizer(serializers.HyperlinkedModelSerializer):
    # addresses = AdderssSeraLizer(many=True)

    class Meta:
        model = UserModel
        fields = ('id', 'name', 'phone', 'image', 'sex', 'bool')


