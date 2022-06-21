from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.

class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    occupants_count = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    def save_neighborhood(self):
        self.save()
    
    def delete_neighborhood(self):
        self.delete()
        
    @classmethod
    def get_hoods(cls):
        hood = cls.objects.all()
        return hood
    
    @classmethod
    def search_hoods(cls, search_term):
        hood = cls.objects.filter(name__icontains=search_term)
        return hood
    
    @classmethod
    def get_by_admin(cls, Admin):
        hood = cls.objects.filter(Admin=Admin)
        return hood
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to = 'profile_pics/', blank=True, default='profile_pics/default.jpg')
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE, blank=True, default='1')

    @receiver(post_save,sender=User)
    def create_profile(sender, instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_profile(sender, instance,**kwargs):
        instance.profile.save()

    def save_profile(self):
        self.save()
        
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)