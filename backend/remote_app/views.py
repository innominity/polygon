from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import RemoteApp, RemoteAppFileConfigType
from .serializers import RemoteAppFileConfigTypeSerializer


@api_view(["POST", "GET"])
def app_main(request, app_slug):
    try:
        if request.method == "GET":
            remote_app = RemoteApp.objects.get(slug=app_slug)
            app_config_types = RemoteAppFileConfigType.objects.filter(
                remote_app=remote_app
            )
            serializer = RemoteAppFileConfigTypeSerializer(app_config_types, many=True)
            response = {
                "name": remote_app.name,
                "version": remote_app.get_version(),
                "description": remote_app.description,
                "config": serializer.data,
            }
            return JsonResponse(
                response, json_dumps_params={"ensure_ascii": False}, status=200
            )
        elif request.method == "POST":
            # Ожидаем в запросе файлы конфигурации и словарь параметров ПО
            pass
    except Exception as e:
        return JsonResponse(
            {"exception_message": str(e)},
            json_dumps_params={"ensure_ascii": False},
            status=200,
        )
