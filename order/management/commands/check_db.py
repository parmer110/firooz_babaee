from django.core.exceptions import ObjectDoesNotExist
from order.models import WarehouseOrder

def check_warehouse_orders():
    orphan_orders = []
    for order in WarehouseOrder.objects.all():
        try:
            # اینجا فرض می‌کنیم که هر سفارش حداقل باید به یک شرکت مرتبط باشد
            print(f"Checking order {order.id}")
            if not order.company:
                orphan_orders.append(order)
        except ObjectDoesNotExist:
            orphan_orders.append(order)
    
    if orphan_orders:
        print("Found orphan orders:")
        for order in orphan_orders:
            print(order.id)
    else:
        print("No orphan orders found.")

# اجرای اسکریپت بررسی
check_warehouse_orders()
