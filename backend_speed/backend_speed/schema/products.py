from ..Interface.product.product_interface import Product

def ProductEmptity(product_data: Product) -> Product:
    return {
        "_id": str(product_data["_id"]),
        "product_name": product_data["product_name"],
        "product_description": product_data["product_description"],
        "price": product_data["price"],
        "sales": product_data["sales"],
        "owner": product_data["owner"],
        "date_created": product_data["date_created"],
        "date_updated": product_data["date_updated"]
    }
   
    
def ProductsEmptity(product_data: list[Product]) -> list[Product]:
    return [ProductEmptity(product) for product in product_data]