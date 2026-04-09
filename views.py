from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class StoreView(View):
    def get(self, request):
        products = Product.objects.all()
        my_orders = Order.objects.filter(id__in=request.session.get('my_orders', []), status='paid')
        return render(request, 'shop.html', {'products': products, 'orders': my_orders})


class CheckoutView(View):
    def post(self, request):
        order = Order.objects.create(status='pending')
        line_items = []
        for p in Product.objects.all():
            qty = int(request.POST.get(f'qty_{p.id}', 0))
            if qty > 0:
                OrderItem.objects.create(order=order, product=p, quantity=qty)
                line_items.append({
                    'price_data': {'currency': 'inr', 'unit_amount': int(p.price * 100),
                                   'product_data': {'name': p.name}},
                    'quantity': qty,
                })
        if not line_items: return redirect('/')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'], line_items=line_items, mode='payment',
            client_reference_id=order.id,
            success_url=request.build_absolute_uri(f'/success/?session_id={{CHECKOUT_SESSION_ID}}'),
            cancel_url=request.build_absolute_uri('/'),
        )
        order.stripe_session_id = session.id
        order.save()
        return redirect(session.url, code=303)


class SuccessView(View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if session_id:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                if session.payment_status == 'paid':
                    order = Order.objects.get(id=session.client_reference_id)
                    if order.status != 'paid':
                        order.status = 'paid'
                        order.save()
                        request.session['my_orders'] = request.session.get('my_orders', []) + [order.id]
            except Exception:
                pass
        return redirect('/')