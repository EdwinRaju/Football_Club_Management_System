from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth
from django.contrib import messages
from django.db import IntegrityError
from .models import CustomUser
# Create your views here.
def index(request):
    return render(request,"index.html")



# Get the custom user model

def reg(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        contract_start = request.POST.get('cdate')
        cdate = datetime.strptime(contract_start, '%Y-%m-%d')
        sal = request.POST['salary']
        player_age = request.POST['dob']
        role = request.POST['role']
        jno = request.POST.get('jerseyNumber')
        dob = datetime.strptime(player_age, "%Y-%m-%d")
        img = request.FILES.get('image')

        try:
            # Check if the role is "player" and jno is not provided
            if role == 'player':
                if jno is None:
                    raise ValueError("Jersey number (jno) is required for players.")
                
                # Check if the selected jersey number is already in use
                if CustomUser.objects.filter(jno=jno).exists():
                    raise IntegrityError("This jersey number is already in use.")
            else:
                jno = None  # Set jno to None for non-players
            
            # Create a new custom user instance
            user = CustomUser.objects.create_user(
                username=email,
                first_name=fname,
                last_name=lname,
                email=email,
                password=password,
                dob=dob,
                sal=sal,
                role=role,
                img=img,
                jno=jno,
                cdate=cdate,
            )

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('registration')  # Redirect to the login page after successful registration
        except IntegrityError as e:
            # Check if the IntegrityError is due to a duplicate email
            if 'unique constraint' in str(e).lower():
                messages.error(request, "This email is already registered. Please use a different email.")
            else:
                messages.error(request, "Jersey no is already taken")
        except ValueError as e:
            messages.error(request, str(e))  # Display the custom error message

    return render(request, 'reg.html')




def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        if email == "admin@gmail.com" and password == "Admin@123":
            # Check if the user is the admin and redirect to the admin dashboard
            request.session['email'] = email
            return redirect('adminreg')  # Redirect to the admin dashboard for admin users
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth(request, user)
            
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
    
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response





def staff(request):
    if 'email' in request.session:
        response = render(request, 'staff.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')



def coach(request):
    if 'email' in request.session:
        response = render(request, 'coach.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')



def player(request): 
    if 'email' in request.session:
        response = render(request, 'player.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')
    

def logout(request):
    try:
        del request.session['email']
    except:
        return redirect('index')
    return redirect('index')


def adminreg(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    user_profiles = User.objects.all()
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    
    # Render the HTML template6
    return render(request, 'adminreg.html', context)