from django.contrib import messages
from django.forms import formset_factory
from pizza.forms import MultiplePizzaForm, PizzaForm
from pizza.models import Pizza, Size
from django.shortcuts import render, HttpResponse, get_object_or_404
from .serializers import PizzaSerializer, SizeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def index(request):
    return HttpResponse('<h1>API Page</h1>')

@api_view(['GET', 'POST'])
def pizzas_api(request):
    if request.method == 'GET':
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Pizza {serializer.validated_data.get('topping1')}, {serializer.validated_data.get('topping2')} saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def pizzas_api_get_update_delete(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    if request.method == 'GET':
        serializer = PizzaSerializer(pizza)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = PizzaSerializer(pizza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Pizza order updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = PizzaSerializer(pizza, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Pizza updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pizza.delete()
        data = {
            "message": f"Pizza order deleted successfully"
        }
        return Response(data)

@api_view(['GET', 'POST'])
def size_api(request):
    # from rest_framework.decorators import api_view
    # from rest_framework.response import Response
    # from rest_framework import status

    if request.method == 'GET':
        sizes = Size.objects.all()
        serializer = SizeSerializer(sizes, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        # from pprint import pprint
        # pprint(request)
        serializer = SizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Size saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
def home(request):
    pizzas = Pizza.objects.all()
    context = {
        "pizzas":pizzas,
    }
    return render(request, 'pizza/home.html', context)

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id

            size = filled_form.cleaned_data.get('size')
            topping1 = filled_form.cleaned_data.get('topping1')
            topping2 = filled_form.cleaned_data.get('topping2')

            messages.success(request, f'Thanks for ordering! Your {size}, {topping1} and {topping2} pizza is on its way!')

            filled_form = PizzaForm()
        else:
            created_pizza_pk = None
            messages.warning(request, 'Pizza order failded, try again!')

        return render(request, 'pizza/order.html', {'created_pizza_pk':created_pizza_pk, 'pizzaform':filled_form,
'multiple_form':multiple_form})

    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form':multiple_form})

def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data.get('number')
        # doldurulmus = PizzaForm(request.POST)
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == "POST":
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            # print(filled_formset)
            for form in filled_formset:
                form.save()
            messages.success(request, 'Pizzas have been ordered!')

        else:
            messages.warning(request, 'Order was not created, please try again')

        return render(request, 'pizza/pizzas.html', {'formset': formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset': formset})

def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            messages.success(request, 'Order has been updated')

            return render(request, 'pizza/edit_order.html', {'pizzaform':form,'pizza':pizza})

    return render(request, 'pizza/edit_order.html', {'pizzaform':form,'pizza':pizza})


