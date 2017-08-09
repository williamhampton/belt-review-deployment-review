#$ ssh -i "djangokey.pem" ubuntu@ec2-35-166-63-151.us-west-2.compute.amazonaws.com

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
        context['sucess'] =  'You sucessfully registerd'
        users.objects.create(first_name = request.POST['first'], last_name = request.POST['last'], email = request.POST['email'], password= pw_hash)
        return render(request, 'index.html',context)
    else:
        return render(request, 'index.html',context)

def login(request):
    email_login = request.POST['email_login']
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
    users_all = users.objects.all()
    books_all = books.objects.all()
    reviews_all = reviews.objects.all()
    var = 0;
    for book in books_all:
        var +=1;
    rec_var = var;
    var = var-3;
    page_id = id;
    rec_var = rec_var -6;
    while rec_var < 0:
        rec_var +=1;
    while var < 0:
        var +=1;
    recent_books = books.objects.all();
    while var != 0:
        recent_books = recent_books.exclude(id = var);
        var -=1;
    book_page = books.objects.all();
    while rec_var !=0:
        book_page = book_page.exclude(id = rec_var);
        rec_var -= 1;
    last_id = 0;
    for review in reviews_all:
        last_id +=1;
    context = {
        'recent_books': recent_books,
        'last_id': last_id,
        'books': book_page.order_by('-id'),
        'reviews': reviews.objects.all(),
        'users': users.objects.all(),
        'page_id': page_id,
        'alphabet': ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
        }
    return render(request, 'bookx.html',context )

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
    if request.session['id'] == None:
        context['nulldescription'] = 'Guests Cannot create a review'
        return render(request, 'newbook.html', context)
        error = True
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
    if len(description)>300:
        error = True
        context['nulldescription'] = 'Your description is too long'
    if request.session['id'] ==None:
        error == True;
        context['nulldescription'] = "Guest Users can not create reviews"
    if error == True:
        return render(request, 'newbook.html', context)
    if error != True:
        users_instance = users_all.filter(id = request.session['id'])
        books.objects.create(title = title, author = author)
        variable = 0;
        for book in books.objects.all():
            variable +=1;
        book_instance = books_all.filter(id =variable)
        if error != True:
            reviews.objects.create( review = description, user = users_instance[0], book = book_instance[0] )
        return redirect('/books')
def newreview(request, id):

    context = {

    }
    if request.session['id'] == None:
        context['nullreview'] = 'Guests Cannot create a review'
        return render(request, 'bookx.html', context)
    users_instance = users_all.filter(id = request.session['id'])
    books_instance = books_all.filter( id = id)
    newreview = request.POST['newreview']
    if len(newreview)<10:
        context['nullreview'] = 'Enter a valid description'
        return render(request, 'bookx.html', context)
    if request.session['id'] == None:
        context['nullreview']= 'Guest Users can not create a review'
        return render(request, 'bookx.html',context)
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
def newreview2(request, id):
    context = {

    }
    identifier = id;
    users_instance = users_all.filter(id = request.session['id'])
    books_instance = books_all.filter( id = id)
    newreview = request.POST['newreview']
    users = users_all.filter(id = id);
    reviews = reviews_all.filter(book = id);
    books = books_all.filter(id = id);
    user_id = request.session['id'];
    context= {
        'books': books,
        'reviews': reviews,
        'users': users,
        'id': id,
        'user_id': user_id
    }
    if request.session['id'] == None:
        context['nullreview'] = 'Guests Cannot create a review'
        return render(request, 'book_review.html', context)
    if len(newreview)<10:
        context['nullreview'] = 'Enter a valid description'
        return render(request, 'book_review.html', context)
    if request.session['id'] == None:
        context['nullreview']= 'Guest Users can not create a review'
        return render(request, 'book_review.html',context)
    else:
        reviews.objects.create(review = newreview, book = books_instance[0],user = users_instance[0] )
        return render(request, 'book_review.html', context)
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
    users = users_all.filter(id = id);
    reviews = reviews_all.filter(book = id);
    books = books_all.filter(id = id);
    user_id = request.session['id'];
    context= {
        'books': books,
        'reviews': reviews,
        'users': users,
        'id': id,
        'user_id': user_id
    }
    return render(request, 'book_review.html', context)
def destroy(request, id):
    reviews_all.filter(id = id).delete();
    return redirect('/books');
def logout(request):
    request.session['first_name'] = None;
    request.session['last_name'] = None;
    request.session['email'] = None;
    request.session['id'] = None;
    return redirect('/');
def skip(request):
    request.session['first_name'] = None;
    request.session['last_name'] = None;
    request.session['email'] = None;
    request.session['id'] = None;
    return redirect('/books');
def game(request):
    return render(request, '1942/game.html');

def alphabetizedbook(request, letter):
    letter = letter;
    books_all = books.objects.all();
    for book in books_all:
        if book.title[0].upper() != letter:
            books_all = books_all.exclude(id = book.id);
    books_all = books_all.order_by('title')
    context = {
        'letter': letter,
        'books_all': books_all,
        'reviews': reviews.objects.all(),
    }
    return render(request, 'alphabet.html', context)
def alphabetizedauthor(request, letter):
    letter = letter;
    books_all = books.objects.all();
    for book in books_all:
        if book.author[0].upper() != letter:
            books_all = books_all.exclude(id = book.id);
    books_all = books_all.order_by('author')
    array1 = [];
    array2 = [];
    for book in books_all:
        array1.append(book.author);
        array2.append(book.id);
    for i in range(0,len(array1)):
        if i == len(array1)-1:
            context = {
                'letter': letter,
                'books_all': books_all,
                'reviews': reviews.objects.all(),
            }
            return render(request, 'alphabetauthor.html', context)
        if array1[i] == array1[i+1]:
            books_all = books_all.exclude(id = array2[i+1]);

    context = {
        'letter': letter,
        'books_all': books_all,
        'reviews': reviews.objects.all(),
    }
    return render(request, 'alphabetauthor.html', context)

def authordisplay(request,id):
    books_all = books.objects.all();
    identifier = int(id) ;
    name = []
    for book in books_all:
        if book.id == identifier:
            name.append(book.author);
            print name[0]
    for book in books_all:
        if book.author != name[0]:
            books_all = books_all.exclude(id = book.id);
    context = {
        'books_all': books_all,
        'reviews': reviews.objects.all(),
        }
    return render(request, 'author.html', context);
def booksearch(request):
    booksearch = request.POST['booksearch']
    books_all = books.objects.all();
    for book in books_all:
        if book.title == booksearch:
            return redirect('book/{}'.format(book.id));
    users_all = users.objects.all()
    books_all = books.objects.all()
    reviews_all = reviews.objects.all()
    var = 0;
    for book in books_all:
        var +=1;
    rec_var = var;
    var = var-3;
    page_id = id;
    rec_var = rec_var -6;
    while rec_var < 0:
        rec_var +=1;
    while var < 0:
        var +=1;
    recent_books = books.objects.all();
    while var != 0:
        recent_books = recent_books.exclude(id = var);
        var -=1;
    book_page = books.objects.all();
    while rec_var !=0:
        book_page = book_page.exclude(id = rec_var);
        rec_var -= 1;
    last_id = 0;
    for review in reviews_all:
        last_id +=1;
    context = {
        'recent_books': recent_books,
        'last_id': last_id,
        'books': book_page.order_by('-id'),
        'reviews': reviews.objects.all(),
        'users': users.objects.all(),
        'page_id': page_id,
        'alphabet': ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
        'nullsearch': 'Im sorry, But we do not have this book reviewed currently',
        }
    return render(request, 'bookx.html',context );
def silly(request):
    return render(request, 'silly.html');
