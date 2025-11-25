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
from typing import Annotated
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db import get_db_session
from file_storage import upload_file
#import psycopg
from config import settings
from models import JobBoard,JobPost
from pydantic import BaseModel, Field, field_validator

from supabase import create_client, Client

# Serve static folder

app= FastAPI()
# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# templates = Jinja2Templates(directory="templates")

##SEREVR SIDE ROUTING
#app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))
#app.mount("/app",StaticFiles(directory="vite-project/dist" , html=True),name="app")


##/Uploads
if not settings.PRODUCTION:
    app.mount("/uploads", StaticFiles(directory="uploads/company_logos"))


class User(BaseModel):
    username: str
    id: str
    


@app.get("/api/health")
async def health():
    try:
        
        with get_db_session() as session:
            session.execute(text("SELECT 1"))
            #print("All good!")
            return {"DB-Health":"ok"}
    except:
        return {"DB-Health":"down"}



# job_boards={"acme": [{"title":"Software Engineer","jobDescription":"Builds, tests, and maintains software systems to deliver reliable, scalable, and efficient applications."},
#             { "title":"HR Manager","jobDescription":"Leads recruitment, employee relations, and HR operations to build a productive, compliant, and engaged workforce."}],
#             "bcg":[{"title":"Technical Architect","jobDescription":"Designs and oversees high-level technical solutions, ensuring system scalability, performance, and alignment with business needs."},
#             { "title":"Junior Software Developer","jobDescription":"Assists in coding, testing, and debugging applications while learning best practices under senior developer guidance."}],
#             "atlas":[{"title":"Design Engineer", "jobDescription":"Develop UI/UX webpages"},
#             { "title":"Senior Software Developer","jobDescription":"Develop software in Java Springboot"}]
# }


@app.get("/api/job-boards")
async def company_job_board():
    with get_db_session() as session:
        jobBoards=session.query(JobBoard).all()
        jobPosts = session.query(JobPost).all()
        # print(jobBoards)
        # print(jobPosts)
        return jobBoards
############################################################    
# @app.get("/api/job-boards/{id}/job-posts")
# async def company_job_board(id):
#     with get_db_session() as session:
#         jobBoards=session.query(JobBoard).all()
#         val = int(id)+1
#         jobPosts = session.query(JobPost).filter(JobPost.job_board_id == val).first()
#         # print(jobBoards)
#         # print(jobPosts)
       
#         return jobPosts

# @app.get("/api/job-boards/{company_name}")
# async def company_job_board(company_name):
#     with get_db_session() as session:
#         jobBoards=session.query(JobBoard).filter(JobBoard.company_name == str(company_name)).first()
        
#         jobPosts = session.query(JobPost).filter(JobPost.job_board_id == jobBoards.id).first()
#         return jobPosts
##################################################################
##ALTERNATE WAY
# class JobPost(Base):
#   __tablename__ = 'job_posts'
#   id = Column(Integer, primary_key=True)
#   title = Column(String, nullable=False)
#   description = Column(String, nullable=False)
#   job_board_id = Column(Integer, ForeignKey("job_boards.id"),  nullable=False)
#   job_board = relationship("JobBoard")
 
 ##############################################################
 
@app.get("/api/job-boards/{job_board_id}/job-posts")
async def api_company_job_board(job_board_id):
  with get_db_session() as session:
     
     jobPosts = session.query(JobPost).filter(JobPost.job_board_id.__eq__(int(job_board_id))).all()
     print(jobPosts)
     return jobPosts
  
@app.get("/api/job-boards/{company_name}")
async def api_company_job_board(company_name):
  with get_db_session() as session:
     jobPosts = session.query(JobPost) \
        .join(JobPost.job_board) \
        .filter(JobBoard.company_name.__eq__(company_name)) \
        .all()
     return jobPosts
  


# @app.post("/api/job-boards")
# async def api_create_new_job_board(request:Request):
#     body = await request.body()
#     raw_text=body.decode()
#     print(request.headers.get('content-type'))
#     print(raw_text)
#     return{}

# @app.post("/api/job-boards")
# async def api_create_new_job_board(slug:Annotated[str,Form()]):
#     return {"slug":slug}


@app.post("/multiply")
async def multiply(x:Annotated[int,Form()],y:Annotated[int,Form()]):
    res=x*y
    return {"result":res}

@app.post("/result")
def register_user(data: User):
    
    result = {"name":data.username,"id":data.id}
    return {"message": result}

#### FORM BINDING WITH PYDANTIC

class JobBoardForm(BaseModel):
   company_name : str = Field (min_length=3,max_length=20)
   logo : UploadFile = File()
   
   ##TRANSFORMING DATA USING PYDANTIC
   @field_validator('company_name')
   @classmethod
   def to_lowercase(cls,v):
    print(v)
    return v.lower()



@app.post("/api/job-boards")
async def api_create_new_job_board(job_board_form:Annotated[JobBoardForm,Form()]):
    logo_contents = await job_board_form.logo.read()
    file_url = upload_file("company_logos",job_board_form.logo.filename,logo_contents,job_board_form.logo.content_type)
    # query = f"insert into job-boards(logo_url) values ({file_url})"
    


    with get_db_session() as session:
        
        new_post = JobBoard(
               company_name= job_board_form.company_name,  # assign relationship
                logo_url = file_url)

        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        
    return {"company_name":job_board_form.company_name, "file_url":file_url}

@app.put("/api/job-boards")
async def api_create_new_job_board(job_board_form:Annotated[JobBoardForm,Form()]):
    logo_contents = await job_board_form.logo.read()
    file_url = upload_file("company_logos",job_board_form.logo.filename,logo_contents,job_board_form.logo.content_type)
    
    with get_db_session() as session:
        
        l_url = session.query(JobBoard).filter(JobBoard.company_name == str(job_board_form.company_name)).first()
        l_url.logo_url = file_url

        session.commit()
                
    return {"company_name":job_board_form.company_name, "file_url":file_url}




  
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
########################################################### 
## RENDER USING JINJA TEMPLATE
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

