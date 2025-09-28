from rest_framework.response import Response
from rest_framework import views, status


class PingAPI(views.APIView):
    permission_classes = []
    def get(self, request):
        return Response(
            data={
                "Status": "success", 
                "Message": "pong"
            }, 
            status=status.HTTP_200_OK
        )
