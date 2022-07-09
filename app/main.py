from os import stat
from tkinter.messagebox import NO
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    difficulty: int = 1
    content: str
    

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='fuckofff', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("connecting to database failed")
        print("error:",error)
        time.sleep(2)



@app.get("/recipes/all")
async def getPosts():
    cursor.execute('''SELECT * FROM recipes''')
    my_recipes=cursor.fetchall()
    return{"data":my_recipes}
    
@app.get("/recipes/{id}")
async def getPost(id : int, response: Response):
    cursor.execute('''SELECT * FROM recipes WHERE id =%s ''',(str(id)))
    recipe = cursor.fetchone()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist  ")
    return{"data":recipe}

@app.post("/recipes", status_code=status.HTTP_201_CREATED)
def create(post: Post):
    cursor.execute("""INSERT INTO recipes (name, content, difficulty) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.difficulty))
    new_post=cursor.fetchone()
    conn.commit()

    return{'data':new_post}

@app.delete("/recipes/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
    cursor.execute('''DELETE FROM recipes WHERE id = %s RETURNING *''',(str(id)))
    recipe= cursor.fetchone
    conn.commit()

    if recipe == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/recipes/{id}",status_code=status.HTTP_206_PARTIAL_CONTENT)
def update(id:int, post:Post):
    cursor.execute('''UPDATE recipes SET name= %s , content= %s, difficulty = %sWHERE id = %s RETURNING *''', (post.title, post.content, post.difficulty, (str(id))))
    updatedPost= cursor.fetchone()
    print(updatedPost)
    conn.commit()
    
    if updatedPost==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return{'data': updatedPost}