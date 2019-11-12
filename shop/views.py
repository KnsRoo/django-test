from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from shop.models import Categories, Goods
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from random import randint, uniform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from shop.query import Query
import simplejson

query = Query()

def index(request):
	if not User.objects.all().exists():
		for user in ['admin', 'user']:
			newuser = User.objects.create_user(username = user, password = user)
			if newuser.username == 'admin':
				content_type = ContentType.objects.get_for_model(Categories)
				change = Permission.objects.create(codename='can_change', name='Can Change Model',
					content_type = content_type)
				newuser.user_permissions.add(change)
			newuser.save()
	if not Categories.objects.all().exists():
		for i in range(20):
			temp_category = Categories(name = 'Категория '+str(i),
									 description = ('Описание'+str(i))*400)
			temp_category.save()
	if not Goods.objects.all().exists():
		for i in range(500):
			temp_good = Goods(name = 'Товар'+str(i),
							category = Categories.objects.get(name = 'Категория '+str(randint(0,19))), 
							count = str(randint(0,200)),
							price = str(round(uniform(100.0, 2000.0),2)),
							description = ('Описание'+str(i))*400)
			temp_good.save()
	return render(request, "index.html")

def goods(request):
	gpp, show = 10, 0
	if request.GET.get('cpp'):
		gpp = request.GET.get('cpp')
	if not request.user.is_authenticated:
		return render(request, "index.html")
	goods = Goods.objects.all()
	if request.GET.get('delete'):
		Goods.objects.get(pk = request.GET.get('delete')).delete()
	if request.GET.get('show'):
		show = request.GET.get('show')
	filtr = request.GET.get('filter')
	if filtr:
		if filtr != 'None' and filtr != 'undefined':
			goods = Goods.objects.filter(category__name = request.GET.get('filter'))
	sort = request.GET.get('sortMethod')
	if sort != 'None' and sort != 'undefined':
		if sort == '1': goods = goods.order_by('name')
		if sort == '2': goods = goods.order_by('count')
		if sort == '3': goods = goods.order_by('price')
		if sort == '1R': goods = goods.order_by('-name') 
		if sort == '2R': goods = goods.order_by('-count') 
		if sort == '3R': goods = goods.order_by('-price') 
	paginator = Paginator(goods, gpp)
	page = request.GET.get('page')
	try:
		categories = paginator.page(page)
	except PageNotAnInteger:
		categories = paginator.page(1)
	except EmptyPage:
		categories = paginator.page(paginator.num_pages)
	return render(request, "goods.html", {'canchange': request.user.has_perm('shop.can_change'),'show': int(show), 'cpp': int(gpp), 'username': request.user.username, "filter": filtr, "sort": sort, "categories": query.result, "goods": categories})

def deletecat(request):
	if not request.user.is_authenticated:
		return render(request, "index.html")
	target = request.GET.get('delete')
	Goods.objects.filter(category__name = target).delete()
	Categories.objects.filter(name = target).delete()
	query.update()
	return cats(request)

def savecat(request):
	if not request.user.is_authenticated:
		return render(request, "index.html")
	if 'newname' in request.POST:
		newname = request.POST['newname']
		newdescription = request.POST['newdescription']
		newcat = Categories(name = newname, description = newdescription)
		newcat.save()
	if 'editname' in request.POST:
		newname = request.POST['editname']
		oldname = request.GET.get('edit')
		newdescription = request.POST.get('editdescription')
		Object = Categories.objects.filter(name = oldname)
		Object.update(name = newname, description = newdescription)
	query.update()
	return cats(request)

def addGood(request):
	if not request.user.is_authenticated:
		return render(request, "index.html")
	name = request.POST.get('name')
	description = request.POST.get('description')
	image_file = request.FILES['file'].file.read()
	category = Categories.objects.filter(name = request.POST.get('cat'))[:1].get()
	exists = Goods.objects.filter(category = category).filter(name = name).exists()
	count = request.POST.get('count')
	price = request.POST.get('price')
	if exists:
		return render(request, 'newedit.html', {"values": [name, image, description,
		 count, price],"exists": True, "categories": query.result, "addGood": True })
	newGood = Goods(name = name, image = image_file, description = description, category = category,
		count = count, price = price)
	newGood.save()
	return render(request,"form.html")

def editGood(request):
	if not request.user.is_authenticated:
		return render(request, "index.html") 
	name = request.POST.get('name')
	image_file = request.FILES['file'].file.read()
	description = request.POST.get('description')
	category = Categories.objects.filter(name = request.POST.get('cat'))[:1].get()
	exists = Goods.objects.filter(category = category).filter(name = name).exists()
	if exists:
		return render(request, 'newedit.html', {"exists": True, "categories": query.result, "addGood": False})
	count = request.POST.get('count')
	price = request.POST.get('price')
	Object = Goods.objects.get(pk = request.GET.get('pk'))
	Object.update(name = name, image = image_file, description = description, category = category,
		count = count, price = price)
	return render(request,"form.html")

def cats(request):
	if not request.user.is_authenticated:
		return render(request, "index.html")
	cpp, show, addCat, editcategory = 10, 0, False, None
	if request.GET.get('sortMethod'):
		if request.GET.get('sortMethod') != 'undefined':
			query.sortByCategory(request.GET.get('sortMethod'))
	if request.GET.get('show'):
		show = request.GET.get('show')
	if request.GET.get('cpp'):
		cpp = int(request.GET.get('cpp'))
	paginator = Paginator(query.result, cpp)
	page = request.GET.get('page')
	try:
		categories = paginator.page(page)
	except PageNotAnInteger:
		categories = paginator.page(1)
	except EmptyPage:
		categories = paginator.page(paginator.num_pages)
	if request.GET.get('edit'):
		editcategory = request.GET.get('edit')
	if request.GET.get('addCat'):
		addCat = True
	if request.GET.get('savecat'):
		return savecat(request)
	if request.GET.get('delete'):
		return deletecat(request)
	return render(request, 'cats.html', {'canchange': request.user.has_perm('shop.can_change'), 'user': request.user.username, "show": show, "cpp": cpp, "categories": categories, "all_c": simplejson.dumps(query.all_c), "addCat": addCat, "editcategory": editcategory })

def log_out(request):
	if not request.user.is_authenticated:
		return render(request, "index.html")
	logout(request)
	return render(request, 'index.html')

def newedit(request):
	if not request.user.is_authenticated:
		return render(request, "index.html")
	addGood, Object = True, None
	if request.GET.get('edit'):
		addGood = False
		Object = Goods.objects.get(pk = request.GET.get('edit'))
	return render(request, 'newedit.html', { "categories": query.result, "good": Object, "addGood": addGood})

def log_in(request):
	error = None
	username, password = request.GET.get('login'),request.GET.get('password')
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return cats(request)
		else:
			error = 'Ошибка авторизации'
	else:
		error = 'Неверное имя пользователя или пароль'
	return render(request, "index.html", {'error': error})
