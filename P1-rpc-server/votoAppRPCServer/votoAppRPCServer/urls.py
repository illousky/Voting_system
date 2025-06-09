from modernrpc.views import RPCEntryPoint
from django.urls import path

urlpatterns = [path("rpc/", RPCEntryPoint.as_view(), name="rpc")]