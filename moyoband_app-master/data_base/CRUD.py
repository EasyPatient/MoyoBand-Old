from sqlalchemy import create_engine,update
from sqlalchemy.orm import relationship,sessionmaker
from data_base.models import Patient, Band, Doctor,Patient,Nurse

##### Connecting to DataBase #######

####### Ten engine w komentarzu sluzy sie do laczenia z zewnetrzna baza danych. Oogolnie mozecie sobie potestowac ale ma on ograniczenia ######
# engine= create_engine("postgresql+psycopg2://ukeybyqq:p2HS4u8sycy-NBKfG6x_hq0lqI9YU1iB@balarama.db.elephantsql.com:5432/ukeybyqq")
# engine = create_engine("postgresql+psycopg2://postgres:Mateusz12@192.168.0.168/moyo")
engine = create_engine('sqlite:///moyo.db',echo = True)
engine.connect()
Session = sessionmaker(bind=engine)
session=Session()




#### CRUD ELEMENTS (CreateReadUpdateDelete) #########


####### Nurse QUERIES ###########

def AddNurse(name,lastname,email,phone):
    if name==None or lastname==None:
        print("Brak poprawanych danych")
    else:
        all_nurses = session.query(Nurse).filter_by(name=name,lastname=lastname).first()
        if all_nurses is None:
            nurse = Nurse(name=name,lastname=lastname,email=email,phone=phone)
            session.add(nurse)
            session.commit()
            session.bind.dispose()
            print("Nowa pielęgniarka dodana")
        else:
            print("Taka pielęgniarka juz istnieje. Usun lub sprawdz dane")
            session.bind.dispose()


def DeleteNurse(name,lastname,email):
    nurse= session.query(Nurse).filter_by(name=name,lastname=lastname,email=email).first()
    if nurse == None:
        print("Nie ma takiej pielęgniarki")
        session.bind.dispose()
    else:
        session.delete(nurse)
        session.commit()
        session.bind.dispose()
        print("Pomyślnie usunięto pielęgniarkę")

def UpdateNurse(name,lastname,email,phone,tasks):
    nurse = session.query(Nurse).filter_by(name=name,lastname=lastname,email=email).first()
    if nurse == None:
        print("Nie ma takiej pielęgniarki")
        session.bind.dispose()
    else:
        update.name = name
        update.lastname = lastname
        update.email = email
        update.phone = phone
        update.tasks = tasks
        session.commit()
        session.bind.dispose()
        print="Dane zaktualizowane"





#####Doctor QUERIES #######
def AddDoctor(name,lastname,email,phone):
    if name==None or lastname==None:
        print("Brak poprawanych danych")
    else:
        all_doctors = session.query(Doctor).filter_by(name=name,lastname=lastname).first()
        if all_doctors is None:
            doctor = Doctor(name=name,lastname=lastname,email=email,phone=phone)
            session.add(doctor)
            session.commit()
            session.bind.dispose()
            print("Nowy lekarz dodany")
        else:
            print("Taki lekarz juz istnieje. Usun lub sprawdz dane")
            session.bind.dispose()


def DeleteDoctor(name,lastname,email):
    doctor= session.query(Doctor).filter_by(name=name,lastname=lastname,email=email).first()
    if doctor == None:
        print("Nie ma takiego lekarza")
        session.bind.dispose()
    else:
        session.delete(doctor)
        session.commit()
        session.bind.dispose()
        print("Pomyślnie usunięto lekarza")

def UpdateDoctor(name,lastname,email,phone,tasks):
    doctor = session.query(Doctor).filter_by(name=name,lastname=lastname,email=email).first()
    if doctor == None:
        session.bind.dispose()
        print("Nie ma takiego lekarza")
    else:
        update.name = name
        update.lastname = lastname
        update.email = email
        update.phone = phone
        update.tasks = tasks
        session.commit()
        session.bind.dispose()
        print="Dane zaktualizowane"






######### Patient Queries ######
def AddPatient(name,lastname,age,sex,phone="",nameOfRelative="",phoneToRelative="",description="",disease="",medicaments=""):
    if name==None or lastname==None or age==None or sex==None:
        print("Brak poprawnych danych wpisz ponownie")
    else:
        patient_look = session.query(Patient).filter_by(name=name,lastname=lastname).first()
        if patient_look is None:
            patient = Patient(name=name,lastname=lastname,age=age,sex=sex,phone=phone,nameOfRelative=nameOfRelative,phoneToRelative=phoneToRelative,description=description,disease=disease,medicaments=medicaments)
            session.add(patient)
            session.commit()
            session.bind.dispose()
            print("Pacjent dodany pomyślnie")
        else:
            print("Taki pacjent juz istnieje. Usun aby dodac na nowo")    
            session.bind.dispose()


def DeletePatient(name,lastname):
    patient = session.query(Patient).filter_by(name=name,lastname=lastname).first()
    if patient is None:
        print("Nie ma takiego uzytkownika")
        session.bind.dispose()
    else:
        session.delete(patient)
        session.commit()
        session.bind.dispose()



def ShowPatient():
    pacjenci = session.query(Patient).all()
    print(pacjenci)
    session.bind.dispose()

##### Bands #####

def AddBand (lastname,MAC,room,bed,HeartRate="",Temperature="",Saturation=""):
    patient = session.query(Patient).filter_by(lastname=lastname)
    if lastname == None or MAC == None or patient== None:
        print("Brak poprawnych danych wpisz ponownie")
        session.bind.dispose()
    else:
        patient_id = session.query(Patient.id).filter_by(lastname=lastname).scalar()
        band = Band(MAC=MAC, room=room, bed=bed, HeartRate=HeartRate, Temperature=Temperature, Saturation=Saturation, patient_id=patient_id)
        band.save()
        print("Opaska została dodana")
        session.bind.dispose()
    
def ShowId(name):
    id_name = session.query(Patient.id).filter_by(name=name).scalar()
    print(id_name)
    session.bind.dispose()


def UpdateStats(MAC,HeartRate,Temperature,Saturation):
    band_update = session.query(Band).filter_by(MAC=MAC).first()
    if band_update is None:
        print("Nie ma takiej opaski")
        session.bind.dispose()
    else:
        band_update.HeartRate = HeartRate
        band_update.Temperature = Temperature
        band_update.Saturation = Saturation
        session.commit()
        session.bind.dispose()
        print = "Baza danych zaktualizowana"
        


def ShowBands():
    opaski = session.query(Band).all()
    print(opaski)
    session.bind.dispose()
def ShowDoctor():
    doctor = session.query(Doctor).all()
    print(doctor)
    session.bind.disposśe()
    
def BandMac():
    room = 2
    MAC = session.query(Band.MAC).filter_by(room=room).scalar()
    print(MAC)
    session.bind.dispose()