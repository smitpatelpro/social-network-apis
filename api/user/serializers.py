from django.contrib.auth.password_validation import validate_password
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from api.user.models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "password",
            "password_confirm",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create(
                email=validated_data["email"],
                name=validated_data["name"],
            )
            user.set_password(validated_data["password"])
            user.save()
        except IntegrityError:
            raise ValidationError({"email": ["This field must be unique."]})
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    requested_by = UserSerializer()
    requested_to = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = "__all__"

    def eager_load(qs):
        qs = qs.select_related("requested_by", "requested_to")
        return qs
