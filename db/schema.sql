-- MySleep academic prototype: schema only, no patient records or credentials.
-- Extracted from the original local SQLite demo database.
-- Intended for local experimentation, not clinical deployment.

CREATE TABLE IF NOT EXISTS DataSummary (
    DeviceID INTEGER NOT NULL,
    SummaryDate DATE NOT NULL,
    HRMax FLOAT NOT NULL,
    HRMin FLOAT NOT NULL,
    HRRange FLOAT NOT NULL,
    BPMax FLOAT NOT NULL,
    BPMin FLOAT NOT NULL,
    BPRange FLOAT NOT NULL,
    PO2Max FLOAT NOT NULL,
    PO2Min FLOAT NOT NULL,
    PO2Range FLOAT NOT NULL,
    PO2Path TEXT,
    HRPath TEXT,
    BPPath TEXT, 
    FallAsleepTime TIME NOT NULL,
    WakingUpTime TIME NOT NULL,
    RemDuration INTEGER CHECK(RemDuration >= 0),
    SleepingTime INTEGER CHECK(SleepingTime >= 0),
    NumberOfRems INTEGER CHECK(NumberOfRems >= 0), PO2PlotPath TEXT, HRPlotPath TEXT, BPPlotPath TEXT, PatientID INTEGER,
    PRIMARY KEY (DeviceID, SummaryDate), 
    FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID)
);

CREATE TABLE IF NOT EXISTS Questionnaire (
    UserID INTEGER NOT NULL,     
    QuestionnaireDate DATE NOT NULL,
    SubjectiveQuality INTEGER CHECK(subjectiveQuality >= 0 AND SubjectiveQuality <= 3 ),
    SleepLatency INTEGER CHECK(SleepLatency>=0 AND SleepLatency<=3),
    SleepDuration INTEGER CHECK(SleepDuration>=0 AND SleepDuration<=3),
    SleepDisturbances INTEGER CHECK(SleepDisturbances>=0 AND SleepDisturbances<=3),
    Medications INTEGER CHECK(Medications=0 OR Medications=3),
    TroubleAwake INTEGER CHECK(TroubleAwake=0 OR TroubleAwake=3),
    DayNapDuration INTEGER CHECK(DayNapDuration>=0 AND DayNapDuration<=3),
    Screens30Mins INTEGER CHECK(Screens30Mins=0 OR Screens30Mins=3),
    SleepScore INTEGER CHECK(SleepScore>=0 AND SleepScore<=100),
    PRIMARY KEY (UserID, QuestionnaireDate), 
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE IF NOT EXISTS Tips (
        tipsID INTEGER PRIMARY KEY AUTOINCREMENT,
        tips VARCHAR(300)
    );

CREATE TABLE IF NOT EXISTS appointments (
          PatientID INTEGER,
          DoctorID INTEGER,
          DateTime DATETIME,
          Location VARCHAR(300),
          FOREIGN KEY (PatientID) REFERENCES patients (PatientID),
          FOREIGN KEY (DoctorID) REFERENCES doctors (DoctorID),
          PRIMARY KEY (PatientID, DoctorID, DateTime)
          );

CREATE TABLE IF NOT EXISTS device (
        PatientID INTEGER,
        DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,
        Bactery INTEGER CHECK (Bactery > 0),
        Correct_Positioning VARCHAR(3) CHECK (Correct_Positioning IN ('YES', 'NO')),
        Time DATETIME,
        Mode VARCHAR(6) CHECK (Mode IN ('Asleep', 'Awake')),
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID));

CREATE TABLE IF NOT EXISTS doctors (
          doctorID INTEGER PRIMARY KEY,
          openinghour TIME,
          closinghour TIME,
          FOREIGN KEY (DoctorID) REFERENCES user (UserID)
          
          );

CREATE TABLE IF NOT EXISTS notes (
          NotesID INTEGER PRIMARY KEY AUTOINCREMENT,
          PatientID INTEGER,
          DoctorID INTEGER,
          DateTime DATETIME,
          Note TEXT,
          FOREIGN KEY (PatientID) REFERENCES patients (PatientID),
          FOREIGN KEY (DoctorID) REFERENCES doctors (DoctorID)
          
          );

CREATE TABLE IF NOT EXISTS patient (
          UserID INTEGER PRIMARY KEY,
          Gender CHAR(1) CHECK (Gender IN ('F','M','O')),
          Height INTEGER,
          Weight INTEGER,
          Pathologies TEXT,
          Medications TEXT,
          DoctorID INTEGER,
          FOREIGN KEY (UserID) REFERENCES user(UserID)
          FOREIGN KEY (DoctorID) REFERENCES doctors(Doctor_ID)

          );

CREATE TABLE IF NOT EXISTS prescriptions (
          PrescriptionID INTEGER PRIMARY KEY AUTOINCREMENT, 
          PatientID INTEGER,
          DoctorID INTEGER,
          DateTime DATETIME,
          Status VARCHAR(10),
          Drug VARCHAR(20),
          Dosage VARCHAR(20),
          StartDate DATE,
          EndingDate DATE,
          Frequency VARCHAR(30),
          Warnings VARCHAR(100),
          FOREIGN KEY (PatientID) REFERENCES patients (PatientID),
          FOREIGN KEY (DoctorID) REFERENCES doctors (DoctorID)
          );

CREATE TABLE IF NOT EXISTS software_daily_report (
        UserID INTEGER NOT NULL,
        Report_Date DATE,
        Tips TEXT,
        SleepScore INTEGER CHECK (SleepScore >= 0 And SleepScore <= 100),
        FOREIGN KEY (UserID) REFERENCES User (UserID),
        PRIMARY KEY (UserID, Report_Date)
    );

CREATE TABLE IF NOT EXISTS user (
          UserID INTEGER PRIMARY KEY AUTOINCREMENT,  
          Role CHAR(1) CHECK (Role IN ('P','D')),
          Password VARCHAR(30) NOT NULL,
          Name VARCHAR(30) NOT NULL,
          Surname VARCHAR(30) NOT NULL,
          Email VARCHAR(30) UNIQUE NOT NULL,
          PhoneNumber VARCHAR(20) UNIQUE NOT NULL,    
          SocialSecurityNumber VARCHAR(30) UNIQUE NOT NULL,
          Address VARCHAR(30) NOT NULL,
          BirthPlace VARCHAR(30) NOT NULL,
          BirthDate DATE NOT NULL
         );
