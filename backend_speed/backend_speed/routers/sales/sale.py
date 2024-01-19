from fastapi import APIRouter, Path, Query, Depends, HTTPException, status
from typing import Annotated
from ...config.connection import db
from ...depencies.user import retrieve_current_user
from ...Interface.user.user_interface import UserInterface
from ...schema.products import ProductEmptity
from ...enums.index import SaleTags
from ...models.product.products import Product

saleRouter: APIRouter = APIRouter(prefix="/sale")

@saleRouter.get("/{product_name}", tags=[SaleTags.ALL_SALES], response_description="all sales by products",
               status_code=status.HTTP_200_OK, response_model=Product)
async def retrieve_product_sale(product_name: Annotated[str, Path(max_length=30, min_length=5, strict=True, 
                                                   title="PRODUCT_NAME", description="single product name")],
                                product_id: Annotated[str, Query(max_length=70, min_length=6, title="PRODUCT_ID",
                                                                 description="unique product id")],
                                current_user: Annotated[UserInterface, Depends(retrieve_current_user)]):
    
    if not product_name or not product_id or not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    sale_by_product = await db.products.find_one({"_id": product_id, "product_name": product_name, 
                                                  "owner._id": current_user["_id"], 
                                                  "sales.product": {"$eq": product_name}})
    if not sale_by_product:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content")
    serialize_product_sale = ProductEmptity(sale_by_product)
    return serialize_product_sale


@saleRouter.patch("/{product_name}", tags=[SaleTags.SINGLE_SALE], response_model=Product)
async def udpate_sale(product_name: Annotated[str, Path(max_length=30, min_length=5, strict=True,
                                                        title="PRODUCT_NAME", description="single product name")], 
                      quantity: Annotated[int, Query(gt=1, le=20, title="PRODUCT_QUANTITY", 
                                                     strict=True, description="number of product")],
                      current_user: Annotated[UserInterface, Depends(retrieve_current_user)]):
    if not quantity or current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    try:
        product_sales = await db.products.find_one_and_update({"product_name": product_name, "owner._id": current_user["_id"]},
                                                              {"$set": {"sales.$.quantity": quantity}})
        serialize_product_sale = ProductEmptity(product_sales)                                                      
        return serialize_product_sale
    except Exception as error:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    

@saleRouter.delete("/{product_name}", tags=[SaleTags.SINGLE_SALE], response_model=Product,
                   response_description="delete a sale from a specic product")
async def delete_product(product_name: Annotated[str, Path(max_length=30, min_length=5, title="PRODUCT_NAME",
                                                           description="single product name")], 
                         current_user: Annotated[UserInterface, Depends(retrieve_current_user)]):
    if not product_name or not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    product = await db.products.find_one_and_update({"product_name": product_name}, {
        "$pull": {"sales": {"product": product_name}}
    })
    serialize_product = ProductEmptity(product)
    return serialize_product