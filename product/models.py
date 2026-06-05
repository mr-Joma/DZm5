from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    # HW 2
    @property
    def rating(self):
        reviews = self.reviews.all()

        if reviews.exists():
            return sum(i.stars for i in reviews) / reviews.count()

        return 0
    
    
class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=((i, i) for i in range(1, 6)),# HW 2
                                default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    
    def __str__(self):
        return self.text