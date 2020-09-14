"""Serializer user."""

# Django REST framework
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.utils import timezone

# Models
from admingym.users.models import User

# Utilities
import jwt
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'cc',
            'first_name',
            'last_name',
            'already_owns'
        )

        read_only_fields = ('already_owns', )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

        handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, validated_data):
        """Check credentials."""

        user = authenticate(email=validated_data['email'], password=validated_data['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')

        self.context['user'] = user

        return validated_data

    def create(self, validated_data):
        """Generate or retrieve new token"""

        token, created = Token.objects.get_or_create(user=self.context['user'])

        return token.key, self.context['user']


class UserCreateSerializer(serializers.Serializer):
    """User create account serializer

        Handle create account and gym, validation.
    """

    # Regex
    cc_regex = RegexValidator(
        regex=r'\d{8,10}$',
        message='Identification number must be of type 1,000,000',
    )

    # Fields
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Another user is already this email, try another.'
            )
        ]
    )

    username = serializers.CharField(
        min_length=2,
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Another user is already this username, try another.'
            )
        ]
    )

    cc = serializers.CharField(
        validators=[
            cc_regex,
            UniqueValidator(
                queryset=User.objects.all(),
                message='Another user added this ID as an identification property.',
            )
        ],
        min_length=8,
        max_length=10
    )

    first_name = serializers.CharField(
        min_length=2,
        max_length=20
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=20
    )

    # Password confirmation backend
    password = serializers.CharField(
        min_length=8,
    )

    password_confirmation = serializers.CharField(
        min_length=8,
    )

    def validate(self, validated_data):
        """Validation password and password_confirmation match."""
        password = validated_data['password']
        password_confirmation = validated_data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match.')

        # Module django validation passwords
        password_validation.validate_password(password)

        return validated_data

    def create(self, validated_data):
        """Handle create account user and gym."""
        del validated_data['password_confirmation']
        user = User.objects.create_user(**validated_data, is_verified=True, is_active=True)

        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        """Send account verification link to given user."""

        verification_token = self.gen_verification_token(user)

        subject = 'Welcome @{name_user} verify your account to start using Comparte Ride.'.format(
            name_user=user.username)

        message = verification_token

        from_email = 'Admin Gym <manuel.rivera1788@gmail.com>'

        send_mail(subject, message, from_email, [user.email], fail_silently=False,)

    def gen_verification_token(self, user):
        """Create JWT tha the user can use to verify its account."""

        exp_data = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': exp_data,
            'type': 'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # return and pass from binary type to string
        return token.decode()


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, value):
        """Verify token is valid."""

        try:
            payload = jwt.decode(value, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload

        return value

    def save(self):
        """Is responsable for updating the field of the models is_verified to true."""

        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.is_active = True
        user.save()
