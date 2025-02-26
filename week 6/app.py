from fastapi import FastAPI, Form, Depends, Query, Path, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 

import mysql.connector
con=mysql.connector.connect(
    user="root",
    password="123456",
    host="localhost",
    database="website"
)



app=FastAPI()
templates = Jinja2Templates(directory="file")
app.add_middleware(SessionMiddleware, secret_key="Safety Key")



@app.get("/") # 主頁面(根路徑)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/error",response_class=HTMLResponse)
async def error_page(request: Request, message: str = "Unknown error", status_code=303):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
    
@app.post("/signup")
def signup(name: str=Form(...), 
           username: str=Form(...), 
           password: str=Form(...)
           ):
        cursor=con.cursor()
        cursor.execute("SELECT * FROM member WHERE username = %s ", (username,))
        existed_user = cursor.fetchone()

        if existed_user:
            return RedirectResponse(url="/error?message=Repeated username", status_code=303) 
        else:
            cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
            con.commit()
            return RedirectResponse(url="/", status_code=303) # post方式轉成get，使用status_code=303 導回首頁

@app.post("/signin")
def signin(request: Request, 
           signInUsername: str=Form(...),
           signInPassword: str=Form(...)
           ):
        cursor=con.cursor(dictionary=True) # 建立cursor物件操作資料庫
        cursor.execute("SELECT * FROM member where username=%s and password=%s ", (signInUsername, signInPassword))
        login_in_user = cursor.fetchone()
        print(login_in_user)
        if login_in_user:
            request.session["SIGNED_IN"] = True  # 設定 Session 為已登入
            request.session["user_id"] = login_in_user["id"]
            request.session["name"] = login_in_user["name"]
            request.session["USERNAME"] = login_in_user["username"] # 存入 username
            return RedirectResponse(url="/member", status_code=303)
        
        return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)

             
@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    if not request.session.get("SIGNED_IN"):  # 未登入者強制導回首頁
        return RedirectResponse(url="/", status_code=303) 
    name=request.session.get("name")
    username = request.session.get("USERNAME")  # 取得儲存在 session 的帳號
    user_id = request.session.get("user_id")

    cursor=con.cursor(dictionary=True)
    cursor.execute("""
        SELECT member.username, message.content
        FROM message
        JOIN member ON message.member_id = member.id
    """)
    messages = cursor.fetchall()  # 取得留言列表
    return templates.TemplateResponse("member.html", {"request": request, "username":username, "messages": messages, "name":name}) # 登入狀態為"登入"，才可以進入member

@app.get("/signout")
def signout(request: Request):
    request.session.clear()  # 清除 session
    return RedirectResponse(url="/", status_code=303)
    
@app.post("/createMessage")
def leave_message(
                request: Request, 
                content: str=Form(...)
                ):
    user_id = request.session.get("user_id")  # 取得登入者的 user_id
    if not request.session.get("SIGNED_IN"):  # 未登入者強制導回首頁
        return RedirectResponse(url="/", status_code=303)

    cursor = con.cursor()
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (user_id, content)) # 插入留言 (content + member_id)
    con.commit() # 確認動作

    return RedirectResponse(url="/member", status_code=302)  # 發送後回到會員頁
    

    

app.mount(
    "/",
    StaticFiles(directory="file")
)