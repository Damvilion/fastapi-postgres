from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:

    try:
        # connects to database
        conn = psycopg2.connect(host='localhost', database='backend', user='postgres',
                                password='', cursor_factory=RealDictCursor)
        # set up a cursor to execute sql commands
        cursor = conn.cursor()
        print("Success!")
        break
    except Exception as error:
        print("Connection failed ")
        print(error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


@app.get("/")
def index():
    return {"data": "New page"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    new_post = cursor.fetchone()
    if not new_post:
        return {"data": "Not FOund"}
    return {"data": new_post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    return {"data": deleted_post}
