from ..Interface.sale.sale_interface import Sale_interface

def saleEmptity(sale: Sale_interface):
    return {
        "product": sale["product"],
        "quantity": sale["quantity"],
        "date_selling": sale["date_selling"]
    }