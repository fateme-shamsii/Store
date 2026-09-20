from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,related_name='profile')
    name = models.CharField(max_length=10)
    mobile_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
# after fields we have just one line white space and then write methods
    def __str__(self):
        return self.name

# if you want write multple classes(like models here) between 2 classes you enter 2 lines white space.
 # class model1:
    # ------
    # ------


# class model2:
    # -----
