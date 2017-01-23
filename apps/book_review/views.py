from django.shortcuts import render,redirect
from models import users, books, reviews
from django.db.models import Count
from django.contrib import messages
import re
from django.contrib.auth import authenticate
import inspect
email_re = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
import bcrypt
def containnumber(string):
    return bool(re.search(r'\d', string))
users_all = users.objects.all()
books_all = books.objects.all()
reviews_all = reviews.objects.all()
def index(request):
    context= {
        'users': users.objects.all()

    }
    return render(request, 'index.html',context)

def add(request):
    firstname = request.POST['first']
    lastname = request.POST['last']
    email = request.POST['email']
    password = request.POST['pass']
    passwordcon = request.POST['passcon']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    error = False
    context = {
        'users': users.objects.all(),
        }
    if len(firstname)<2:
        error= True
        context['enterfirst'] = 'Enter a valid name'
    if containnumber(firstname)==True:
        error = True
        context['enterfirst'] = 'Enter a valid name'
    if len(lastname)<2:
        error = True
        context['enterlast'] = 'Enter a valid name'
    if containnumber(lastname):
        error = True
        context['enterlast'] = 'Enter a valid name'
    if not email_re.match(email):
        error = True
        context['emailcon'] = 'Must be a valid email'
    if len(password)<9:
        error = True
        context['password'] = 'Password must be longer than 8 digits'
    if len(passwordcon)<9:
        error = True
        context['password'] = 'Password must be longer than 8 digits'
    if password != passwordcon:
        context['password'] = 'Passwords must match'
        error = True
    if not error:
        print pw_hash
        context['sucess'] =  'You sucessfully registerd'
        users.objects.create(first_name = request.POST['first'], last_name = request.POST['last'], email = request.POST['email'], password= pw_hash)
        return render(request, 'index.html',context)
    else:
        return render(request, 'index.html',context)

def login(request):
    email_login = request.POST['email_login']
    print users.objects.filter(email = request.POST['email_login']).exists()

    if users.objects.filter(email = request.POST['email_login']).exists() == False:
        context = {
            'fail': 'Enter a valid email'
        }
        return render(request, 'index.html',context)
    else:
        password_login = request.POST['password_login']
        user = users.objects.filter(email = email_login)
        hashed = user[0].password
        if user is not None:
            if bcrypt.hashpw(password_login.encode(), hashed.encode()) == hashed:
                print user[0].first_name
                request.session['first_name'] = user[0].first_name
                request.session['last_name'] = user[0].last_name
                request.session['email'] = user[0].email
                request.session['id'] = user[0].id
                return redirect('/books')
            else:
                context = {
                'fail': 'Email and password did not match'
                }
                return render(request, 'index.html', context)

def books_route(request):
    context = {
        'books': books.objects.all(),
        'reviews': reviews.objects.all(),
        'users': users.objects.all(),
    }
    return render(request, 'books.html',context )

def newbook(request):
    return render(request, 'newbook.html')

def createbook(request):
    title = request.POST.get('book', '1')
    author = request.POST.get('author', '1')
    description = request.POST.get('description', '1')
    error = False
    context = {
        'title': title,
        'author': author,
        'description': description
        }
    if len(author)<2:
        error= True
        context['nullauthor'] = 'Enter a valid name'
    if containnumber(author)==True:
        error = True
        context['nullauthor'] = 'Enter a valid name'
    if len(title)<2:
        error = True
        context['nulltitle'] = 'Enter a valid Title'
    if len(description)<10:
        error = True
        context['nulldescription'] = 'Enter a valid description'
    if error == True:
        return render(request, 'newbook.html', context)
    else:
        users_instance = users_all.filter(id = request.session['id'])
        books.objects.create(title = title, author = author)
        book_instance = books_all.filter(id = len(books_all))
        reviews.objects.create( review = description, user = users_instance[0], book = book_instance[0] )
        return redirect('/books')
def newreview(request, id):
    context = {

    }
    users_instance = users_all.filter(id = request.session['id'])
    books_instance = books_all.filter( id = id)
    newreview = request.POST['newreview']
    if len(newreview)<10:
        context['nullreview'] = 'Enter a valid description'
        return render(request, books.html, context)
    else:
        reviews.objects.create(review = newreview, book = books_instance[0],user = users_instance[0] )
        return redirect('/books')
def user_display(request,id):
    users_user = users_all.filter(id = id)
    reviews_review = reviews_all.filter(user = id)
    number = reviews.objects.filter(id= id).annotate(count = Count("id"))
    context = {
        'reviews': reviews_review,
        'users': users_user,
        'number': number.count
    }
    return render(request, 'user_display.html', context)
def book_reviews(request, id):
    users = users_all.filter(id = id)
    reviews = reviews_all.filter(book = id)
    books = books_all.filter(id = id)
    user_id = request.session['id']
    context= {
        'books': books,
        'reviews': reviews,
        'users': users,
        'id': id,
        'user_id': user_id
    }
    return render(request, 'book_review.html', context)
def destroy(request, id):
    reviews_all.filter(id = id).delete()
    return redirect('/books')
