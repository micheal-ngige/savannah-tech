from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from africastalking import SMS

@login_required
def order_list(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.save()

            # Send SMS
            try:
                phone_number = order.customer.phone
                message = f"Order placed: {order.item} - {order.amount}"
                SMS.send(message, [phone_number])
            except Exception as e:
                print(f"Error sending SMS: {e}")

            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})
