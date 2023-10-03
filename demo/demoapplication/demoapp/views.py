from datetime import datetime 
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from passlib.hash import pbkdf2_sha256
from django.contrib import messages
from django.db import IntegrityError
from .models import Registration

def reg(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = pbkdf2_sha256.hash(password)
        contract_start = request.POST.get('cdate')  # Get the contract_start field
        cdate = datetime.strptime(contract_start, '%Y-%m-%d')
        sal =request.POST['salary']
        player_age = request.POST['dob']
        role = request.POST['role']
        jno = request.POST.get('jerseyNumber')  # Use request.POST.get to handle missing jerseyNumber gracefully
        dob = datetime.strptime(player_age, "%Y-%m-%d")
        img = request.FILES.get('image')
    
        try:
            # Check if the role is "player" and jno is not provided
            if role == 'player':
                if jno is None:
                    raise ValueError("Jersey number (jno) is required for players.")
                
                # Check if the selected jersey number is already in use
                if Registration.objects.filter(jno=jno).exists():
                    raise IntegrityError("This jersey number is already in use.")
            else:
                jno = None  # Set jno to None for non-players
            user = Registration.objects.create(
                fname=fname, lname=lname, email=email, dob=dob, sal=sal, passwd=hashed_password, role=role, img=img, jno=jno, cdate=cdate
            )

            return redirect('signin')  # Redirect to the login page after successful registration
        except IntegrityError as e:
            # Check if the IntegrityError is due to a duplicate email
            if 'unique constraint' in str(e).lower():
                messages.error(request, "This email is already registered. Please use a different email.")
            else:
                messages.error(request, "Jersey no is already taken")
        except ValueError as e:
            messages.error(request, str(e))  # Display the custom error message
    
    return render(request, 'reg.html')





def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Registration.objects.get(email=email)
            
            # Verify the hashed password using passlib
            if pbkdf2_sha256.verify(password, user.passwd):
                
                # Check the user's role and redirect accordingly
                if user.role == 'staff':
                    request.session['email'] = email
                    return redirect('staff')
                elif user.role == 'coach':
                    request.session['email'] = email
                    return redirect('coach')
                elif user.role == 'player':
                    request.session['email'] = email
                    return redirect('player')
            else:
                messages.error(request, "Login failed. Please check your credentials.")
        except Registration.DoesNotExist:
            messages.error(request, "Login failed. Please check your credentials.")
            
        return redirect('signin')  # Redirect back to the signin page if login fails
    response = render(request, 'signin.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response






def user_logout(request):
    try:
        del request.session['email']
    except:
        return redirect('signin')
    return redirect('signin')




def staff(request):
     if 'email' in request.session:
        response = render(request, 'staff.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
     else:
        return redirect('signin')



def coach(request):
    if 'email' in request.session:
        response = render(request, 'coach.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('signin')




def player(request): 
    if 'email' in request.session:
        response = render(request, 'player.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('signin')