from django.db import models
from django.core.exceptions import PermissionDenied

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=False)
    price = models.FloatField()
    quantity_grams = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_cost(self):
        # Suppose price is x / 500g
        return self.price * self.quantity_grams / 500.0
    
    def set_price(self, user, p):
        if not user.is_staff:  # Check if the user is an admin
            raise PermissionDenied("You do not have permission to set the price of the ingredient.")
        self.price = p
        self.save()

class Dish(models.Model):
    name = models.CharField(max_length=200, blank=False)
    time_required = models.IntegerField(blank=False)
    ingredients = models.ManyToManyField(Ingredient)
    price = models.FloatField(default=0.0)
    img = models.ImageField()
    description = models.TextField(blank=True)

    def get_cost(self):
        cost = 0.0
        for ingredient in self.ingredients.all():
            cost += ingredient.get_cost()
        return cost
    
    def set_price(self, user, p):
        if not user.is_staff:  # Check if the user is an admin
            raise PermissionDenied("You do not have permission to set the price of the dish.")
        self.price = p
        self.save()

    def __str__(self) -> str:
        ingredients_list = ", ".join([ingredient.name for ingredient in self.ingredients.all()])
        return f"Dish_name: {self.name}, Prepare_time: {self.time_required} minutes, Ingredients: {ingredients_list}, Cost: {self.get_cost():.2f}, Price: {self.price:.2f}"
