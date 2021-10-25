from enum import Enum


class OrganizationType(str, Enum):
    large_company = 'Large company'
    small_company = 'Small Company/Startup'
    academic = 'Lab case/Academic'
    other = 'Other'
    unknown = 'Unknown'


class DevelopmentProcess(str, Enum):
    research_based = 'Research-based'
    ad_hoc = 'Ad-hoc'
    agile = 'Agile'
    iterative = 'Iterative'
    waterfall = 'Waterfall'
    mix = 'Mix'
    other = 'Other'
    unknown = 'Unknown'


class Context(str, Enum):
    in_house = 'In-house'
    outsource = 'Outsource'
    other = 'Other'
    unkwon = 'Unknown'


class DataSource(str, Enum):
    open_source = 'Open-Source'
    private = 'Private'
    experimental = 'Experimental'
    simulated_data = 'Simulated Data'
    other = 'Other'
    unknown = 'Unknown'


class ContributionType(str, Enum):
    theory = 'Theory'
    model = 'Model'
    framework = 'Framework/methods'
    guideline = 'Guideline'
    lesson_learning = 'Lesson Learning'
    advice = 'Advice/implications'
    tool = 'Tool'


class Challenges(str, Enum):
    testing = 'Testing'
    data_management = 'Data Management'
    model_development = 'Model Development'
    ai_software_quality = 'AI Software Quality'
    ai_engineering = 'AI Engineering'
    infrastructure = 'Infrastructure'
    requirement_engineering = 'Requirement Engineering'
    project_management = 'Project Management'
    architecture_design = 'Architecture Design'
    model_deployment = 'Model deployment'
    education = 'Education'
    integration = 'Integration'
    operation_support = 'Operation Support'


class SWEBOK(str, Enum):
    requirements = 'Requirements'
    design = 'Design'
    construction = 'Construction'
    testing = 'Testing'
    maintenance = 'Maintenance'
    configuration_management = 'Configuration Management'
    process = 'Process'
    models_methods = 'Models and Methods'
    software_quality = 'Software Quality'
    professional_practice = 'Professional Practice'


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
