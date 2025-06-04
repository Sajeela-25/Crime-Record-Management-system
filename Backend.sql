-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS Arrested, Evidence, Criminal, Petitioner, Victim, Crime;

-- 1. Crime Table
CREATE TABLE Crime (
    CrimeID INT PRIMARY KEY, 
    Offence VARCHAR(25), 
    Description VARCHAR(25), 
    PenalCode INT
);

-- 2. Victim Table
CREATE TABLE Victim (
    vID INT PRIMARY KEY, 
    CNIC VARCHAR(15), 
    Fname VARCHAR(20), 
    Lname VARCHAR(20), 
    DOB DATE, 
    age INT
);

-- 3. Petitioner Table
CREATE TABLE Petitioner (
    pID INT PRIMARY KEY, 
    Fname VARCHAR(20), 
    Lname VARCHAR(20), 
    Relationship VARCHAR(10),
    CNIC VARCHAR(15),
    VictimID INT,
    CONSTRAINT FK_Petitioner_Victim 
        FOREIGN KEY (VictimID) 
        REFERENCES Victim(vID) 
        ON DELETE CASCADE  -- Automatically delete petitioners when victim is deleted
);

-- 4. Criminal Table
CREATE TABLE Criminal (
    CriminalID INT PRIMARY KEY, 
    CrimeID INT, 
    Name VARCHAR(25), 
    Address VARCHAR(25), 
    DOB DATE, 
    Age INT, 
    CNIC VARCHAR(15), 
    PrevCases INT, 
    Description VARCHAR(25),
    CONSTRAINT FK_Criminal_Crime 
        FOREIGN KEY (CrimeID) 
        REFERENCES Crime(CrimeID)
        ON DELETE CASCADE  -- Automatically delete criminals when crime is deleted
);

-- 5. Evidence Table
CREATE TABLE Evidence (
    eID INT PRIMARY KEY, 
    Location VARCHAR(25), 
    Item VARCHAR(10), 
    Description VARCHAR(25),
    CrimeID INT,
    CONSTRAINT FK_Evidence_Crime 
        FOREIGN KEY (CrimeID) 
        REFERENCES Crime(CrimeID)
        ON DELETE CASCADE  -- Automatically delete evidence when crime is deleted
);

-- 6. Arrested Table
CREATE TABLE Arrested (
    ArrestID INT PRIMARY KEY,
    CriminalID INT, 
    ArrestDate DATE,
    ArrestLocation VARCHAR(50),
    CONSTRAINT FK_Arrested_Criminal 
        FOREIGN KEY (CriminalID) 
        REFERENCES Criminal(CriminalID)
        ON DELETE CASCADE  -- Automatically delete arrests when criminal is deleted
);


-- Insert sample data into Crime
INSERT INTO Crime VALUES
(1,'Murder','Premeditated',302),
(2,'Rape','Forced',304),
(3,'Burglary','home alone',102),
(4,'Hit and run','Jaan Phuch ky',205),
(5,'Divorce','Unlawful',236),
(6,'LandMafia','Kabza',654),
(7,'Electricity Chori','Ziada chori',112),
(8,'Gas Chori','kafi ziada',154),
(9,'Bakri Chori','Eid',147),
(10,'Gattar Chori','Steal seller',149),
(11,'Car theft','Spare parts',502),
(12,'CyberCrime','Online',402),
(13,'Harassment','Chera Cheri',107),
(14,'Stalking','Picha karna',117),
(15,'Forced Marriage','family pressure',998),
(16,'Kidnapping','ransom',209),
(17,'Child Labour','forced work',120),
(18,'Child Marriage','underage',333),
(19,'Money Laundering','swiss account',666),
(20,'Gambling','cricket',999);

-- Insert sample data into Victim
INSERT INTO Victim VALUES
(1,'31203-0331111-1','Ali', 'Sheikh','1998-01-01',21),
(2,'31203-0331122-1','Ali','Shah','1998-01-02',17),
(3,'31203-0331133-1','usman','khan','1998-01-03',19),
(4,'31203-0331144-1','Ali','ahmed','1998-01-04',20),
(5,'31203-0331155-1','Ali','usman','1998-01-05',18),
(6,'31203-0331166-1','usman','ali','1998-01-06',19),
(7,'31203-0331177-1','usman','shah','1998-01-07',21),
(8,'31203-0331188-1','adil','khan','1998-01-08',20),
(9,'31203-0331199-1','adil','ali','1998-01-09',23),
(10,'31203-0330002-1','saqib','Jangli','1998-01-10',26),
(11,'31203-0330003-1','saqib','ali','1998-02-01',24),
(12,'31203-0330004-1','saqib','usman','1998-02-02',26),
(13,'31203-0330005-1','saqib','shah','1998-02-03',20),
(14,'31203-0330006-1','ALLAH','DITA','1998-02-04',32),
(15,'31203-0330007-1','qasim','shah','1998-02-05',21),
(16,'31203-0330008-1','zahid','CH','1998-02-06',20),
(17,'31203-0330009-1','iqbal','Thippa','1998-02-07',20),
(18,'31203-0333001-1','shahid','PAppu','1998-02-08',19),
(19,'31203-0333002-1','abdul','aziz','1998-02-09',18),
(20,'31203-0333003-1','Billa','Builder','1998-02-10',19);

-- Insert sample data into Petitioner with Victim relationships
INSERT INTO Petitioner VALUES
(1,'Ali', 'Sheikh','Cousin','31203-0331111-1',1),
(2,'Ali','Shah','Mamu','31203-0331122-1',2),
(3,'usman','khan','Chacha','31203-0331133-1',3),
(4,'Ali','ahmed','Taya','31203-0331144-1',4),
(5,'Ali','usman','Bhanja','31203-0331155-1',5),
(6,'usman','ali','Bhai','31203-0331166-1',6),
(7,'usman','shah','Bhen','31203-0331177-1',7),
(8,'adil','khan','Pet','31203-0331188-1',8),
(9,'adil','ali','Khalu','31203-0331199-1',9),
(10,'saqib','Jangli','Taya','31203-0330002-1',10),
(11,'saqib','ali','Abba','31203-0330003-1',11),
(12,'saqib','usman','Ama','31203-0330004-1',12),
(13,'saqib','shah','Chacha','31203-0330005-1',13),
(14,'ALLAH','DITA','Bhenoyi','31203-0330006-1',14),
(15,'qasim','shah','Sala','31203-0330007-1',15),
(16,'zahid','CH','Beta','31203-0330008-1',16),
(17,'iqbal','Thippa','Kabootar','31203-0330009-1',17),
(18,'shahid','PAppu','Mamu','31203-0333001-1',18),
(19,'abdul','aziz','Mami','31203-0333002-1',19),
(20,'Billa','Builder','Pappa','31203-0333003-1',20);

-- Insert sample data into Criminal
INSERT INTO Criminal VALUES
(1,1,'Ali Sheikh','Lahore','1998-01-01',21,'90008-0100170-1',0,'Black Mark on Back'),
(2,2,'Amir Bhatti','Lahore','1998-02-02',21,'12008-0100170-2',2,'Spot on face'),
(3,3,'Fazeel Noor','Lahore','1998-03-03',21,'34008-0100170-3',0,'Mark on Arm'),
(4,4,'Khokar Niazi','Lahore','1998-04-04',21,'56008-0100170-4',2,'One legged'),
(5,5,'Jameel Boxer','Lahore','1998-05-05',21,'78008-0100170-5',3,'4 fingers'),
(6,6,'Abid Boxer','Lahore','1998-06-06',21,'68008-0100170-6',1,'Kana'),
(7,7,'Chota Kali','Lahore','1998-07-07',21,'69008-0100170-7',7,'Red Hair'),
(8,8,'Bara Kali','Lahore','1998-08-08',21,'11008-0100170-8',9,'White Hair'),
(9,9,'Ramesh Khan','Lahore','1998-09-09',21,'23008-0100170-9',12,'Blonde'),
(10,10,'Jiju Komi','Lahore','1998-10-10',21,'44008-0100170-2',14,'Kala hy'),
(11,11,'Kamlesh Sindhu','Lahore','1998-11-11',21,'17008-0100170-1',1,'No eyebrows'),
(12,12,'Shamir Idres','Lahore','1998-12-12',21,'54008-0100170-3',21,'Scar on face'),
(13,13,'Akbar Toka','Lahore','1998-03-13',21,'37008-0100170-3',10,'Short height'),
(14,14,'Asfand Jangli','Lahore','1998-04-14',21,'88008-0100170-2',7,'very tall'),
(15,15,'Fika','Lahore','1998-05-15',21,'99008-0100170-5',0,'builder'),
(16,16,'Karate Kid','Lahore','1998-06-16',21,'17008-0100170-5',4,'sukha'),
(17,17,'Rock Pathar','Lahore','1998-07-17',21,'23008-0100170-5',9,'powderi'),
(18,18,'Kamli Badmaash','Lahore','1998-08-18',21,'34008-0100170-5',21,'very fast runner'),
(19,19,'Shani Gujjar','Lahore','1998-09-19',21,'50008-0100170-5',20,'single handed'),
(20,20,'Saddam Daler','Lahore','1998-10-20',21,'34008-0100170-5',0,'mark on leg');

-- Insert sample data into Evidence
INSERT INTO Evidence VALUES
(1,'Garage','Knife','Blood Stained',1),
(2,'Attic','Gun','empty magazine',2),
(3,'Roof','Bottle','broken',3),
(4,'Lawn','Knuckle','Blood Stained',4),
(5,'Store Room','Hockey','broken',5),
(6,'Jhuggi','Bat','Blood Stained',6),
(7,'Bathroom','Nailcutter','Blood Stained',7),
(8,'Master Room','Scissor','wengi',8),
(9,'Servant Room','Rope','found on fan',9),
(10,'Cellar','Shisha','coal was burning',10),
(11,'Drawing Room','Car','headlight broken',11),
(12,'Kids Room','Bike','jharri mei thi',12),
(13,'Backyard','Truck','drugs found inside',13),
(14,'Alley','Chain','gold',14),
(15,'Frontyard','Acid','empty',15),
(16,'Courtyard','thread','glass',16),
(17,'Lobby','hair','Blonde',17),
(18,'Office','mobile','broken',18),
(19,'Washroom','ipad','Blood Stained',19),
(20,'Daftar','wallet','Blood Stained',20);

-- Insert sample data into Arrested (simplified)
INSERT INTO Arrested VALUES
(1,1,'2023-01-15','Lahore Central'),
(2,2,'2023-02-20','Gulberg Station'),
(3,3,'2023-03-10','Model Town'),
(4,4,'2023-04-05','Cantt Police Station'),
(5,5,'2023-05-12','Iqbal Town'),
(6,6,'2023-06-18','Samnabad'),
(7,7,'2023-07-22','Shadman'),
(8,8,'2023-08-30','Johar Town'),
(9,9,'2023-09-14','Faisal Town'),
(10,10,'2023-10-05','DHA Phase 5'),
(11,11,'2023-11-11','Bahria Town'),
(12,12,'2023-12-25','Wapda Town'),
(13,13,'2024-01-03','Garden Town'),
(14,14,'2024-02-14','Liberty Market'),
(15,15,'2024-03-08','Muslim Town'),
(16,16,'2024-04-01','Township'),
(17,17,'2024-05-09','Gulshan Station'),
(18,18,'2024-06-12','Ravi Town'),
(19,19,'2024-07-07','Shahdara'),
(20,20,'2024-08-19','Wagah Border');

-- View all tables with sample queries
SELECT * FROM Crime;
SELECT * FROM Criminal;
SELECT * FROM Victim;
SELECT * FROM Petitioner;
SELECT * FROM Evidence;
SELECT * FROM Arrested;
