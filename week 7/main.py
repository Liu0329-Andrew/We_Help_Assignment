from fastapi import FastAPI, Request, Form
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles 
import mysql.connector

app=FastAPI() # 建立API物件
templates = Jinja2Templates(directory="file")
app.add_middleware(SessionMiddleware, secret_key="Safety Key")


con=mysql.connector.connect( # 建立python MySQL連線物件
    user="root",
    password="123456",
    host="localhost",
    database="website"
)



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



@app.get("/api/member")
def get_member(username:Annotated[str, None], request: Request):
    if not request.session.get("SIGNED_IN"):  # 未登入者強制導回首頁
        return RedirectResponse(url="/", status_code=303) 
    
    cursor=con.cursor()
    cursor.execute("select id, name from member where username=%s", (username,))
    result=cursor.fetchone()
    
    if result:
        id, name=result
        return {"data": {
            "id":id, # type=list，取出第一個值
            "name":name, # type=list，取出第一個值
            "username":username
        }}
    
    return {"data": None}

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

class UpdateMemberName(BaseModel):
    name: str  # 確保 name 必須是字串

@app.patch("/api/member")
def update_member(request:Request,
                  member: UpdateMemberName
                  ):
    if not request.session.get("SIGNED_IN"):
        return RedirectResponse(url="/", status_code=303) 
    
    username=request.session.get("USERNAME") # 取得帳號名
    cursor = con.cursor()
    cursor.execute("UPDATE member SET name = %s WHERE username = %s", (member.name, username))
    con.commit()

    if cursor.rowcount > 0: # 如果資料庫被更新成功
        return {"ok": True}
    return {"error": True}  # 若更新未成功，回傳錯誤


    


app.mount(
    "/",
    StaticFiles(directory="file")
)
