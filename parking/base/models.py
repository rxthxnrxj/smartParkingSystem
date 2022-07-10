from django.db import models

# Create your models here.
# class parkingSlots(models.Model):
#     name=models.CharField(max_length=100, null=True)
#     latitude = models.CharField(max_length=100, null=True)
#     longitude = models.CharField(max_length=100, null=True)
#     slots = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return str(self.name)


class searchData(models.Model):
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.address)


class parkingInformation(models.Model):
    name = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)
    slots = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class cameraInformation(models.Model):
    name = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)
    availableSlots = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class imageData(models.Model):
    name = models.CharField(max_length=100, null=True)
    slots = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    capture = models.ImageField(null=True, blank=True,
                                default='/placeholder.png')
    _id = models.AutoField(primary_key=True, editable=False)
    availableSlots = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
