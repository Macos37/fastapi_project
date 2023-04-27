import os
from typing import List, Union
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.auth.oauth import current_user
from database import get_async_session
from app.projects.models import Project
from app.projects.schema import (
    ProjectsCreate, ProjectsUpdate,
    ImageCreate, ProjectRead, ImageRead)
import aiofiles
from app.auth.models import User
from app.projects.models import Image
from logs.logger import Logger

logger = Logger(__name__)

router = APIRouter(
    prefix="/users/me",
    tags=["projects"],
)


@router.post("/projects/", response_model=ProjectsCreate)
async def create_project(
    project: ProjectsCreate, 
    db: Session = Depends(get_async_session), 
    current_user: User = Depends(current_user),
):
    new_project = Project(
        title=project.title,
        description=project.description,
        user_id=current_user.id,
        )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    logger.logger.info(f"New project '{new_project.title}'\
        created with user_id {current_user.id}")
    return new_project


@router.get("/projects/", response_model=List[ProjectRead])
async def get_all_project(
        db: Session = Depends(get_async_session),
        current_user: User = Depends(current_user),
) -> List[ProjectRead]:
    query = selectinload(Project.image)
    project = await db.execute(select(Project).where(
        Project.user_id == current_user.id).options(query))
    return project.scalars().all()


@router.get("/projects/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int, 
    db: Session = Depends(get_async_session), 
    current_user: User = Depends(current_user),
):
    query = selectinload(Project.image)
    project = await db.execute(select(Project).where(
        Project.id == project_id, Project.user_id == current_user.id
        ).options(query))
    return project.scalars().first()


@router.put("/projects/{project_id}")
async def put_project(
    project_id: int,
    project_update: ProjectsUpdate,
    db: Session = Depends(get_async_session), 
    current_user: User = Depends(current_user),
) -> Union[dict, ProjectsUpdate]:
    project = await db.execute(select(Project).where(
        Project.id == project_id, Project.user_id == current_user.id))
    project = project.scalars().first()
    if project is None:
        raise HTTPException(
            status_code=404, detail="Project not found or permission denied")
    project.title = project_update.title
    project.description = project_update.description
    await db.commit()
    await db.refresh(project)
    logger.logger.info(f"User ID {current_user.id} update project \
        {project_id}")
    return {'message': f"Project {project_id} was update",
            'project_update': project}


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int, 
    db: Session = Depends(get_async_session), 
    current_user: User = Depends(current_user),
) -> dict:
    project = await db.execute(select(Project).where(
        Project.id == project_id, Project.user_id == current_user.id))
    project = project.scalars().first()
    if project is None:
        raise HTTPException(
            status_code=404, detail="Project not found or permission denied")
    await db.delete(project)
    await db.commit()
    logger.logger.info(f"User ID {current_user.id} \
    delete project {project_id}")
    return {'message': f"Project {project_id} deleted"}


@router.post("/projects/{project_id}/image", response_model=ImageCreate)
async def add_image_for_project(
    project_id: int, 
    image: UploadFile = File(...),
    db: Session = Depends(get_async_session), 
    current_user: User = Depends(current_user),
):
    project = await db.execute(select(Project).where(
        Project.id == project_id, Project.user_id == current_user.id))
    project = project.scalars().first()
    
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    path_img = '/static/media/'
    user_folder_path = f"{os.getcwd()}{path_img}"
    os.makedirs(user_folder_path, exist_ok=True)
    
    new_image = Image(
        url=path_img + image.filename,
        project_id=project_id,
    )
    async with aiofiles.open(user_folder_path + image.filename, "wb")as buffer:
        buffer.write(await image.read())
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)
    
    logger.logger.info(f"User ID {current_user.id} \
add image {new_image.url} for project {project_id}")
    
    return new_image

@router.get("/projects/{project_id}/static/media/", response_model=ImageRead)
async def get_image_for_project(
    project_id: int, 
    db: Session = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    project = await db.execute(select(Image).where(Image.project_id == project_id))
    logger.logger.info(
        f"User ID {current_user.id} GET image project ID {project_id}")
    if project is None:
        raise HTTPException(
            status_code=404, detail="Project not found or permission denied")
    return project.scalars().first()


@router.delete("/projects/{project_id}/static/media/", response_model=None)
async def delete_image_for_project(
    project_id: int, 
    db: Session = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> dict:
    project = await db.execute(select(Image).where(Image.project_id == project_id))
    project = project.scalars().first()
    if project is None:
        raise HTTPException(
            status_code=404, detail="Project not found or permission denied")
    os.remove(f"{os.getcwd()}{project.url}")
    await db.delete(project)
    await db.commit()
    logger.logger.info(
        f"User ID {current_user.id} image project ID {project_id} deleted")
    return {'message': f"Image project ID {project_id} deleted"}