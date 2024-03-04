from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    order = models.IntegerField(null=True)
    def __str__(self):
        return self.image.url
    
    def get_real_estate(self):
        return RealEstate.objects.filter(photos=self).first()
    class Meta:
        app_label = 'app'

class RealEstate(models.Model):
    title = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    area = models.FloatField()
    num_rooms = models.IntegerField(null=True)
    bath_rooms = models.IntegerField(null=True)
    bed_rooms = models.IntegerField(null=True)
    address = models.CharField(max_length=255)
    district_location = models.CharField(max_length=255)
    rent_cost = models.FloatField()
    rent_type = models.IntegerField()  # 1 - hour, 2 - day, 3 - month
    description = models.TextField()
    photos = models.ManyToManyField(Photo, blank=True, related_name="real_estate")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    liked = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_number = models.CharField(max_length=255, null=True)
    whatsapp = models.BooleanField(null=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-update_date"]
        app_label = 'app'

    def __str__(self):
        return self.title + " " + self.owner.username
    
    def get_absolute_url(self):
        return reverse('property_detail', kwargs = {"property_id":self.pk})
    
    def get_photos(self):
        return self.photos.all().order_by('order')

    def get_preview_photo(self):
        return self.photos.get(order=1)
    

class LeaseContract(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    property = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name='lease_contracts', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_contracts', null=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leased_contracts', null=True)
    applied = models.BooleanField(default=False)

    def __str__(self):
        return self.property.title + " " + self.tenant.username
    class Meta:
        app_label = 'app'

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField() # 1 - new application, 2 - application confirmed, 3 - application denied, 4 - rent denied

    def __str__(self):
        if self.type == 1:
            return self.user.username + " " + "new application"
        elif self.type == 2:
            return self.user.username + " " + "application confirmed"
    class Meta:
        app_label = 'app'

class Mailling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
    class Meta:
        app_label = 'app'

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(RealEstate, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " " + self.property.title
    class Meta:
        app_label = 'app'

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField(null=True)
    rate = models.IntegerField()
    class Meta:
        app_label = 'app'

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.CharField(max_length=1000)
    class Meta:
        app_label = 'app'
