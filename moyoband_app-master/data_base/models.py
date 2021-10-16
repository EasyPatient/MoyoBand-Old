from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker

######## Connecting to database ########



engine= create_engine("postgresql+psycopg2://ukeybyqq:p2HS4u8sycy-NBKfG6x_hq0lqI9YU1iB@balarama.db.elephantsql.com:5432/ukeybyqq")   #Here we have connection to postgresql (for ease of use is disable because sqllite is easier to start with)
engine = create_engine('sqlite:///moyo.db',echo = True)
# engine = create_engine("postgresql+psycopg2://postgres:Mateusz12@192.168.0.168/moyo")
# engine.connect()
Session = sessionmaker(bind=engine)
session=Session()
Base = declarative_base()

##### Creatinge Map of our Database #########

class Doctor(Base):
    __tablename__ ="doctor"

    id = Column('id',Integer,primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String,nullable=False)
    email = Column(String,nullable=True)
    phone = Column (String,nullable=True)
    tasks = Column (String,nullable=True)
    def __repr__(self):
        return f"('{self.name}','{self.lastname}','{self.email}','{self.phone}','{self.tasks}')"

class Nurse(Base):
    __tablename__="nurse"
    
    id = Column('id',Integer,primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String,nullable=False)
    email = Column(String,nullable=True)
    phone = Column (String,nullable=True)
    tasks = Column (String,nullable=True)
    def __repr__(self):
        return f"('{self.name}','{self.lastname}','{self.email}','{self.phone}','{self.tasks}')"

class Patient(Base):
    __tablename__="patient"
    
    id = Column('id',Integer,primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    sex = Column(String,nullable=False)
    phone = Column (String,nullable=True)
    nameOfRelative = Column (String,nullable=True)
    phoneToRelative = Column(String,nullable=True)
    description = Column(String,nullable=True)
    disease = Column(String,nullable=True)
    medicaments = Column(String,nullable=True)
    bands = relationship('Band',backref="patient",lazy=True)
    def __repr__(self):
        return f"('{self.name}','{self.lastname}','{self.age}','{self.phone}','{self.nameOfRelative}','{self.phoneToRelative}','{self.description}','{self.disease},'{self.medicaments}')"

class Band(Base):
    __tablename__="band"

    id = Column('id',Integer,primary_key=True)
    MAC = Column(String,nullable=False)
    room = Column(Integer,nullable=False)
    bed = Column (Integer,nullable=False)
    HeartRate = Column(String,nullable=True)
    Temperature = Column(String,nullable=True)
    Saturation = Column (String,nullable=True)
    patient_id = Column(Integer,ForeignKey('patient.id'),nullable=True)
    def __repr__(self):
        return f"('{self.MAC}','{self.room}','{self.bed}','{self.HeartRate}','{self.Temperature}','{self.Saturation}')"
    def __init__(self, MAC, room, bed, HeartRate, Temperature, Saturation, patient_id):
        self.MAC = MAC
        self.room = room
        self.bed = bed
        self.HeartRate = HeartRate
        self.Temperature = Temperature
        self.Saturation = Saturation
        self.patient_id = patient_id

    def save(self):
    # inject self into db session
        session.add(self)
        session.commit()
        return self

##### Creatinge our DataBase ########
if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)    
