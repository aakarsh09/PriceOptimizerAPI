from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)
        columns = [
            {
                "field": field.name,
                "headerName": field.verbose_name.title()
            }
            for field in Product._meta.fields
            if field.name != 'id'
        ]

        return Response({
            "columns": columns,
            "rows": data.data
        })
