import enum
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
    title: str
    difficulty: int = 1
    content: str
    id:int = 0
    

app = FastAPI()

my_recipes=[{"title": "post 1","content":"content of post 1",'id':1},{"title":"post 2","content":"content of post 2",'id':2}]

def find_post(id):
    for p in my_recipes:
        if p["id"]==id:
            return p

def find_index(id):
    for i , p in enumerate(my_recipes):
        if p["id"]==id:
                return i

@app.get("/")
def root():
    return{"message":"Hello world"}

@app.get("/recipes/all")
async def getPosts():
    return{"data":my_recipes}
    
@app.get("/recipes/{id}")
async def getPost(id : int, response: Response):
    recipe=find_post(id)
    if recipe == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return{"data":recipe}

@app.post("/recipes", status_code=status.HTTP_201_CREATED)
def create(post: Post):
    new_post=post.dict()
    new_post['id']=randrange(0,1000000)
    my_recipes.append(new_post)

    return{'data':new_post}

@app.delete("/recipes/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
    index=find_index(id)
    if  index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_recipes.pop(find_index(id))
    return{'message':"post deleted"}

@app.put("/recipes/{id}",status_code=status.HTTP_206_PARTIAL_CONTENT)
def update(id:int, post:Post):
    index=find_index(id)
    if  index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_dict=post.dict()
    post_dict['id']=id
    my_recipes[index]=post_dict
    return{'data': post_dict}