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
from typing import Annotated, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db import get_db_session
from file_storage import upload_file
#import psycopg
from config import settings
from models import JobBoard,JobPost,JobApplication
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
    #app.mount("/uploads", StaticFiles(directory="uploads/resumes"))


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

@app.put("/api/job-boards/{job_board_id}")
async def update_job_board(job_board_id: int,
    company_name: Annotated[Optional[str], Form()] = None,
    logo: Annotated[Optional[UploadFile], File()] = None):
    
    
    with get_db_session() as session:
        job_board = session.query(JobBoard).filter(JobBoard.id == job_board_id).first()
        c_name = job_board.company_name

        if not job_board:
            raise HTTPException (status_code=404,detail="Job board not found")
        
        # Update company_name if provided
        if company_name:
            job_board.company_name = company_name.lower()
            c_name = company_name.lower()
        

        if logo:
            logo_contents = await logo.read()
            file_url = upload_file("company_logos",logo.filename,logo_contents,logo.content_type)
            job_board.logo_url = file_url
        else:
            file_url = job_board.logo_url 

        session.commit()
                
    return {"job_board_id": job_board_id,"company_name":c_name, "file_url":file_url }


@app.delete("/api/job-boards/{job_board_id}")
def delete_job_board(job_board_id: int):

    with get_db_session() as session:
        # 1. Find JobBoard
        job_board = session.get(JobBoard, job_board_id)

        if not job_board:
            raise HTTPException(status_code=404, detail="Job board not found")

         # 2. Fetch all job posts under this job board
        job_posts = session.query(JobPost).filter(
            JobPost.job_board_id == job_board_id
        ).all()

        # 3. Collect all job_post_ids
        job_post_ids = [jp.id for jp in job_posts]

        if job_post_ids:
            # 4. Delete job applications related to these job posts
            session.query(JobApplication).filter(
                JobApplication.job_post_id.in_(job_post_ids)
            ).delete(synchronize_session=False)

            # 5. Delete job posts under job board
            session.query(JobPost).filter(
                JobPost.id.in_(job_post_ids)
            ).delete(synchronize_session=False)

        # 6. Safe deletion
        session.delete(job_board)
        session.commit()

    return {"message": "Job board deleted successfully"}

users = {}  
class GetJobApplications(BaseModel):
    job_post_id : int
    first_name: str 
    last_name: str
    email: str
    resume : UploadFile = File()
    

@app.post("/api/job-applications")
async def api_create_new_job_application(job_application:Annotated[GetJobApplications,Form()] ):
    logo_contents = await job_application.resume.read()
    file_url = upload_file("company_logos",job_application.resume.filename,logo_contents,job_application.resume.content_type)
    
    with get_db_session() as session:

        get_status = session.query(JobPost.status).filter(JobPost.id == job_application.job_post_id).scalar()
        # print("STATUS-----",get_status)
        if str(get_status) == "Closed":
            raise HTTPException(status_code=404, detail="This job post is already closed")
        
        else:
            new_post = JobApplication(
                    job_post_id = job_application.job_post_id,
                    first_name= job_application.first_name,
                    last_name = job_application.last_name,
                    email=job_application.email,
                    resume_url = file_url,
                    
                    )

            session.add(new_post)
            session.commit()
            session.refresh(new_post)
        
    return {"status":"User added"}



@app.get("/api/job-applications")
async def get_job_application():
     with get_db_session() as session:
        get_job_applications = session.query(JobApplication).all()

        return get_job_applications

@app.put("/api/job-posts/{job_post_id}/close")
async def close_job_posts(job_post_id : int):
    with get_db_session() as session:
        get_status = session.query(JobPost).filter(JobPost.id == job_post_id).first()
        get_status.status = "Closed"
        session.commit()


    return{"details":f"{job_post_id} is Closed"}


  
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

