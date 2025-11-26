from fastapi import FastAPI,Query,Body
from pydantic import BaseModel, Field
from typing import List,Literal,Annotated
from enum import Enum

class ModelName(int, Enum):
    alexnet = 1
    resnet = 2
    lenet = 3

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about")
def rea_about():
    return {"About": "This is a sample FastAPI application."}


@app.get("/blog/{id}")
def get_blog(id: int):
    return {"Blog": id}


@app.get("/blogStr/{id}")
def get_blog(id: str):
    return {"Blog": id}


@app.get("/models/{mode_name}")
def get_model(mode_name: ModelName):
    if mode_name == ModelName.alexnet:
        return {"model_name": mode_name, "message": "Deep Learning FTW!"}

    if mode_name.value == 2:
        return {"model_name": mode_name, "message": "LeCNN all the images"}

    return {"model_name": mode_name, "message": "Have some residuals"}


@app.get("/modelsInt/{mode_name}")
def get_model(mode_name: int):
    if mode_name == ModelName.alexnet.value:
        return {"model_name": mode_name, "message": "Deep Learning FTW!"}

    if mode_name == ModelName.resnet.value:
        return {"model_name": mode_name, "message": "LeCNN all the images"}

    return {"model_name": mode_name, "message": "Have some residuals"}



# here the paramter name is file_path and we are using path converter
# means any path after /files/ will be captured
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}


#query parameters
@app.get("/blog/{id}/comments")
def get_comments(id:int, limit: int = 10, published: bool = True, sort: str = "asc"):
    if published:
        return {"id": id, "comments": f"{limit} published comments", "sort": sort}
    else:
        return {"id": id, "comments": f"{limit} comments", "sort": sort}


#required query parameter
@app.get("/blog/{id}/commentsRequired")
def get_comments_required(id:int, limit: int, published: bool = True):
    if published:
        return {"id": id, "comments": f"{limit} published comments"}
    else:
        return {"id": id, "comments": f"{limit} comments"}
    

#----------------------------
class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None


@app.post("/items")
def create_item(item: Item):
    item_doct = item.model_dump()  # convert pydantic model to dict
    
    if item.tax is not None :
        total_price = item.price + item.tax
        item_doct.update({"total_price": total_price})
    return item



#=--------------  query parameter with model -----------------

class BlogQueryParams(BaseModel):

    model_config = {"extra": "forbid"} # forbid extra fields not defined in the model

    limit : int = Field(100,gt=0, lt=1000)
    published : bool = True
    sort : Literal["asc","desc"] = "asc"
    tags : List[str] | None = []

    
@app.get("/blog/{id}/commentsModel")
def get_comments_model(id:int,params : Annotated[BlogQueryParams,Query()]):
    if params.published:
        return {"id": id, "comments": f"{params.limit} published comments", "sort": params.sort, "tags": params.tags}
    else:
        return {"id": id, "comments": f"{params.limit} comments", "sort": params.sort, "tags": params.tags}
    


#---- multi body parameters -----

class User(BaseModel):
    username : str
    email : str
    full_name : str | None = None

class Image(BaseModel):
    url : str
    alias : str | None = None

@app.post("/user/image")
def create_user_image(user: User, image: Image):
    user_dict = user.model_dump()
    image_dict = image.model_dump()
    return {"user": user_dict, "image": image_dict}


# ------- multi body parameters with query params -----
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)]=20,
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# ------- body parameters with embedded models -----
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results