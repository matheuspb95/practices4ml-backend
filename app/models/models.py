from pydantic import BaseModel

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
    work: str # {ACADEMIC, INDUSTRY}
    organization: str
    occupation: str
    degree: str # {STUDENT, GRADUATE, SPECIALIST, MASTER, PHD, OTHER}
    areas: str  #OPTIONS: 
                # Software Engineering
                # Human computer interaction
                # Interaction design
                # Artificial intelligence
                # Machine learning
                # Neural networks
                # Deep Learning
                # Data mining
                # Data science
                # Big data
                # Computer vision
                # Software architecture
    photo: str #BASE64

