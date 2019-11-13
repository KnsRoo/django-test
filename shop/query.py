from shop.models import Categories, Goods
from django.db.models import Sum
import json

class Query:
	def __init__(self):
		self.result = []
		self.R1, self.R2 = False, False
		self.saved_req = ''
		self.categories_list = list(Categories.objects.values_list('name', flat=True))
		description_list = Categories.objects.values_list('description', flat=True)
		sum_list = []
		for item in self.categories_list:
			query = Goods.objects.filter(category__name = item).aggregate(Sum('count'))
			sum_list.append(query['count__sum'])
		for i in range(len(self.categories_list)):
			self.result.append((self.categories_list[i],sum_list[i],description_list[i]))

	def update(self):
		self.result = []
		self.categories_list = list(Categories.objects.values_list('name', flat=True))
		description_list = Categories.objects.values_list('description', flat=True)
		sum_list = []
		for item in self.categories_list:
			query = Goods.objects.filter(category__name = item).aggregate(Sum('count'))
			sum_list.append(query['count__sum'])
		sum_list = [0 if x is None else x for x in sum_list ]
		for i in range(len(self.categories_list)):
			self.result.append((self.categories_list[i],sum_list[i],description_list[i]))

	def jsoncats(self):
		return json.dumps(self.categories_list)

	def cats(self):
		return sorted(self.categories_list)

	def sortByCategory(self, key, R = False):
		if 'R' in key: R = True
		d = {'1': 0, '2': 1}
		self.result.sort(reverse = R, key = lambda x: x[d[key[0]]])