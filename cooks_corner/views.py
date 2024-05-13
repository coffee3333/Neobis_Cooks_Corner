from drf_yasg import openapi
from rest_framework import mixins, generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from cooks_corner.models import Recipe, Category
from cooks_corner.pagination import CustomPagination
from cooks_corner.serializers import RecipeSerializer, CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


class RecipeCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):

        try:
            # Code that might raise an exception
            self.create(request, *args, **kwargs)
        except Exception as e:
            return e
                
        
        # return self.create(request, *args, **kwargs)


class RecipeListView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination


    @swagger_auto_schema(
        operation_description="Этот эндпоинт позволяет получить "
        "список туров. Вы можете применить "
        "поиск по заголовку или по id.",
        responses={200: RecipeSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                "category_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Отфильтровать туры по id категории.",
            ),
            openapi.Parameter(
                "category_name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Отфильтровать туры по названию категории.",
            ),
        ],

    )
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Применение фильтров по категориям, начальной и конечной датам
        category_id = request.query_params.get("category_id")
        category_name = request.query_params.get("category_name")

        if category_id and category_name:
                return Response(
                    {"error": "Search via one parametr"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if category_name:
            queryset = queryset.filter(category__name=category_name)


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)