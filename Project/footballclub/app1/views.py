from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
import string
import secrets

def generate_password(length=12):
    # Define character sets for uppercase letters, lowercase letters, special characters, and digits
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    special_characters = string.punctuation
    digits = string.digits

    # Combine all character sets into one
    all_characters = uppercase_letters + lowercase_letters + special_characters + digits

    # Use secrets module to generate a random password of the specified length
    password = ''.join(secrets.choice(all_characters) for _ in range(length))

    return password


def index(request):
    return render(request,"index.html")




def delete_user(request, user_email):
    user = get_object_or_404(CustomUser, email=user_email)
    
    if user:
        email = user.email  # Store the email address in a variable
        if not user.is_superuser and user.role != "admin":
            user.delete()
            messages.success(request, f"User {email} has been successfully deleted.")
        else:
            messages.error(request, "You cannot delete superusers or admins.")
    else:
        messages.error(request, f"User with email {user_email} not found.")
    
    return redirect('adminreg')



def validate_email(request):
    email = request.GET.get('email', None)
    response_data = {}

    try:
        # Check if the email is valid according to Django's EmailValidator
        CustomUser._meta.get_field('email').validators[0](email)
        if CustomUser.objects.filter(email=email).exists():
            response_data['valid'] = False
        else:
            response_data['valid'] = True
    except ValidationError:
        response_data['valid'] = False

    return JsonResponse(response_data)




def checkJerseyNumberAvailability(request):
    if request.is_ajax() and request.method == "GET":
        jersey_no = request.GET.get('jersey_no', None)

        if jersey_no is not None:
            try:
                jersey_no = int(jersey_no)
                user_with_jersey = CustomUser.objects.filter(jno=jersey_no).first()
                if user_with_jersey is not None:
                    return JsonResponse({"available": False})
                else:
                    return JsonResponse({"available": True})
            except ValueError:
                # Handle invalid jersey number (not a valid integer)
                return JsonResponse({"available": False})

    # Return an error response if the request is not valid
    return JsonResponse({"error": "Invalid request"})




def check_email(request):
    if request.method == "GET":
        email = request.GET.get('email', None)

        if email:
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})

    return JsonResponse({'error': 'Invalid request'})



def reg(request):
    # Count the number of users for each role
    player_count = CustomUser.objects.filter(role='player').count()
    coach_count = CustomUser.objects.filter(role='coach').count()
    staff_count = CustomUser.objects.filter(role='staff').count()

    if request.method == "POST":
        email = request.POST['email']
        contract_start = request.POST.get('cdate')
        cdate = datetime.strptime(contract_start, '%Y-%m-%d')
        sal = request.POST['salary']
        role = request.POST['role']
        pos = request.POST.get('pos')

        try:
            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():
                raise IntegrityError("This email is already registered. Please use a different email.")

            # Check if the maximum limit for a specific role has been reached
            if role == 'player' and player_count >= 15:
                raise IntegrityError("The maximum limit for players has been reached.")
            elif role == 'coach' and coach_count >= 10:
                raise IntegrityError("The maximum limit for coaches has been reached.")
            elif role == 'staff' and staff_count >= 10:
                raise IntegrityError("The maximum limit for staff has been reached.")

            generated_password = generate_password()
            # Create a new custom user instance
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=generated_password,
                sal=sal,
                role=role,
                pos=pos,
                cdate=cdate,
            )
            if role == 'player':
                user.pos = pos
            else:
                user.pos = None

            user.save()
            my_dict = {'password': generated_password, 'email': email}
            html_template = 'email_page.html'
            html_message = render_to_string(html_template, context=my_dict)
            subject = 'Welcome to club'
            email_from = settings.EMAIL_HOST_USER
            recipient = [email]
            message = EmailMessage(subject, html_message, email_from, recipient)
            message.content_subtype = 'html'
            message.send()
            messages.success(request, "Registration successful!")
            return redirect('registration')  # Redirect to the login page after successful registration
        except IntegrityError as e:
            messages.error(request, str(e))  # Display the custom error message
        except ValueError as e:
            messages.error(request, str(e))  # Display the custom error message

    return render(request, 'reg.html')





def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth(request, user)
            
            # Check if the user is a superuser (admin)
            if user.is_superuser:
                request.session['email'] = email
                return redirect('admin1')
            # Check the user's role and redirect accordingly
            elif user.role == 'staff':
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





def admin1(request):
    if 'email' in request.session:
        email = request.session['email']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.is_superuser:
                # Add your admin dashboard logic here
                # For example, you can fetch admin-specific data or perform admin actions

                # Count the number of staff and coaches
                staff_count = CustomUser.objects.filter(role='staff').count()
                player_count = CustomUser.objects.filter(role='player').count()
                coach_count = CustomUser.objects.filter(role='coach').count()
                total_count = player_count + staff_count + coach_count
                other_count = staff_count + coach_count
                users = CustomUser.objects.exclude(is_superuser=True)


                context = {
                    'player_count': player_count,
                    'staff_count': staff_count,
                    'coach_count': coach_count,
                    'total_count': total_count,
                    'other_count': other_count,
                    'users': users,
                    
                }

                response = render(request, 'admin.html', context)
                response['Cache-Control'] = 'no-store, must-revalidate'
                return response
            else:
                messages.error(request, "You don't have permission")
        except User.DoesNotExist:
            pass
    return redirect('login')



def navigate_to_page(request):
    # Get the value of the 'page' parameter from the GET request
    page = request.GET.get('page')

    # Define a dictionary to map page names to their corresponding URLs
    page_urls = {
        'dashboard': 'admin1',  # 'home' is the page name, 'admin_home' is the URL name
        'registration': 'registration',
        'team list': 'adminreg',
        # Add more page names and URL names as needed
    }

    # Check if the page name is in the dictionary
    if page in page_urls:
        # If the page name is valid, redirect to the corresponding URL
        return redirect(page_urls[page])
    else:
        # If the page name is not found, you can handle it, e.g., show an error page
        return redirect('admin_error_page')  # 'admin_error_page' is a placeholder for an error page URL

    # You can customize this logic further based on your requirements







def staff(request):
    if 'email' in request.session:
        email = request.session['email']
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            if user.role == "staff":
                # Check if first_name and last_name are empty; if so, redirect to the update page
                if not user.first_name or not user.last_name:
                    return redirect('staffupdate')
                response = render(request, 'staff.html')
                response['Cache-Control'] = 'no-store, must-revalidate'
                return response
            else:
                messages.error(request, "You don't have permission")
        except User.DoesNotExist:
            pass
    
    return redirect('login')

@login_required  
def staffprofile(request):
    staff = request.user  # Assuming the player is logged in
    context = {
        'staff': staff,
    }
    return render(request, 'staffprofile.html', context)


def staffupdate(request):
    if request.method == 'POST':
        user = request.user  # Assuming the player is logged in
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.age = request.POST.get('age')
        image = request.FILES.get('image')
        if image:
            user.img = image
        user.save()
        return redirect('staffprofile')  # Redirect to the player profile page

    return render(request, 'staffupdate.html', {'user': request.user})


# COACH

def coach(request):
    if 'email' in request.session:
        email = request.session['email']
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            if user.role == "coach":
                # Check if first_name and last_name are empty; if so, redirect to the update page
                if not user.first_name or not user.last_name:
                    return redirect('coachupdate')
                response = render(request, 'coach.html')
                response['Cache-Control'] = 'no-store, must-revalidate'
                return response
            else:
                messages.error(request, "You don't have permission")
        except User.DoesNotExist:
            pass
    
    return redirect('login')


@login_required 
def coachprofile(request):
    coach = request.user  # Assuming the player is logged in
    context = {
        'coach': coach,
    }
    return render(request, 'coachprofile.html', context)


def coachupdate(request):
    if request.method == 'POST':
        user = request.user  # Assuming the player is logged in
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.age = request.POST.get('age')
        image = request.FILES.get('image')
        if image:
            user.img = image
        user.save()
        return redirect('coachprofile')  # Redirect to the player profile page

    return render(request, 'coachupdate.html', {'user': request.user})



from django.utils.timezone import timedelta
from django.db.models import Q
from .models import TrainingSession
from .forms import TrainingSessionForm

def coachaddtraining(request):
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():

            training_date = form.cleaned_data['date']
            coach = request.user
            if coach:
                # Check if a training session with the same date already exists
                existing_session = TrainingSession.objects.filter(
                    Q(date=training_date) & Q(coach=coach)
                ).first()

                if existing_session:
                    messages.error(request, f"A training session for {training_date} already exists.")
                else:
                    # Create a new training session
                    training_session = form.save(commit=False)
                    training_session.coach = coach
                    training_session.save()
                    messages.success(request, f"Training session for {training_date} has been created.")
                    return redirect('coachaddtraining')
            else:
                messages.error(request, "Invalid coach selected.")
        else:
            messages.error(request, "Training session already exist in this date")

    form = TrainingSessionForm()
    return render(request, 'coachaddtraining.html', {'form': form})

from django.shortcuts import render
from .models import TrainingSession

def training_list(request):
   training_sessions = TrainingSession.objects.order_by('date')
   return render(request, 'training_list.html', {'training_sessions': training_sessions})






from django.shortcuts import render, redirect
from .models import PlayerPerformance

def update_performance(request, training_id):
    training_session = TrainingSession.objects.get(pk=training_id)
    players = CustomUser.objects.filter(role='player')

    if request.method == 'POST':
        for player in players:
            # Retrieve the values from the form
            shoot = request.POST.get(f'shoot_{player.email}')
            passing = request.POST.get(f'passing_{player.email}')
            dribble = request.POST.get(f'dribble_{player.email}')
            defense = request.POST.get(f'defense_{player.email}')
            physical = request.POST.get(f'physical_{player.email}')
            speed = request.POST.get(f'speed_{player.email}')

            # Check if shoot is not None and not an empty string
            if shoot is not None and shoot != '':
                try:
                    # Ensure the shoot value is an integer
                    shoot = int(shoot)
                except ValueError:
                    # Handle the case where shoot is not a valid integer
                    shoot = 0
                # Ensure shoot is within the valid range [0, 100]
                shoot = max(0, min(shoot, 100))
            else:
                # If shoot is None or an empty string, set a default value (e.g., 0)
                shoot = 0

            # Create or update PlayerPerformance
            player_performance, created = PlayerPerformance.objects.get_or_create(
                training_session=training_session,
                player=player,
            )
            player_performance.shoot = shoot    
            player_performance.passing = passing
            player_performance.dribble = dribble
            player_performance.defense = defense
            player_performance.physical = physical
            player_performance.speed = speed
            player_performance.save()

        return redirect('training_list')

    return render(request, 'update_performance.html', {'training_session': training_session, 'players': players})




#player



    

def logout(request):
    try:
        del request.session['email']
    except:
        return redirect('index')
    return redirect('index')


def adminreg(request):
        User = get_user_model()
        user_profiles = User.objects.filter(is_superuser=False)  # Exclude superusers

        role_filter = request.GET.get('role')

        if role_filter:
        # Filter user profiles by the selected role
          user_profiles = user_profiles.filter(role=role_filter)


        sort_by = request.GET.get('sort', 'email')  # Default sorting column
        order = request.GET.get('order', 'asc')  # Default sorting order

        # Toggle the sorting order between ascending and descending
        if order == 'asc':
            user_profiles = user_profiles.order_by(sort_by)
            order = 'desc'
        else:
            user_profiles = user_profiles.order_by(f'-{sort_by}')
            order = 'asc'

        context = {'user_profiles': user_profiles, 'order': order, 'sort_by': sort_by}
        return render(request, 'adminreg.html', context)
        
    


    # Pass the data to the template
def adminindex(request):
    return render(request, 'adminindex.html')


def dashboard(request):
    User = get_user_model()
    user_profiles = User.objects.all()
    context = {'user_profiles': user_profiles}
    return render(request, 'dashboard.html')



def player(request):
    if 'email' in request.session:
        email = request.session['email']
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            if user.role == "player":
                # Check if first_name and last_name are empty; if so, redirect to the update page
                if not user.first_name or not user.last_name:
                    return redirect('playerupdate')
                response = render(request, 'player.html')
                response['Cache-Control'] = 'no-store, must-revalidate'
                return response
            else:
                messages.error(request, "You don't have permission")
        except User.DoesNotExist:
            pass
    
    return redirect('login')


@login_required  # Ensure the user is logged in to access this view
def player_profile(request):
    player = request.user  # Assuming the player is logged in
    context = {
        'player': player,
    }
    return render(request, 'playerprofile.html', context)



def playerupdate(request):
    if request.method == 'POST':
        user = request.user  # Assuming the player is logged in
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.age = request.POST.get('age')
        user.jno = request.POST.get('jerseyno')
        image = request.FILES.get('image')
        if image:
            user.img = image
        user.save()
        return redirect('player_profile')  # Redirect to the player profile page

    return render(request, 'playerupdate.html', {'user': request.user})


def player2(request):
    return render(request, 'player2.html')


def training_list1(request):
   training_sessions = TrainingSession.objects.order_by('date')    
   return render(request, 'training_list1.html', {'training_sessions': training_sessions})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import PlayerPerformance

from django.db.models import Avg  # Add this import

@login_required
def playerperformance(request, player_id):
    player = CustomUser.objects.get(email=player_id)  # Retrieve the player using the email
    latest_performance = PlayerPerformance.objects.filter(player=player).last()

    # Calculate the average performance for the player
    average_performance = PlayerPerformance.objects.filter(player=player).aggregate(
        shoot_avg=Avg('shoot'),
        passing_avg=Avg('passing'),
        dribble_avg=Avg('dribble'),
        defense_avg=Avg('defense'),
        physical_avg=Avg('physical'),
        speed_avg=Avg('speed')
    )

    return render(request, 'playerperformance.html', {'player': player, 'latest_performance': latest_performance, 'average_performance': average_performance})




# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class ChatStart(APIView):
    def post(self, request):
        coach_email = request.user.email  # Assuming you have coach authentication
        player_email = request.data.get("player_email")

        # Check if the player exists and is valid
        try:
            player = get_user_model().objects.get(email=player_email, role="player")
        except ObjectDoesNotExist:
            return Response({"error": "Invalid player or player not found."}, status=status.HTTP_400_BAD_REQUEST)

        # You can add additional validation logic here if needed

        # Generate a unique room name (e.g., coach_player) to establish a WebSocket connection
        room_name = f"{coach_email}_{player_email}"

        # Build the WebSocket URL
        websocket_url = f"ws/chat/{room_name}/"

        return Response({"websocket_url": websocket_url}, status=status.HTTP_201_CREATED)



# views.py

from django.http import JsonResponse
from .models import CustomUser

# In views.py
def get_players(request):
    # Fetch a list of player email addresses (excluding the coach's email)
    players = CustomUser.objects.filter(role='player').values_list('email', flat=True)
    data = {'players': list(players)}
    print(data)  # Add this line for debugging
    return JsonResponse(data)

def get_coach_email(request):
    # Fetch the coach's email based on their role
    coach_email = CustomUser.objects.filter(role='coach').values_list('email', flat=True).first()
    data = {'coach_email': coach_email}
    print(data)  # Add this line for debugging
    return JsonResponse(data)





# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import PlayerEmailSerializer

class PlayerEmailListView(APIView):
    def get(self, request):
        players = CustomUser.objects.filter(role='player')
        serializer = PlayerEmailSerializer(players, many=True)
        return Response({"players": serializer.data}, status=status.HTTP_200_OK)


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from .serializers import CoachEmailSerializer

class CoachEmailView(APIView):
    def get(self, request):
        # Retrieve the coach's email based on their role
        try:
            coach_email = CustomUser.objects.get(role='coach').email
            serializer = CoachEmailSerializer({'coach_email': coach_email})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Coach not found'}, status=status.HTTP_404_NOT_FOUND)


from django.shortcuts import render

def chat_with_coach(request):
    return render(request, 'chat_with_coach.html')


def chat_from_coach(request):
    return render(request, 'chat_from_coach.html')


def lobby(request):
    return render(request, 'lobby.html')



from django.shortcuts import render, redirect
from .models import Opponent
from .forms import OpponentForm

def add_opponent(request):
    if request.method == 'POST':
        form = OpponentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_match_schedule')  # Redirect to a page showing the list of opponents
    else:
        form = OpponentForm()
    
    return render(request, 'add_opponent.html', {'form': form})




from django.shortcuts import render, redirect
from .forms import MatchForm
from .models import Match
from datetime import timedelta

def add_match_schedule(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            date = cleaned_data.get('date')
            venue = cleaned_data.get('venue')

            # Check if there are matches with results scheduled on or after the selected date for the same venue
            existing_matches = Match.objects.filter(
                date__gte=date,
                venue=venue,
                result__in=['win', 'draw', 'loss']
            )

            if existing_matches.exists():
                # Matches with results are already scheduled on or after the selected date
                error_message = 'You can only schedule a new match after the date of an already updated match.'
                return render(request, 'add_match_schedule.html', {'form': form, 'error_message': error_message})

            # Check if there is an already updated match with a date after the selected date
            updated_matches = Match.objects.filter(
                date__gt=date,
                result__in=['win', 'draw', 'loss']
            )

            if updated_matches.exists():
                # There is an updated match scheduled after the selected date
                error_message = 'You cannot schedule a match before the date of an already updated match.'
                return render(request, 'add_match_schedule.html', {'form': form, 'error_message': error_message})

            form.save()
            return redirect('admin1')  # Redirect to a success page

    else:
        form = MatchForm()
    return render(request, 'add_match_schedule.html', {'form': form})




def admin_opponent_list(request):
    opponents = Opponent.objects.all()
    return render(request, 'admin_opponent_list.html', {'opponents': opponents})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Opponent

from django.shortcuts import render, redirect, get_object_or_404
from .models import Opponent
from django.contrib import messages

def delete_opponent(request, opponent_id):
    opponent = get_object_or_404(Opponent, opponent_id=opponent_id)
    
    if opponent:
        opponent_name = opponent.name  # Store the opponent name in a variable
        opponent.delete()
        messages.success(request, f"Opponent '{opponent_name}' has been successfully deleted.")
    else:
        messages.error(request, "Opponent not found.")
    
    return redirect('admin_opponent_list')



from django.shortcuts import render
from .models import Match

def match_list(request):
 matches = Match.objects.order_by('date')
 return render(request, 'match_list.html', {'matches': matches})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Match
from .forms import MatchResultForm

def update_result(request, match_id):
    match = get_object_or_404(Match, match_id=match_id)
    non_updated_matches = Match.objects.filter(date__lt=match.date, result='upcoming match')

    if non_updated_matches.exists():
        # There are non-updated match schedules in the past
        error_message = 'You cannot update this match until all previous match schedules are updated.'
        return render(request, 'match_list1.html', {'matches': Match.objects.order_by('date'), 'error_message': error_message})

    if request.method == 'POST':
        form = MatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match_list1')  # Redirect to the match list page after updating
    else:
        form = MatchResultForm(instance=match)

    return render(request, 'update_result.html', {'form': form, 'match': match, 'match_id': match_id})




def match_list1(request):
 matches = Match.objects.order_by('date')
 return render(request, 'match_list1.html', {'matches': matches})

def match_list2(request):
 matches = Match.objects.order_by('date')
 return render(request, 'match_list2.html', {'matches': matches})