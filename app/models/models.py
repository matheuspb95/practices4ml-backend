from pydantic import BaseModel
from enum import Enum


class Work(str, Enum):
    ACADEMIC = 'academic'
    INDUSTRY = 'industry'


class Degree(str, Enum):
    STUDENT = 'student'
    GRADUATE = 'graduate'
    SPECIALIST = 'specialist'
    MASTER = 'master'
    PHD = 'phd'
    OTHER = 'other'


class Areas(str, Enum):
    SOFTWARE_ENGINEERING = 'software engineering'
    HUMAN_COMPUTER_INTERACTION = 'human computer interaction'
    INTERACTION_DESIGN = 'interaction design'
    ARTIFICIAL_INTELLIGENCE = 'artificial intelligence'
    MACHINE_LEARNING = 'machine learning'
    NEURAL_NETWORKS = 'neural networks'
    DEEP_LEARNING = 'deep learning'
    DATA_MINING = 'data mining'
    DATA_SCIENCE = 'data science'
    BIG_DATA = 'big data'
    COMPUTER_VISION = 'computer vision'
    SOFTWARE_ARCHITECTURE = 'software architecture'

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
    work: Work
    organization: str
    occupation: str
    degree: Degree
    areas: Areas
    photo: str #BASE64

