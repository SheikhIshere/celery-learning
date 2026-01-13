from django.shortcuts import redirect

def redirect_doc(request):
    return redirect('swagger-ui')