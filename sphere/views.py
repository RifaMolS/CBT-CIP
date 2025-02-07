from django.shortcuts import render,redirect
from .models import registration 
from .models import Post, Like, Comment
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from django.conf import settings
# Create your views here.
def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Insert data into sphere_registration table
        new_user = registration(username=username, email=email, password=password)
        new_user.save()

        # Redirect to login or another page
        return redirect('login')
    return render(request, 'register.html')
def login(request):
    if request.method == "POST":
        # Safely retrieve email and password from the form using .get()
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            # Return an error message if either the email or password is missing
            error = "Please enter both email and password"
            return render(request, 'login.html', {'error': error})

        try:
            # Fetch the user from the database based on the email and password
            logdet = registration.objects.get(email=email, password=password)
            
            # Print the user id for debugging purposes
            print(logdet.id)

            # Store user ID in session for persistent login
            request.session['session1'] = logdet.id

            # Print the session id for debugging purposes
            print(request.session['session1'])

            # Redirect based on role or redirect to the homepage
            return redirect('homepage')  # Change 'homepage' to your actual route

        except registration.DoesNotExist:
            # If the user is not found, show an error message
            error = "Invalid email or password"
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')
def homepage(request):
    if not request.session.get('session1'):
        return redirect('login')  # Redirect to login if no user is logged in

    # Retrieve all posts from the database
    posts = Post.objects.all().order_by('-created_at')  # Get posts ordered by creation time

    if request.method == "POST":
        if 'content' in request.POST:
            # Handle post creation
            content = request.POST.get('content')
            if content:
                user = registration.objects.get(id=request.session['session1'])
                new_post = Post(user=user, content=content)
                new_post.save()

        elif 'comment_content' in request.POST:
            # Handle comment creation
            post_id = request.POST.get('post_id')
            comment_content = request.POST.get('comment_content')
            if comment_content and post_id:
                post = Post.objects.get(id=post_id)
                user = registration.objects.get(id=request.session['session1'])
                new_comment = Comment(user=user, post=post, content=comment_content)
                new_comment.save()

        elif 'like' in request.POST:
            # Handle like action
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            user = registration.objects.get(id=request.session['session1'])
            if not Like.objects.filter(post=post, user=user).exists():
                new_like = Like(user=user, post=post)
                new_like.save()

    # Retrieve likes and comments for each post
    for post in posts:
        post.likes_count = Like.objects.filter(post=post).count()
        post.comments = Comment.objects.filter(post=post)
        post.user_profilepic = post.user.profilepic.url if post.user.profilepic else None


    return render(request, 'homepage.html', {'posts': posts})


def profile_view(request):
    if 'session1' in request.session:  # Check if user is logged in
        user_id = request.session['session1']
        user = registration.objects.get(id=user_id)  

        # Handle missing profile picture
        profile_picture = user.profilepic.url if user.profilepic else None  

        return render(request, 'profile.html', {'user': user, 'profile_picture': profile_picture})
    else:
        return redirect('login')

from django.db import IntegrityError

def update_profile(request):
    if 'session1' not in request.session:
        return redirect('login')

    user_id = request.session['session1']
    user = registration.objects.get(id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        bio = request.POST.get('bio')

        # Handle profile picture upload
        if 'profilepic' in request.FILES:
            user.profilepic = request.FILES['profilepic']

        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.address = address
        user.bio = bio
        user.save()

        return redirect('profile')

    return render(request, 'profile_update.html', {'user': user})

    
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Message, registration

def message_page(request):
    if 'session1' not in request.session:
        return redirect('login')

    user_id = request.session['session1']
    logged_in_user = registration.objects.get(id=user_id)

    # Fetch all users except the logged-in user
    users = registration.objects.exclude(id=user_id)

    return render(request, 'messages.html', {'users': users, 'logged_in_user': logged_in_user})


def chat_view(request, user_id):
    if 'session1' not in request.session:
        return redirect('login')

    sender = registration.objects.get(id=request.session['session1'])
    receiver = get_object_or_404(registration, id=user_id)

    return render(request, 'chat.html', {'receiver': receiver, 'sender': sender})

def send_message(request):
    if request.method == "POST":
        sender_id = request.session.get('session1')
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('message')

        if sender_id and receiver_id and content.strip():
            sender = registration.objects.get(id=sender_id)
            receiver = registration.objects.get(id=receiver_id)
            message = Message.objects.create(sender=sender, receiver=receiver, content=content)
            return JsonResponse({"status": "success", "message": content, "sender": sender.username})
    
    return JsonResponse({"status": "error"})

def fetch_messages(request, user_id):
    sender_id = request.session.get('session1')
    receiver_id = user_id

    messages_list = Message.objects.filter(
        sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id]
    ).order_by('created_at')

    messages_data = [
        {"sender": msg.sender.username, "content": msg.content, "created_at": msg.created_at.strftime('%H:%M')}
        for msg in messages_list
    ]
    return JsonResponse({"messages": messages_data})

def forgot_password(request):
    email = ""  # Initialize the email variable to an empty string
    if request.method == "POST":
        email = request.POST.get("email_forgotpassword")  # Get the email from the form
        
        if email:
            # Send password reset email
            send_password_reset_email(email)
            #messages.success(request, "A password reset link has been sent to your email.")
        else:
            messages.error(request, "Please enter a valid email.")

    return render(request, "forgot_password.html", {"email": email})

def send_password_reset_email(request):
    return render(request, "reset_password.html")
    

from django.contrib import messages
from .models import registration  # Import your user model

def reset_password(request):
    email = request.GET.get("email")  # Get email from the URL

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and confirm_password:
            if new_password == confirm_password:
                try:
                    # Find the user with the given email
                    user = registration.objects.get(email=email)
                    
                    # Update the password
                    user.password = new_password  # Change this to hashed password in production
                    user.save()

                    messages.success(request, "Your password has been reset successfully.")
                    return redirect("login")
                except registration.DoesNotExist:
                    messages.error(request, "Invalid or expired password reset link.")
            else:
                messages.error(request, "Passwords do not match!")

    return render(request, "reset_password.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import registration

def update_password(request):
    if request.method == 'POST':
        # Retrieve the current password and new password
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            # Ensure all fields are filled out
            return render(request, 'update_password.html', {'error': 'All fields are required'})

        if new_password != confirm_password:
            # Ensure the new password and confirm password match
            return render(request, 'update_password.html', {'error': 'New passwords do not match'})

        try:
            # Fetch the user from the session
            user_id = request.session.get('session1')
            if not user_id:
                return redirect('login')  # Redirect to login if user is not logged in

            user = registration.objects.get(id=user_id)

            if user.password != current_password:
                # Ensure the current password matches
                return render(request, 'update_password.html', {'error': 'Current password is incorrect'})

            # Update the password
            user.password = new_password
            user.save()

            # Provide a success message
            #messages.success(request, 'Your password has been updated successfully.')
            return redirect('homepage')  # Redirect to login page after successful password update

        except registration.DoesNotExist:
            return render(request, 'update_password.html', {'error': 'User not found'})

    return render(request, 'update_password.html')

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def logout(request):
    # Log the user out
    auth_logout(request)
    
    # Redirect to the login page
    return redirect('login')

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')