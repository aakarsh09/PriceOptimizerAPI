from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Prefetch
from .models import Product, Sales
from .serializers import SaleWithProductSerializer
from .permissions import IsAdminGroupOrReadOnly

class ProductViewSet(ModelViewSet):
    queryset = Sales.objects.select_related('product').all()
    serializer_class = SaleWithProductSerializer
    permission_classes = [IsAdminGroupOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name', 'product__category']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page else queryset, many=True)

        columns = [
            {"field": "name", "headerName": "Product Name"},
            {"field": "category", "headerName": "Product Category"},
            {"field": "cost_price", "headerName": "Cost Price"},
            {"field": "selling_price", "headerName": "Selling Price"},
            {"field": "description", "headerName": "Description"},
            {"field": "stock_available", "headerName": "Available"},
            # {"field": "customer_rating", "headerName": "Customer Rating"},
            # {"field": "demand_forecast", "headerName": "Demand Forecast"},
            # {"field": "optimized_price", "headerName": "Optimized Price"},
            {"field": "units_sold", "headerName": "Units Sold"},
        ]

        response_data = {
            "columns": columns,
            "rows": serializer.data
        }

        return self.get_paginated_response(response_data) if page else Response(response_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 400, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Product & Sale record created successfully"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
