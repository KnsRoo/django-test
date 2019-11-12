from shop.models import Categories, Goods
from django.db.models import Sum

class Query:
	def __init__(self):
		self.result = []
		self.R1, self.R2 = False, False
		self.saved_req = ''
		categories_list = list(Categories.objects.values_list('name', flat=True))
		description_list = Categories.objects.values_list('description', flat=True)
		sum_list = []
		for item in categories_list:
			query = Goods.objects.filter(category__name = item).aggregate(Sum('count'))
			sum_list.append(query['count__sum'])
		for i in range(len(categories_list)):
			self.result.append((categories_list[i],sum_list[i],description_list[i]))
		self.all_c = [i[0] for i in self.result]

	def update(self):
		self.result = []
		categories_list = list(Categories.objects.values_list('name', flat=True))
		description_list = Categories.objects.values_list('description', flat=True)
		sum_list = []
		for item in categories_list:
			query = Goods.objects.filter(category__name = item).aggregate(Sum('count'))
			sum_list.append(query['count__sum'])
		sum_list = [0 if x is None else x for x in sum_list ]
		for i in range(len(categories_list)):
			self.result.append((categories_list[i],sum_list[i],description_list[i]))
		self.all_c = [i[0] for i in self.result]

	def sortByCategory(self,key):
		if key == '1':
			z = 0; R = self.R1;
			self.R1 = not self.R1
		if key == '2': 
			z = 1; R = self.R2;
			self.R2 = not self.R2
		self.result.sort(reverse = R, key = lambda x: x[z])