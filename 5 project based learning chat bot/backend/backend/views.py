from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import redirect

@api_view(['GET'])
def hello_world(request):
    """Hello world endpoint."""
    return Response({'message': f'Hello World: {datetime.now().isoformat()}'})

def script(request):
    return redirect("swagger-ui")