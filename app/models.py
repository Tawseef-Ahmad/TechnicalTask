from django.db import models


class MyUserManager(models.Manager):
    def create_user(self, email, username, address, qualification):
        user = self.create(
            email=email,
            username=username,
            address=address,
            qualification=qualification,
        )
        return user

class MyUser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    address = models.TextField()
    qualification = models.CharField(max_length=20)

    objects = MyUserManager()
