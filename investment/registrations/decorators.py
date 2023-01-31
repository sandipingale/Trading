from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function


def allowed_user(allowed_groups=[]):
    def decorator_function(view_function):
        def wrapper_function(request, *args, **kwargs):
            #print("allowed Roles ", allowed_groups)
            db_groups = [x.name for x in request.user.groups.all()]
            common_groups = set(allowed_groups).intersection(set(db_groups))

            if len(common_groups) > 0:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to use this function")

        return wrapper_function

    return decorator_function