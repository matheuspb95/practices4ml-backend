from datetime import datetime
from pydantic import BaseModel
from typing import List
from .enums import (Work, Degree, Areas, OrganizationType, DevelopmentProcess,
                    DataSource, Challenges, Context, ContributionType, SWEBOK)
from bson import ObjectId
from typing import Optional


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class CreateUserModel(BaseModel):
    email: str
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UpdateUserModel(BaseModel):
    email: str
    name: str
    work: List[Work]
    organization: str
    occupation: str
    degree: Degree
    areas: List[Areas]
    photo: str  # BASE64


class File(BaseModel):
    filename: str
    filedata: str


class Author(BaseModel):
    author_name: str
    user_id: Optional[PyObjectId]
    editor: bool


class ListPractices(BaseModel):
    create_date: datetime
    name: str
    description: str
    organization_type: OrganizationType
    development_process: DevelopmentProcess
    context: Context
    data_source: DataSource
    contribution_type: ContributionType
    authors: List[Author]
    challenges: List[Challenges]
    swebok: List[SWEBOK]
    files: List[File]
    reference: str
    link: str
    doi: str


class CreateComment(BaseModel):
    comment: str



class CreatePractices(BaseModel):
    create_date: Optional[datetime]
    name: str
    description: str
    organization_type: OrganizationType
    development_process: DevelopmentProcess
    context: Context
    data_source: DataSource
    contribution_type: ContributionType
    authors: List[Author]
    challenges: List[Challenges]
    swebok: List[SWEBOK]
    files: List[File]
    reference: str
    link: str
    doi: str


class UpdatePractices(BaseModel):
    name: Optional[str]
    description: Optional[str]
    organization_type: Optional[OrganizationType]
    development_process: Optional[DevelopmentProcess]
    context: Optional[Context]
    data_source: Optional[DataSource]
    contribution_type: Optional[ContributionType]
    authors: Optional[List[Author]]
    challenges: Optional[List[Challenges]]
    swebok: Optional[List[SWEBOK]]
    files: Optional[List[File]]
    reference: Optional[str]
    link: Optional[str]
    doi: Optional[str]
