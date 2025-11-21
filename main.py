from fastapi import FastAPI
from fastapi import FastAPI, Request, UploadFile, File, Form
import shutil
import os
from fastapi.responses import FileResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db import get_db_session
import psycopg
from config import settings

# Serve static folder

app= FastAPI()
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# templates = Jinja2Templates(directory="templates")





@app.get("/health")
async def health():
    try:
        
        with get_db_session() as session:
            session.execute(text("SELECT 1"))
            #print("All good!")
            return {"DB-Health":"ok"}
    except:
        return {"DB-Health":"down"}



@app.get("/")
async def root():
    return {"hello":"world"}

@app.get("/hi")
async def hi():
    return {"Hi":"Uthra"}

@app.get("/hello")
async def hello():
    return {"HELLO":"this is Uthra"}


@app.get("/add")
async def add(x: int = 10, y: int = 20):
    res=x+y
    return {"result":res}

@app.get("/multiply")
async def multiply(x: int = 10, y: int = 20):
    res=x*y
    return {"result":res}

app.mount("/app",StaticFiles(directory="vite-project/dist" , html=True),name="app")



job_boards={"acme": [{"title":"Software Engineer","jobDescription":"Builds, tests, and maintains software systems to deliver reliable, scalable, and efficient applications."},
            { "title":"HR Manager","jobDescription":"Leads recruitment, employee relations, and HR operations to build a productive, compliant, and engaged workforce."}],
            "bcg":[{"title":"Technical Architect","jobDescription":"Designs and oversees high-level technical solutions, ensuring system scalability, performance, and alignment with business needs."},
            { "title":"Junior Software Developer","jobDescription":"Assists in coding, testing, and debugging applications while learning best practices under senior developer guidance."}],
            "atlas":[{"title":"Design Engineer", "jobDescription":"Develop UI/UX webpages"},
            { "title":"Senior Software Developer","jobDescription":"Develop software in Java Springboot"}]
}

@app.get("/api/job-board/{company_name}")
async def company_job_board(company_name):
    return job_boards[company_name]

# @app.get("/api/job-board/{company}")
# def job_list(request: Request, company):
#     #global uploaded_logo_path, selected_company, logos
#     #print("UPLOAD PATH ------", uploaded_logo_path)
#     #print("logos--------",logos)
    

#     jobBoard = job_boards[company]
#     #logo=logos[company]
#     #print(logo)
#     #print(len(jobBoard))
#     return templates.TemplateResponse(request=request, name="job-board.html",  context = {"jobs": jobBoard, "company":company}) 

