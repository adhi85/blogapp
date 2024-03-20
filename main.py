from fastapi import FastAPI
from routers import blogs, auth, users, dashboard, adminuser

app = FastAPI(
    title="Blog API",
    description="A blogapp API",
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Blogs API. Visit /docs for documentation."}


app.include_router(auth.router)
app.include_router(adminuser.router)
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(dashboard.router)
