from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Category, Product, Sale
from api.serializers import CategorySerializer, ProductSerializer

from api.models import Sale

import json
import stripe

# from api.models import Product
# from api.serializers import ProductSerializer
# Create your views here.
class CategoryList(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        cats = Category.objects.all()
        if request.query_params.get('title'):
            cats = cats.filter(title__contains=request.query_params.get('title'))
        elif request.query_params.get('name'):
            cats = cats.filter(title__contains=request.query_params.get('name'))
        elif request.query_params.get('description'):
            cats = cats.filter(title__contains=request.query_params.get('description'))
        elif request.query_params.get('category'):
            cats = cats.filter(title__contains=request.query_params.get('category'))
        elif request.query_params.get('filename'):
            cats = cats.filter(title__contains=request.query_params.get('filename'))
        elif request.query_params.get('price'):
            cats = cats.filter(title__contains=request.query_params.get('price'))                                                
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self , request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

class CategoryDetail(APIView):
    @csrf_exempt
    def get(self, request, pk, format=None):
        cat = Category.objects.get(id=pk)
        serializer = CategorySerializer(cat)
        return Response(serializer, data)

    @csrf_exempt
    def put(self, request, pk, format=None):
        cat = Category.objects.get(id=pk)
        serializer = CategorySerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, pk, format=None):
        cat = Category.objects.get(id=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        cats = Product.objects.all()
        if request.query_params.get('title'):
            cats = cats.filter(
                title__contains=request.query_params.get('title'))
        serializer = ProductSerializer(cats, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    @csrf_exempt
    def get(self, request, pk, format=None):
        cat = Product.objects.get(id=pk)
        serializer = ProductSerializer(cat)
        return Response(serializer.data)
    @csrf_exempt
    def put(self, request, pk, format=None):
        cat = Product.objects.get(id=pk)
        serializer = ProductSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @csrf_exempt
    def delete(self, request, pk, format=None):
        cat = Product.objects.get(id=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
########################
###  Sales

class CreateSale(APIView):
    '''Creates a sale, including getting a payment intent from Stripe'''
    @csrf_exempt
    def post(self, request, format=None):
        body = json.loads(request.body)

        sale = Sale()
        sale.name = body['name']
        sale.address1 = body['address1']
        sale.address2 = body['address2']
        sale.city = body['city']
        sale.state = body['state']
        sale.zipcode = body['zipcode']
        sale.total = body['total']
        sale.items = body['items']
        sale.payment_intent = stripe.PaymentIntent.create(
            amount=int(sale.total * 100),
            currency='usd',
        )
        sale.save()

        return Response({
            'sale_id': sale.id,     # must have called sale.save() or id will be empty
            'client_secret': sale.payment_intent['client_secret'],
        })