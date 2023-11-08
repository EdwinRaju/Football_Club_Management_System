from django.shortcuts import redirect


class PlayerProfileUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is a player and their first_name and last_name are empty
        if (
            request.user.is_authenticated
            and request.user.role == 'player'
            and (not request.user.first_name or not request.user.last_name)
        ):
            # Redirect to the playerupdate view
            print("Middleware executed")

            return redirect('playerupdate')

        response = self.get_response(request)
        return response
