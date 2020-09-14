"""Membership serializer."""

# Django REST framework
from rest_framework import serializers

# Django
from django.core.validators import RegexValidator

# Models
from admingym.memberships.models import Membership
from admingym.gyms.models import Client

# Serializers
from admingym.gyms.serializers import ClientModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    paid_for = ClientModelSerializer(read_only=True)
    paid_in = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Membership
        exclude = (
            'created_at',
            'updated_at',
        )


class CreateMembershipSerializer(serializers.Serializer):
    """Resume membership serializer"""

    # Regex
    cc_regex = RegexValidator(
        regex=r'\d{8,10}$',
        message='Identification number must be of type 1,000,000,000',
    )
    cc = serializers.CharField(
        validators=[cc_regex, ]
    )

    num_weeks = serializers.IntegerField(min_value=1)

    quantity = serializers.IntegerField(min_value=0)

    def validate_cc(self, value):
        """Validate that the document belongs to a gym client."""

        try:
            client = Client.objects.get(
                cc=value,
                gym=self.context['gym']
            )
        except Client.DoesNotExist:
            raise serializers.ValidationError('No customer is registered with this document.')

        self.context['client'] = client

        return value

    def create(self, validated_data):
        """Create or update membership

            create membership and if there is already an active one, add both and send
            the previous one to is_active = False
        """

        del validated_data['cc']

        payment_date = timezone.now()
        num_weeks = validated_data['num_weeks']

        num_days = num_weeks * 7

        # get already membership active
        try:
            already_active = Membership.objects.get(
                paid_for=self.context['client'],
                paid_in=self.context['gym'],
                is_active=True
            )
        except Membership.DoesNotExist:
            expires = payment_date + timedelta(days=num_days)
        else:
            # Get difference
            ex_already_active = already_active.due_date
            result_days = ex_already_active - payment_date

            expires = payment_date + timedelta(days=num_days) + result_days

            # update already active
            already_active.is_active = False
            already_active.save()

        finally:
            membership = Membership.objects.create(**validated_data, due_date=expires, payment_date=payment_date,
                                                   paid_for=self.context['client'], paid_in=self.context['gym'], is_active=True)

            # Update stats

            # Client
            client = self.context['client']
            client.is_active = True
            client.c_memberships += 1
            client.save()

            # Gym
            gym = self.context['gym']
            gym.c_memberships += 1
            gym.save()

            return membership
