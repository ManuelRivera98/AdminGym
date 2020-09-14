"""Clients serializers."""


# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django
from django.core.validators import RegexValidator

# Models
from admingym.gyms.models import Client

# Serializers
from admingym.gyms.serializers import GymModelSerializer


class CreateModelSerializer(serializers.ModelSerializer):
    """Client model serializer"""

    # Regex validations
    cc_regex = RegexValidator(
        regex=r'\d{8,10}$',
        message='Identification number must be of type 1,000,000,000',
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to is digits allowed.',
    )

    gym = GymModelSerializer(read_only=True)

    cc = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Client.objects.all(),
                message='Another user has this identity document established.'
            ),
            cc_regex,
        ],
        max_length=10,
    )

    phone_number = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Client.objects.all(),
                message='Another user already this number, try another.'
            ),
        ],
        max_length=17,
    )

    c_memberships = serializers.IntegerField(min_value=1, read_only=True)

    class Meta:
        model = Client
        exclude = ('created_at', 'updated_at', )

        read_only_fields = ('is_active', 'c_memberships')

    def create(self, validated_data):
        """create client."""
        gym = self.context['gym']
        client = Client.objects.create(**validated_data, gym=gym)

        return client


class ClientModelSerializer(serializers.ModelSerializer):
    """List model serializer"""

    class Meta:
        model = Client
        exclude = ('created_at', 'updated_at')

        read_only_fields = ('c_memberships', 'is_active')
