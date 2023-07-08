from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    # This saves having to write /posts for every route
    prefix="/posts",
    tags=['Posts']
)


# Returns all the posts


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/", response_model=List[schemas.Post])
# Raw SQL method, replaced with SQLAlchemy
# def get_posts():
# cursor.execute("""SELECT * FROM posts""")
# posts = cursor.fetchall()
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Create new post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# Raw SQL method, replaced with SQLAlchemy
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING *""",
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # **post.dict() -> makes the pydantic model into a dictionay
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Returns post with particular id


@router.get("/{id}", response_model=schemas.PostOut)
# Raw SQL method, replaced with SQLAlchemy
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
# delete find_posts() funtion
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                      isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post

# Deleting a post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# Raw SQL method, replaced with SQLAlchemy
# def delete_post(id: int):
#     cursor.execute(
#         """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone
#     conn.commit()
# delete find_index_post() funtion
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating a post

@router.put("/{id}", response_model=schemas.Post)
# Raw SQL method, replaced with SQLAlchemy
# def update_post(id: int, post: Post):
#     # delete find_index_post() funtion
#     cursor.execute("""UPDATE posts SET title = %s,content = %s, published =%s WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
