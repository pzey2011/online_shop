from django.db import models

class Group(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group)
    price = models.PositiveIntegerField(default=0)
    comment = models.TextField(max_length=500)
    image = models.ImageField(upload_to="static/images",default="static/images/avatar.jpg")
    stock=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS = (
        ('requested', 'requested'),
        ('canceled', 'canceled'),
        ('pending', 'pending'),
        ('finished', 'finished'),
    )
    items = models.ManyToManyField(Item)
    time = models.DateTimeField('date created', auto_now_add=True)
    total_price=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=1, choices=STATUS, default='requested')

   # def __str__(self):
     #   return self.title
