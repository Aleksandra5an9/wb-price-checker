def main():
    message = "📦 Цены товаров на WB:\n"
    for wb_id in WB_IDS:
        price = get_price_via_search(wb_id)
        if price:
            message += f"- {wb_id}: {price} ₽\n"
        else:
            message += f"- {wb_id}: не найден\n"
    send_message(message)
