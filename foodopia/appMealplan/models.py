from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from abc import abstractmethod

# Create your models here.

class PricedItem(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0.0)

    class Meta:
        abstract = True
    
    def set_price(self, user, p):
        if not user.is_staff:
            raise PermissionDenied("You do not have permission to set the price.")
        self.price = p
        self.save()

    def get_price(self):
        return self.price
    
    @abstractmethod
    def get_cost(self):
        pass
    
    def __str__(self):
        return self.name

class Ingredient(PricedItem):
        
    def get_cost(self, quantity_grams):
        # Suppose price is x / 500g
        return self.price * quantity_grams / 500.0


class Dish(PricedItem):
    type = models.CharField(max_length=100, choices=[("Vegetable", "Vegetable"),
                                                     ("Soup", "Soup"), 
                                                     ("Meat", "Meat"),], default="Undefined")
    time_required = models.IntegerField(default=30)
    ingredients = models.ManyToManyField(Ingredient, through='DishIngredient')
    img = models.ImageField(default=None)

    def get_cost(self):
        total_cost = 0.0
        for dish_ingredient in self.dishingredient_set.all():
            total_cost += dish_ingredient.get_cost()
        return total_cost

    def get_details(self) -> str:
        ingredients_list = ", ".join([ingredient.name for ingredient in self.ingredients.all()])
        return f"Dish_name: {self.name}, Prepare_time: {self.time_required} minutes, Ingredients: {ingredients_list}, Cost: {self.get_cost():.2f}, Price: {self.get_price():.2f}"
    
class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_grams = models.FloatField()

    def __str__(self):
        return f"{self.quantity_grams}g of {self.ingredient.name} in {self.dish.name}"

    def get_cost(self):
        return self.ingredient.get_cost(self.quantity_grams)

class Meal(PricedItem):
    num_protein = models.IntegerField()
    num_vege = models.IntegerField()
    num_side = models.IntegerField()
    dishes = models.ManyToManyField("Dish")
    
    def get_cost(self):
        cost = 0.0
        for dish in self.dishes.all():
            cost += dish.get_cost()
        return cost

    def get_details(self) -> str:
        dishes_list = ", ".join([dish.name for dish in self.dishes.all()])
        return (f"Meal: {self.name}, "
                f"Proteins: {self.num_protein}, "
                f"Vegetables: {self.num_vege}, "
                f"Sides: {self.num_side}, "
                f"Dishes: {dishes_list}, "
                f"Price: {self.get_price():.2f}")

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Economic', _('Economic')),
        ('Healthy', _('Healthy')),
        ('DIY', _('DIY')),
        ('Express', _('Express')),
        ('Ready_to_cook', _('Ready to Cook')),
    ]
    name = models.CharField(max_length=100, null=False, choices=CATEGORY_CHOICES)


class MealPlan(PricedItem):
    num_meals = models.IntegerField()
    meal = models.ForeignKey("Meal", null=False, blank=False, on_delete=models.CASCADE, related_name='meal_plans')
    size = models.IntegerField(choices=[
        (1, 'Single'),
        (2, 'Double'),
        (3, 'Family Lite'),
        (4, 'Family Meal')
    ])
    category = models.ForeignKey("Category", on_delete=models.SET_DEFAULT, default=None)
    
    def get_cost(self):
        return self.num_meals * self.meal.get_cost()
    
    def __str__(self):
        return self.name