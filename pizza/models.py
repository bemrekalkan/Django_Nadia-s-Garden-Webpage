from django.db import models

class Size(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title #? 👈 This is for good visual experimentation!

class Pizza(models.Model):
    topping1 = models.CharField(max_length=100)
    topping2 = models.CharField(max_length=100)
    size = models.ForeignKey(Size, on_delete=models.CASCADE) #? ONE-TO-MANY -> This is for correlation to the Size class

    def __str__(self):
        return f"{self.size}, {self.topping1}, {self.topping2}"