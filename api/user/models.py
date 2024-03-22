import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField("email address", unique=True)
    name = models.CharField(max_length=100, null=True)
    friends = models.ManyToManyField("User", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} ({self.email})"

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super(User, self).save(*args, **kwargs)


class FriendRequest(BaseModel):
    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    requested_by = models.ForeignKey(
        "User", related_name="friend_requests_sent", on_delete=models.CASCADE
    )
    requested_to = models.ForeignKey(
        "User",
        related_name="friend_requests_received",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=Status.choices, max_length=20, default=Status.REQUESTED
    )

    def __str__(self):
        return f"{self.requested_by} -> {self.requested_to} [{self.status}]"

    class Meta:
        ordering = ["-created_at"]
