import pymysql
databaseConnection = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'moyo_band_sql'
}
class Data():
    def UserData(self,loginvariable,passwordvariable):
        self.sTextboxValue = loginvariable
        self.sTextboxValue2 = passwordvariable
        self.sd = False
        # Connecting section -> Connecting with database
        ConnectDB = pymysql.connect(user=databaseConnection['user'],password=databaseConnection['password'],host=databaseConnection['host'],database=databaseConnection['database'])
        # Creating cursor to executing query(ies)
        DataBaseOperate = ConnectDB.cursor()
        query = "SELECT id,login,haslo FROM userdata WHERE login='{0}' AND haslo='{1}'".format(self.sTextboxValue,self.sTextboxValue2)
        DataBaseOperate.execute(query)

        for (id, login, haslo) in DataBaseOperate:
            if (login == self.sTextboxValue and haslo == self.sTextboxValue2):
                self.sd = True

            ConnectDB.commit()
            ConnectDB.close()

    def PatientData(self,PatientID):
        self.iPatient = PatientID
        self.sPatientData = []
        # Connecting section -> Connecting with database
        ConnectDB = pymysql.connect(user=databaseConnection['user'], password=databaseConnection['password'],host=databaseConnection['host'], database=databaseConnection['database'])
        # Creating cursor to executing query(ies)
        DataBaseOperate = ConnectDB.cursor()
        query = "SELECT * FROM pacient WHERE id={0}".format(self.iPatient)
        DataBaseOperate.execute(query)
        self.QueryResult = DataBaseOperate.fetchall()
        for numbercolumn in range(6):
            self.sPatientData.append(self.QueryResult[0][numbercolumn])

        ConnectDB.commit()
        ConnectDB.close()
    def PatientData_Counter(self):
        self.SumPatient = 0
        # Connecting section -> Connecting with database
        ConnectDB = pymysql.connect(user=databaseConnection['user'], password=databaseConnection['password'],
                                    host=databaseConnection['host'], database=databaseConnection['database'])
        # Creating cursor to executing query(ies)
        DataBaseOperate = ConnectDB.cursor()
        query = "SELECT COUNT(id) FROM pacient"
        DataBaseOperate.execute(query)
        self.QueryResult = DataBaseOperate.fetchall()
        self.SumPatient = self.QueryResult[0][0]
        ConnectDB.commit()
        ConnectDB.close()
        
    def PatientAllInfo(self):
        self.sName = []
        # Connecting section -> Connecting with database
        ConnectDB = pymysql.connect(user=databaseConnection['user'], password=databaseConnection['password'],host=databaseConnection['host'], database=databaseConnection['database'])
        # Creating cursor to executing query(ies)
        DataBaseOperate = ConnectDB.cursor()
        query = "SELECT * FROM pacient"
        DataBaseOperate.execute(query)
        self.QueryResult = DataBaseOperate.fetchall()
        for numberrow in range(len(self.QueryResult)):
            self.sName.append(self.QueryResult[numberrow][1])

        ConnectDB.commit()
        ConnectDB.close()