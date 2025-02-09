from fastapi import FastAPI, Form, Depends, Query, Path, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse 
import json


app=FastAPI() # 建立FastAPI物件
templates = Jinja2Templates(directory="file")
VALID_USERNAME = "test"
VALID_PASSWORD = "test" 

app.add_middleware(SessionMiddleware, secret_key="Safety Key")



@app.get("/",  response_class=HTMLResponse) # 主頁面(根路徑)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/square/{num}", response_class=HTMLResponse)
async def square(
    request: Request, 
    num: Annotated[int, Path(ge=1)],
    ):
        result=num*num
        return templates.TemplateResponse("square.html", {"request": request, "result": result}) # 登入狀態為"登入"，才可以進入member
    

@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if not request.session.get("SIGNED_IN"):  
        return RedirectResponse(url="/") # 未登入者強制導回首頁

    return templates.TemplateResponse("member.html", {"request": request}) # 登入狀態為"登入"，才可以進入member

@app.get("/error",response_class=HTMLResponse)
async def error_page(request: Request, message: str = "Unknown error", status_code=303):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
    

@app.post("/signin")
async def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        request.session["SIGNED_IN"] = True  # 設定 Session 為已登入
        return RedirectResponse(url="/member", status_code=303)
    elif not username or not password :
        return RedirectResponse(url="/error?message=Please enter username and password", status_code=303)
    else:
        return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)
    
@app.get("/signout")
async def signout(request: Request):   
    request.session["SIGNED_IN"] = False  # 登入狀態為:"登出"
    return RedirectResponse(url="/")  # 重新導向至首頁根目錄

app.mount(
    "/",
    StaticFiles(directory="file",)
)