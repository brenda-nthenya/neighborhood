from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.

class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    police_number = models.IntegerField()
    health_number = models.IntegerField()
    description = models.TextField(max_length=250)
    occupants_count = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, related_name="hood")

    def __str__(self):
        return f'{self.name} hood'

    def save_neighborhood(self):
        self.save()
    
    def delete_neighborhood(self):
        self.delete()
        
    @classmethod
    def get_hoods(cls):
        hood = cls.objects.all()
        return hood
    
    @classmethod
    def search_hoods(cls, neighbourhood_id):
        hood = cls.objects.filter(id=neighbourhood_id)
        return hood
    
    @classmethod
    def get_by_admin(cls, Admin):
        hood = cls.objects.filter(Admin=Admin)
        return hood
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name  = models.CharField(max_length=60)
    profile_picture = models.ImageField(upload_to = 'profile_pics/', null=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField(max_length=200)
    neighbourhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    @receiver(post_save,sender=User)
    def create_user_profile(sender, instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_user_profile(sender, instance,**kwargs):
        instance.profile.save()

    def save_profile(self):
        self.save()
        

    def delete_profile(self):
        self.delete()
    
    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


    def __str__(self):
        return f"{self.user}, {self.bio}, {self.profile_picture}"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Business(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    neighbourhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='business')

    def save_business(self):
        self.save()
    
    def delete_business(self):
        self.delete()

    @classmethod
    def get_allbusiness(cls):
        business = cls.objects.all()
        return business
    
    @classmethod
    def search_business(cls, name):
        business = cls.objects.filter(name__icontains=name).all()
        return business

    def __str__(self):
        return self.name
    
    @classmethod
    def get_by_hood(cls, neighborhoods):
        business = cls.objects.filter(neighborhood__name__icontains=neighborhoods)
        return business

class Posts(models.Model):
    title = models.CharField(max_length=100, null=True)
    post = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_owner')
    hood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, default='', related_name='hood_post')

    def __str__(self):
        return self.post
    
    def save_post(self):
        self.save()
    
    def delete_post(self):
        self.delete()
        
    @classmethod
    def get_allpost(cls):
        posts = cls.objects.all()
        return posts

    @classmethod
    def get_by_neighborhood(cls, neighborhoods):
        posts = cls.objects.filter(neighborhood__name__icontains=neighborhoods)
        return posts

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'My Post'
        verbose_name_plural = 'Posts'
    

class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()