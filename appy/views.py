from django.shortcuts import render, redirect
from appy.models import User, Message, Comment
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request,"index.html")

def showSignin(request):
    return render(request,"signin.html")

def showRegister(request):
    return render(request,"register.html")

def addUser(request):
    # this is the route that processes the new show

    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/register')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        decoded_hash = hashed.decode('utf-8')
        if (len(User.objects.all()) == 0):
            user = User.objects.create(email = request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=decoded_hash, user_level = "admin")
        else: 
            user = User.objects.create(email = request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=decoded_hash)
        request.session['u_id'] = user.id
        if user.user_level == "admin":
            return redirect('/dashboard/admin')
        else:
            return redirect('/dashboard')

def checkOldUser(request):
    # this is the route that processes the new show
    user_list = User.objects.filter(email=request.POST['email'])
    if not user_list:
        messages.error(request, "Invalid credentials!")
        return redirect('/signin')
   
    user = user_list[0]
    request.session['u_id'] = user.id
   
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        
        if user.user_level == "admin":
            return redirect('/dashboard/admin')
        else:
            return redirect('/dashboard')
    else:
        messages.error(request, "Invalid credentials!")
        return redirect('/signin')

def showDashboard(request):
    user = User.objects.get(id = request.session['u_id'])
    if user.user_level == "admin":
            return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')


def successful(request):
    context = {
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
        "users": User.objects.all(),
        "primary": User.objects.get(id = request.session['u_id']),
    }
    return render(request,"user_dashboard.html", context)

def successful1(request):
    context = {
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
        "users": User.objects.all(),
        "primary": User.objects.get(id = request.session['u_id']),
    }
    return render(request,"admin_dashboard.html", context)

def showNewUserPage(request):
    context = {
        "user": User.objects.get(id = request.session['u_id']),
    }
    return render(request,"new_user.html", context)

def clear(request):
    request.session.clear()
    return redirect("/")

def createUser(request):
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/users/new')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        decoded_hash = hashed.decode('utf-8')
        user = User.objects.create(email = request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=decoded_hash)
        return redirect('/dashboard/admin')

def showEditUserPage(request, val):
    context = {
        "user": User.objects.get(id = val),
        "primary": User.objects.get(id = request.session['u_id']),
    }
    return render(request,"edit_user.html", context)

def showEditPage(request):
    context = {
        "user": User.objects.get(id = request.session['u_id'])
    }
    return render(request,"user_edit.html", context)

def updateUser(request, val):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/users/edit/{val}')
    else:
        user = User.objects.get(id = val)
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.user_level = request.POST["level"]
        user.save()
        return redirect("/user_dashboard")

def updateUser1(request, val):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/users/edit')
    else:
        user = User.objects.get(id = val)
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        return redirect("/user_dashboard")

def updatePassword(request, val):
    errors = User.objects.password_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        if request.session['u_id'] == val:
            return redirect('/users/edit')
        else:
            return redirect(f'/users/edit/{val}')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        decoded_hash = hashed.decode('utf-8')
        # check if password is a valid password 
        user = User.objects.get(id = val)
        user.password = decoded_hash
        user.save()
        return redirect("/user_dashboard")

def updateDesc(request, val):
    user = User.objects.get(id = val)
    user.desc = request.POST["desc"]
    user.save()
    return redirect(f"/users/show/{val}")


def showUserPage(request, val):
    context = {
        "user": User.objects.get(id = val),
        "messages": Message.objects.filter(wall_owner = User.objects.get(id = val)),
        "comments": Comment.objects.all(), 
        "primary": User.objects.get(id = request.session['u_id']),
    }
    return render(request,"user_page.html", context)

def postMessage(request, val):
    authors = User.objects.get(id = request.session['u_id'])
    if request.method == 'POST':
        new_message = Message.objects.create(
            desc = request.POST['desc'],
            author = authors,
            wall_owner = User.objects.get(id = val))
        new_message.save()
    return redirect(f'/users/show/{val}')

def postComment(request, val):
    mes = messages = Message.objects.get(id = val)
    wall = mes.wall_owner.id
    if request.method == 'POST':
        new_comment = Comment.objects.create(desc = request.POST['cmnt'], author = User.objects.get(id = request.session['u_id']), messages = Message.objects.get(id = val)
        )
        new_comment.save()
    return redirect(f'/users/show/{wall}')

def deleteUser(request, val):
    user = User.objects.get(id = val)
    user.delete()
    return redirect("/user_dashboard")