from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)
description = """
This is a simple Social Media Aplication. This API had **5 routes**:

### Posts
This route creates, reads, deletes and updates posts (CRUD functionality)


### Users
This route handles creating users and searching users by id


### Authentication
This route handles the user authentication for the applcation


### Vote
This route handles voting('like') and unvoting(remove the 'like') posts. This route currently does not have a dislike functionality


### Root
This route is the default route  

"""
tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. Handles Creating Users and Searching users by id",
    },
    {
        "name": "Posts",
        "description": "Operations with posts. creates, reads, deletes and updates posts (CRUD functionality)",
    },
    {
        "name": "Authentication",
        "description": "Operations with user authentication.",
    },
    {
        "name": "Vote",
        "description": "This route handles voting('like') and unvoting(remove the 'like') posts.",
    },
    {
        "name": "Root",
        "description": "The Default route",
    },
]
app = FastAPI(
    title="Social Media Application API Documentation",
    description=description,
    contact={
        "name": ": Manu Mahadevan Koipalil",
        "email": "manukoip20@gmail.com",
    },
    openapi_tags=tags_metadata,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}


)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router connection connecting router files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Homepage for API


@app.get("/", tags=['Root'])
def root():
    return {"message": "Welcome to my Social Media Application !! -> Add '/docs' to the end of the url to go to the API documentation"}
