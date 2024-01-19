# externally imports of resources
from fastapi import Path, Query, APIRouter, Depends, HTTPException, status
from typing import Annotated
from bson import ObjectId
import pendulum
# internally relative imports of resources
from ...config.connection import db
from ...depencies.user import retrieve_current_user
from ...Interface.user.user_interface import UserInterface
from ...models.product.product_base import Product_Base
from ...schema.products import ProductEmptity
from ...models.product.products import Product
from ...schema.products import ProductsEmptity
from ...models.sale.sales import Sale_Base
from ...models.sale.saleOuput import SaleOuput
from ...enums.index import ProductTags
from ...models.user.response import Response

productRouter: APIRouter = APIRouter(prefix="/product")

@productRouter.get("/allproducts", tags=[ProductTags.ALL_PRODUCTS], status_code=status.HTTP_200_OK,
                   description="a of all products on the  platform")
async def all_product(limit: Annotated[int, Query(gt=100, lt=1000, 
                                                  title="LIMIT_OF_NUMBER", description="number of products per page")]):
    products = await db.products.find().to_list(length=limit)
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content")
    serialize_products = ProductsEmptity(products)
    return serialize_products
        
@productRouter.get("/user_products", tags=[ProductTags.RELATED_PRODUCTS], status_code=status.HTTP_200_OK,
                   response_description="product information related to specific user")
async def retrieve_user_products(current_user: Annotated[UserInterface, Depends(retrieve_current_user)],
                                 limit: Annotated[int, Query(gt=70, lt=101)]):
    products = await db.products.find({"owner._id": current_user["_id"]}).to_list(length=limit)
    print(products)
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="NO CONTENT")
    serialize_product = ProductsEmptity(products)
    return serialize_product


@productRouter.post("/create_product", response_description="product creation", tags=[ProductTags.SINGLE_PRODUCT],
                    status_code=status.HTTP_201_CREATED)
async def create_product(current_user: Annotated[UserInterface, Depends(retrieve_current_user)],
                         product_inputs: Product_Base) -> Response:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    dump_product_input = product_inputs.model_dump(exclude_unset=True, mode="json")
    product_content = Product(**dump_product_input, date_created=pendulum.now(tz="America/Port-au-prince"), 
                              date_updated=pendulum.now(tz="America/Port-au-prince"), sales=[])
    update_product = product_content.model_copy(update={"owner": current_user})
    
    try:      
        add_new_product = await db.products.insert_one(dict(update_product))
        if not add_new_product.acknowledged:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return Response(message=f"prouduct {product_inputs.product_name} created with success", success=True)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@productRouter.get("/one_product/{product_id}", response_description="single product", tags=[ProductTags.SINGLE_PRODUCT])
async def retrieve_one_product(product_id: Annotated[str, Path(max_length=70, 
                                                               title="PRODUCT_ID", description="unique product id")]):
    if not product_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="product id must not be empty")
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    serialize_product = ProductEmptity(product)
    return serialize_product
    

@productRouter.patch("/{product_id}", tags=[ProductTags.RELATED_PRODUCTS], response_description="altering product info",
                     status_code=status.HTTP_202_ACCEPTED, response_model=Product)
async def update_user_product(current_user: Annotated[UserInterface, Depends(retrieve_current_user)],
                      product_id: Annotated[str, Path(max_length=70, title="PRODUCT_ID", description="unique product id")], product_inputs: Product_Base):
    if not product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    retrieve_product_inputs = product_inputs.model_dump(exclude_unset=True, mode="json")
    product = await db.products.find_one_and_update({"_id": ObjectId(product_id), "owner": {"_id": ObjectId(current_user["_id"])}}, retrieve_product_inputs)
    if not product:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No content")
    serialize_product = ProductEmptity(product)
    return serialize_product
    

@productRouter.put("/buy_product", tags=[ProductTags.SINGLE_PRODUCT], response_description="buying new product",
                    status_code=status.HTTP_200_OK, response_model=Product, response_model_exclude_unset=True)
async def purchase_product(product_name: Annotated[str, Query(max_length=40, min_length=3)],
                           current_user: Annotated[UserInterface, Depends(retrieve_current_user)],
                           product_id: Annotated[str, Query(max_length=70, alias="_id", title="PRODUCT_ID",
                                                            description="unique product id")],
                           sale_inputs: Sale_Base):
    
    retrieve_sale_inputs = SaleOuput(**sale_inputs.model_dump(exclude_unset=True), date_selling=pendulum.now(tz="America/Port-au-prince"))
    update_sale_inputs = retrieve_sale_inputs.model_copy(update={"product": product_name})
    serialize_sale_inputs = update_sale_inputs.model_dump(exclude_unset=True, mode="json")
    try:
       product = await db.products.find_one_and_update({"_id": ObjectId(product_id), "owner._id": current_user["_id"]}, 
                                            {"$set": {"date_updated": pendulum.now(tz="America/Port-au-prince"), "$push": {"sales": dict(serialize_sale_inputs)}}})
       print(product)
       serialize_product = ProductEmptity(product)
       return serialize_product
    except Exception as error:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    

@productRouter.delete("/{product_id}", response_description="delete single product", status_code=status.HTTP_200_OK,
                      tags=[ProductTags.SINGLE_PRODUCT])
async def delete_product(product_id: Annotated[str, Path(max_length=70, title="PRODUCT_ID", 
                                                         description="unique product id")]) -> Response:
    product = await db.products.find_one_and_delete({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return Response(message="product {} successfully deleted".format(product_id), success=True)