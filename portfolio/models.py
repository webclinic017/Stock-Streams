from django.db import models

# Create your models here.
class Account(models.Model):
	name = models.CharField(max_length=100)
	balance = models.FloatField(default=0.0)

	def __str__(self):
		return self.name

class Positions(models.Model):
	name = models.CharField(max_length=100)
	symbol = models.CharField(max_length=6)
	shares = models.FloatField()

	cost_basis = models.FloatField(default=0.0)
	account = models.ForeignKey("Account", on_delete=models.PROTECT)

	def __str__(self):
		return self.symbol

class Stonk(models.Model):
	symbol = models.CharField(max_length=6)
	timestamp = models.DateTimeField()

	price = models.FloatField()
	open = models.FloatField()
	close = models.FloatField()

	high = models.FloatField()
	low = models.FloatField()