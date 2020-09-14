"""Serializer gyms."""

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django
from django.core.validators import RegexValidator

# Serializers
from admingym.users.serializers import UserModelSerializer

# Models
from admingym.gyms.models import Gym


class GymModelSerializer(serializers.ModelSerializer):
    """Gym model serializer"""

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Class meta"""

        model = Gym
        exclude = ('created_at', 'updated_at')

        read_only_fields = (
            'is_official',
            'is_active',
            'owner',
        )


class CreateGymModelSerializer(serializers.ModelSerializer):
    """Create gym Model serializer"""

    # Regex
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to is digits allowed.',
    )

    slug_name_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9]',
        message='Can not have spaces.',
    )

    # Fields
    owner = UserModelSerializer(read_only=True)
    slug_name = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Gym.objects.all(),
                message='Another gym is already this email, try another.'
            ),
            slug_name_regex,
        ],
        max_length=10
    )

    phone_number = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Gym.objects.all(),
                message='Another gym is already this number, try another.'
            ),
            phone_regex,
        ]
    )

    c_memberships = serializers.IntegerField(min_value=1, read_only=True)

    class Meta:
        """Class meta"""

        model = Gym
        fields = '__all__'

        read_only_fields = (
            'is_official',
            'is_active',
            'created_at',
            'updated_at',
            'c_memberships'
        )

    def create(self, validated_data):
        """Create ride and update stats"""
        user = self.context['request'].user
        gym = Gym.objects.create(**validated_data, owner=user, is_active=True)

        # update stats
        user.already_owns = True
        user.save()

        return gym
