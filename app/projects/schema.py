from pydantic import BaseModel


class BaseImage(BaseModel):
    url: str
    
    class Config:
        orm_mode = True


class ImageCreate(BaseImage):
    pass


class ImageRead(BaseImage):
    pass


class BaseProject(BaseModel):
    title: str
    description: str
  
    class Config:
        orm_mode = True

 
class ProjectsCreate(BaseProject):
    pass


class ProjectsUpdate(BaseProject):
    pass


class ProjectsDelete(BaseProject):
    id: int


class ProjectRead(BaseProject):
    id: int
    user_id: int
    image: list[ImageRead] = []