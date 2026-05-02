from flowlens import lens
import time

# --- VALIDATION LAYER (INTERNAL PROCESS) ---
@lens.track_stats
def validate_user(user_id):
    return {"status": "ok", "tier": "premium"}

@lens.track_stats
def check_inventory_stock(sku):
    return True

@lens.track_stats
def verify_credit_limit(user_id, amount):
    return amount < 5000

# --- CALCULATION LAYER (INTERNAL PROCESS) ---
@lens.track_stats
def calculate_subtotal(items):
    return sum(item['p'] for item in items)

@lens.track_stats
def apply_loyalty_discount(total):
    return total * 0.90

@lens.track_stats
def calculate_tax(net_amount):
    return net_amount * 0.19

@lens.track_stats
def estimate_shipping_cost(region):
    return 15.50

@lens.track_stats
def sum_final_total(net_amount, tax, shipping):
    return net_amount + tax + shipping

# --- OUTPUT LAYER (DATA OUTPUT) ---
@lens.track_stats
def generate_print_label(data):
    return f"PRINT_LABEL_PDF_{data['id']}"

@lens.track_stats
def display_screen_confirmation(msg):
    print(f"SCREEN: {msg}")
    return "Render success"

@lens.track_stats
def display_security_alert(alert_type):
    print(f"ALERT: {alert_type}")
    return "Alert sent"

# --- ORCHESTRATION PROCESSES ---
@lens.track_stats
def authorize_payment(user_id, total):
    if verify_credit_limit(user_id, total):
        return "PAYMENT_APPROVED"
    return "REJECTED"

@lens.track_stats
def prepare_logistics(region, order_id):
    cost = estimate_shipping_cost(region)
    return generate_print_label({"id": order_id, "cost": cost})

@lens.track_stats
def process_full_order(user_id, products, zone):
    # 1. Validation
    user = validate_user(user_id)
    check_inventory_stock("SKU-99")
    
    # 2. Calculations
    sub = calculate_subtotal(products)
    net = apply_loyalty_discount(sub)
    tax = calculate_tax(net)
    
    # 3. Payment
    payment = authorize_payment(user_id, net)
    
    # 4. Logistics & Output
    logistics = prepare_logistics(zone, "ORD-123")
    display_screen_confirmation(f"Order {payment} successfully.")
    
    return "ORDER_FINISHED"

# --- TEST EXECUTION ---
if __name__ == "__main__":
    cart = [{'n': 'Laptop', 'p': 1000}, {'n': 'Mouse', 'p': 50}]
    
    lens.start()
    # This process will trigger the 15-step chain
    process_full_order("HANS_SALDIAS", cart, "RM_CHILE")
    lens.stop()
