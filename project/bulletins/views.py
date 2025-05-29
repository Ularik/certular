from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bulletins
from .serializers import BulletinsSerializer
from django.http import FileResponse, JsonResponse


class BulletinsListView(ListView):
    queryset = Bulletins.objects.all()
    template_name = 'bulletins/bulletins.html'
    context_object_name = 'bulletins'


def get_bulletins(request):
    if request.method == 'GET':
        queryset = Bulletins.objects.all().order_by('created_at')
        serializer = BulletinsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

