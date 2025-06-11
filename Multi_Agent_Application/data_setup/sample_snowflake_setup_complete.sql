use role sysadmin;

create warehouse if not exists admin_wh_xsmall
  with
    warehouse_size = 'xsmall'
    warehouse_type = 'standard'
    auto_suspend = 60
    auto_resume = true
    min_cluster_count = 1
    max_cluster_count = 3
    scaling_policy = 'standard'
    initially_suspended = true;


use warehouse admin_wh_xsmall;

create database if not exists streamlit_apps;
use database streamlit_apps;

create schema if not exists llm_apps_sch with manged access;
use schema llm_apps_sch;

-- Snowflake P&C Insurance Database Setup Script
-- This script includes DDL for table creation and DML for sample data insertion.

-- -----------------------------------------------------
-- Data Definition Language (DDL)
-- -----------------------------------------------------

-- Users Table
CREATE OR REPLACE TABLE Users (
    UserID VARCHAR PRIMARY KEY,
    UserName VARCHAR,
    Role VARCHAR
);

-- Customers Table
CREATE OR REPLACE TABLE Customers (
    CustomerID VARCHAR PRIMARY KEY,
    CustomerType VARCHAR,
    FirstName VARCHAR,
    LastName VARCHAR,
    CompanyName VARCHAR,
    DateOfBirth DATE,
    AddressLine1 VARCHAR,
    AddressLine2 VARCHAR,
    City VARCHAR,
    State VARCHAR(2),
    ZipCode VARCHAR(10),
    PhoneNumber VARCHAR(20),
    EmailAddress VARCHAR,
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- Policies Table
CREATE OR REPLACE TABLE Policies (
    PolicyID VARCHAR PRIMARY KEY,
    CustomerID VARCHAR REFERENCES Customers(CustomerID),
    PolicyType VARCHAR,
    EffectiveDate DATE,
    ExpirationDate DATE,
    Status VARCHAR,
    TotalPremium DECIMAL(18,2),
    UnderwriterID VARCHAR REFERENCES Users(UserID),
    IssueDate DATE,
    CancellationDate DATE,
    CancellationReason VARCHAR,
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- PolicyCoverages Table
CREATE OR REPLACE TABLE PolicyCoverages (
    PolicyCoverageID VARCHAR PRIMARY KEY,
    PolicyID VARCHAR REFERENCES Policies(PolicyID),
    CoverageType VARCHAR,
    CoverageLimit DECIMAL(18,2),
    Deductible DECIMAL(18,2),
    PremiumForCoverage DECIMAL(18,2),
    EffectiveDate DATE,
    ExpirationDate DATE,
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- InsuredAssets Table
CREATE OR REPLACE TABLE InsuredAssets (
    InsuredAssetID VARCHAR PRIMARY KEY,
    PolicyID VARCHAR REFERENCES Policies(PolicyID),
    AssetType VARCHAR,
    Description VARCHAR,
    VIN VARCHAR(17),
    Make VARCHAR,
    Model VARCHAR,
    Year INTEGER,
    PropertyAddressLine1 VARCHAR,
    PropertyCity VARCHAR,
    PropertyState VARCHAR(2),
    PropertyZipCode VARCHAR(10),
    InsuredValue DECIMAL(18,2),
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- PolicyTransactions Table
CREATE OR REPLACE TABLE PolicyTransactions (
    PolicyTransactionID VARCHAR PRIMARY KEY,
    PolicyID VARCHAR REFERENCES Policies(PolicyID),
    TransactionType VARCHAR,
    TransactionDate DATE,
    EffectiveDate DATE,
    Description VARCHAR,
    PremiumChangeAmount DECIMAL(18,2),
    CreatedDate TIMESTAMP_NTZ
);

-- BillingSchedules Table
CREATE OR REPLACE TABLE BillingSchedules (
    BillingScheduleID VARCHAR PRIMARY KEY,
    PolicyID VARCHAR REFERENCES Policies(PolicyID),
    InstallmentNumber INTEGER,
    DueDate DATE,
    AmountDue DECIMAL(18,2),
    AmountPaid DECIMAL(18,2),
    PaymentDate DATE,
    Status VARCHAR,
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- Claims Table
CREATE OR REPLACE TABLE Claims (
    ClaimID VARCHAR PRIMARY KEY,
    PolicyID VARCHAR REFERENCES Policies(PolicyID),
    InsuredAssetID VARCHAR REFERENCES InsuredAssets(InsuredAssetID),
    DateOfLoss TIMESTAMP_NTZ,
    DateReported TIMESTAMP_NTZ,
    CauseOfLoss VARCHAR,
    LossDescription VARCHAR,
    Status VARCHAR,
    LocationOfLoss_Address VARCHAR,
    LocationOfLoss_City VARCHAR,
    LocationOfLoss_State VARCHAR(2),
    LocationOfLoss_ZipCode VARCHAR(10),
    AssignedAdjusterID VARCHAR REFERENCES Users(UserID),
    IsPotentiallyFraudulent BOOLEAN DEFAULT FALSE,
    FraudScore DECIMAL(5,2),
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- Claimants Table
CREATE OR REPLACE TABLE Claimants (
    ClaimantID VARCHAR PRIMARY KEY,
    ClaimID VARCHAR REFERENCES Claims(ClaimID),
    CustomerID VARCHAR REFERENCES Customers(CustomerID),
    ClaimantType VARCHAR,
    FirstName VARCHAR,
    LastName VARCHAR,
    CompanyName VARCHAR,
    AddressLine1 VARCHAR,
    City VARCHAR,
    State VARCHAR(2),
    ZipCode VARCHAR(10),
    PhoneNumber VARCHAR(20),
    EmailAddress VARCHAR,
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- ClaimCoverages Table
CREATE OR REPLACE TABLE ClaimCoverages (
    ClaimCoverageID VARCHAR PRIMARY KEY,
    ClaimID VARCHAR REFERENCES Claims(ClaimID),
    PolicyCoverageID VARCHAR REFERENCES PolicyCoverages(PolicyCoverageID),
    Status VARCHAR,
    CreatedDate TIMESTAMP_NTZ
);

-- ClaimReserves Table
CREATE OR REPLACE TABLE ClaimReserves (
    ClaimReserveID VARCHAR PRIMARY KEY,
    ClaimID VARCHAR REFERENCES Claims(ClaimID),
    PolicyCoverageID VARCHAR REFERENCES PolicyCoverages(PolicyCoverageID),
    ReserveType VARCHAR,
    InitialReserveAmount DECIMAL(18,2),
    CurrentReserveAmount DECIMAL(18,2),
    ReserveSetDate DATE,
    LastUpdatedDate TIMESTAMP_NTZ,
    CreatedDate TIMESTAMP_NTZ
);

-- ClaimPayments Table
CREATE OR REPLACE TABLE ClaimPayments (
    ClaimPaymentID VARCHAR PRIMARY KEY,
    ClaimID VARCHAR REFERENCES Claims(ClaimID),
    PolicyCoverageID VARCHAR REFERENCES PolicyCoverages(PolicyCoverageID),
    ClaimantID VARCHAR REFERENCES Claimants(ClaimantID),
    PaymentType VARCHAR,
    PaymentAmount DECIMAL(18,2),
    PaymentDate DATE,
    CheckNumber VARCHAR,
    PaymentMethod VARCHAR,
    Status VARCHAR,
    CreatedDate TIMESTAMP_NTZ
);

-- ClaimSubrogations Table
CREATE OR REPLACE TABLE ClaimSubrogations (
    SubrogationID VARCHAR PRIMARY KEY,
    ClaimID VARCHAR REFERENCES Claims(ClaimID),
    SubrogationTargetName VARCHAR,
    PotentialRecoveryAmount DECIMAL(18,2),
    AmountRecovered DECIMAL(18,2) DEFAULT 0.00,
    Status VARCHAR,
    RecoveryDate DATE,
    CreatedDate TIMESTAMP_NTZ,
    LastUpdatedDate TIMESTAMP_NTZ
);

-- ClaimNotes Table
CREATE OR REPLACE TABLE ClaimNotes (
    ClaimNoteID VARCHAR PRIMARY KEY,
    ClaimID VARCHAR REFERENCES Claims(ClaimID),
    NoteText VARCHAR,
    CreatedByUserID VARCHAR REFERENCES Users(UserID),
    CreatedDate TIMESTAMP_NTZ
);

-- -----------------------------------------------------
-- Data Manipulation Language (DML) - Sample Data
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Sample Data for Users Table
-- -----------------------------------------------------
INSERT INTO Users (UserID, UserName, Role) VALUES 
('U001', 'jsmith', 'Underwriter'),
('U002', 'mwilliams', 'ClaimsAdjuster'),
('U003', 'rjohnson', 'Manager'),
('U004', 'dlee', 'Underwriter'),
('U005', 'jbrown', 'ClaimsAdjuster');

-- -----------------------------------------------------
-- Sample Data for Customers Table
-- -----------------------------------------------------
INSERT INTO Customers (CustomerID, CustomerType, FirstName, LastName, CompanyName, DateOfBirth, AddressLine1, AddressLine2, City, State, ZipCode, PhoneNumber, EmailAddress, CreatedDate, LastUpdatedDate) VALUES 
('C001', 'Individual', 'John', 'Doe', NULL, '1980-05-15', '123 Main St', 'Apt 4B', 'New York', 'NY', '10001', '212-555-1234', 'john.doe@email.com', '2023-01-15 09:30:00', '2023-01-15 09:30:00'),
('C002', 'Individual', 'Jane', 'Smith', NULL, '1975-08-22', '456 Oak Ave', NULL, 'Los Angeles', 'CA', '90001', '310-555-5678', 'jane.smith@email.com', '2023-01-20 14:45:00', '2023-01-20 14:45:00'),
('C003', 'Corporate', NULL, NULL, 'ABC Corporation', NULL, '789 Business Pkwy', 'Suite 300', 'Chicago', 'IL', '60601', '312-555-9012', 'contact@abccorp.com', '2023-02-01 11:15:00', '2023-02-01 11:15:00'),
('C004', 'Individual', 'Robert', 'Johnson', NULL, '1990-03-10', '321 Pine St', NULL, 'Houston', 'TX', '77001', '713-555-3456', 'robert.johnson@email.com', '2023-02-10 16:20:00', '2023-02-10 16:20:00'),
('C005', 'Corporate', NULL, NULL, 'XYZ Industries', NULL, '654 Corporate Dr', 'Floor 5', 'Boston', 'MA', '02101', '617-555-7890', 'info@xyzindustries.com', '2023-02-15 10:00:00', '2023-02-15 10:00:00');

-- -----------------------------------------------------
-- Sample Data for Policies Table
-- -----------------------------------------------------
INSERT INTO Policies (PolicyID, CustomerID, PolicyType, EffectiveDate, ExpirationDate, Status, TotalPremium, UnderwriterID, IssueDate, CancellationDate, CancellationReason, CreatedDate, LastUpdatedDate) VALUES 
('P001', 'C001', 'Auto', '2023-02-01', '2024-02-01', 'Active', 1200.00, 'U001', '2023-01-25', NULL, NULL, '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('P002', 'C002', 'Homeowners', '2023-03-01', '2024-03-01', 'Active', 950.00, 'U004', '2023-02-20', NULL, NULL, '2023-02-20 10:30:00', '2023-02-20 10:30:00'),
('P003', 'C003', 'Commercial Property', '2023-02-15', '2024-02-15', 'Active', 5000.00, 'U001', '2023-02-10', NULL, NULL, '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('P004', 'C004', 'Auto', '2023-03-10', '2024-03-10', 'Active', 1500.00, 'U004', '2023-03-05', NULL, NULL, '2023-03-05 09:15:00', '2023-03-05 09:15:00'),
('P005', 'C005', 'Workers Compensation', '2023-01-01', '2024-01-01', 'Active', 7500.00, 'U001', '2022-12-15', NULL, NULL, '2022-12-15 14:00:00', '2022-12-15 14:00:00');

-- -----------------------------------------------------
-- Sample Data for PolicyCoverages Table
-- -----------------------------------------------------
INSERT INTO PolicyCoverages (PolicyCoverageID, PolicyID, CoverageType, CoverageLimit, Deductible, PremiumForCoverage, EffectiveDate, ExpirationDate, CreatedDate, LastUpdatedDate) VALUES 
('PC001', 'P001', 'Liability', 100000.00, 500.00, 600.00, '2023-02-01', '2024-02-01', '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('PC002', 'P001', 'Collision', 50000.00, 1000.00, 400.00, '2023-02-01', '2024-02-01', '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('PC003', 'P001', 'Comprehensive', 50000.00, 500.00, 200.00, '2023-02-01', '2024-02-01', '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('PC004', 'P002', 'Dwelling', 300000.00, 1000.00, 500.00, '2023-03-01', '2024-03-01', '2023-02-20 10:30:00', '2023-02-20 10:30:00'),
('PC005', 'P002', 'Personal Property', 150000.00, 500.00, 300.00, '2023-03-01', '2024-03-01', '2023-02-20 10:30:00', '2023-02-20 10:30:00'),
('PC006', 'P002', 'Liability', 100000.00, 0.00, 150.00, '2023-03-01', '2024-03-01', '2023-02-20 10:30:00', '2023-02-20 10:30:00'),
('PC007', 'P003', 'Building', 1000000.00, 5000.00, 3000.00, '2023-02-15', '2024-02-15', '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('PC008', 'P003', 'Business Personal Property', 500000.00, 2500.00, 1500.00, '2023-02-15', '2024-02-15', '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('PC009', 'P003', 'Business Interruption', 250000.00, 2500.00, 500.00, '2023-02-15', '2024-02-15', '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('PC010', 'P004', 'Liability', 100000.00, 500.00, 750.00, '2023-03-10', '2024-03-10', '2023-03-05 09:15:00', '2023-03-05 09:15:00'),
('PC011', 'P004', 'Collision', 75000.00, 1000.00, 500.00, '2023-03-10', '2024-03-10', '2023-03-05 09:15:00', '2023-03-05 09:15:00'),
('PC012', 'P004', 'Comprehensive', 75000.00, 500.00, 250.00, '2023-03-10', '2024-03-10', '2023-03-05 09:15:00', '2023-03-05 09:15:00'),
('PC013', 'P005', 'Employer Liability', 1000000.00, 10000.00, 4000.00, '2023-01-01', '2024-01-01', '2022-12-15 14:00:00', '2022-12-15 14:00:00'),
('PC014', 'P005', 'Medical Expenses', 500000.00, 0.00, 3500.00, '2023-01-01', '2024-01-01', '2022-12-15 14:00:00', '2022-12-15 14:00:00');

-- -----------------------------------------------------
-- Sample Data for InsuredAssets Table
-- -----------------------------------------------------
INSERT INTO InsuredAssets (InsuredAssetID, PolicyID, AssetType, Description, VIN, Make, Model, Year, PropertyAddressLine1, PropertyCity, PropertyState, PropertyZipCode, InsuredValue, CreatedDate, LastUpdatedDate) VALUES 
('IA001', 'P001', 'Vehicle', '2020 Toyota Camry', 'ABC123456DEF78901', 'Toyota', 'Camry', 2020, NULL, NULL, NULL, NULL, 25000.00, '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('IA002', 'P002', 'Property', 'Single Family Home', NULL, NULL, NULL, NULL, '456 Oak Ave', 'Los Angeles', 'CA', '90001', 350000.00, '2023-02-20 10:30:00', '2023-02-20 10:30:00'),
('IA003', 'P003', 'Property', 'Office Building', NULL, NULL, NULL, NULL, '789 Business Pkwy', 'Chicago', 'IL', '60601', 1200000.00, '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('IA004', 'P004', 'Vehicle', '2019 Honda Accord', 'XYZ987654ABC12345', 'Honda', 'Accord', 2019, NULL, NULL, NULL, NULL, 22000.00, '2023-03-05 09:15:00', '2023-03-05 09:15:00'),
('IA005', 'P005', 'Property', 'Manufacturing Facility', NULL, NULL, NULL, NULL, '654 Corporate Dr', 'Boston', 'MA', '02101', 2500000.00, '2022-12-15 14:00:00', '2022-12-15 14:00:00');

-- -----------------------------------------------------
-- Sample Data for PolicyTransactions Table
-- -----------------------------------------------------
INSERT INTO PolicyTransactions (PolicyTransactionID, PolicyID, TransactionType, TransactionDate, EffectiveDate, Description, PremiumChangeAmount, CreatedDate) VALUES 
('PT001', 'P001', 'New Business', '2023-01-25', '2023-02-01', 'Initial policy issuance', 1200.00, '2023-01-25 13:45:00'),
('PT002', 'P002', 'New Business', '2023-02-20', '2023-03-01', 'Initial policy issuance', 950.00, '2023-02-20 10:30:00'),
('PT003', 'P003', 'New Business', '2023-02-10', '2023-02-15', 'Initial policy issuance', 5000.00, '2023-02-10 15:20:00'),
('PT004', 'P004', 'New Business', '2023-03-05', '2023-03-10', 'Initial policy issuance', 1500.00, '2023-03-05 09:15:00'),
('PT005', 'P005', 'New Business', '2022-12-15', '2023-01-01', 'Initial policy issuance', 7500.00, '2022-12-15 14:00:00');

-- -----------------------------------------------------
-- Sample Data for BillingSchedules Table
-- -----------------------------------------------------
INSERT INTO BillingSchedules (BillingScheduleID, PolicyID, InstallmentNumber, DueDate, AmountDue, AmountPaid, PaymentDate, Status, CreatedDate, LastUpdatedDate) VALUES 
('BS001', 'P001', 1, '2023-02-01', 300.00, 300.00, '2023-01-28', 'Paid', '2023-01-25 13:45:00', '2023-01-28 10:15:00'),
('BS002', 'P001', 2, '2023-05-01', 300.00, 300.00, '2023-04-29', 'Paid', '2023-01-25 13:45:00', '2023-04-29 14:30:00'),
('BS003', 'P001', 3, '2023-08-01', 300.00, 0.00, NULL, 'Due', '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('BS004', 'P001', 4, '2023-11-01', 300.00, 0.00, NULL, 'Pending', '2023-01-25 13:45:00', '2023-01-25 13:45:00'),
('BS005', 'P002', 1, '2023-03-01', 950.00, 950.00, '2023-02-25', 'Paid', '2023-02-20 10:30:00', '2023-02-25 16:45:00'),
('BS006', 'P003', 1, '2023-02-15', 1250.00, 1250.00, '2023-02-14', 'Paid', '2023-02-10 15:20:00', '2023-02-14 11:30:00'),
('BS007', 'P003', 2, '2023-05-15', 1250.00, 1250.00, '2023-05-10', 'Paid', '2023-02-10 15:20:00', '2023-05-10 09:45:00'),
('BS008', 'P003', 3, '2023-08-15', 1250.00, 0.00, NULL, 'Due', '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('BS009', 'P003', 4, '2023-11-15', 1250.00, 0.00, NULL, 'Pending', '2023-02-10 15:20:00', '2023-02-10 15:20:00'),
('BS010', 'P004', 1, '2023-03-10', 1500.00, 1500.00, '2023-03-08', 'Paid', '2023-03-05 09:15:00', '2023-03-08 13:20:00'),
('BS011', 'P005', 1, '2023-01-01', 1875.00, 1875.00, '2022-12-28', 'Paid', '2022-12-15 14:00:00', '2022-12-28 10:30:00'),
('BS012', 'P005', 2, '2023-04-01', 1875.00, 1875.00, '2023-03-30', 'Paid', '2022-12-15 14:00:00', '2023-03-30 15:45:00'),
('BS013', 'P005', 3, '2023-07-01', 1875.00, 1875.00, '2023-06-29', 'Paid', '2022-12-15 14:00:00', '2023-06-29 11:15:00'),
('BS014', 'P005', 4, '2023-10-01', 1875.00, 0.00, NULL, 'Due', '2022-12-15 14:00:00', '2022-12-15 14:00:00');

-- -----------------------------------------------------
-- Sample Data for Claims Table
-- -----------------------------------------------------
INSERT INTO Claims (ClaimID, PolicyID, InsuredAssetID, DateOfLoss, DateReported, CauseOfLoss, LossDescription, Status, LocationOfLoss_Address, LocationOfLoss_City, LocationOfLoss_State, LocationOfLoss_ZipCode, AssignedAdjusterID, IsPotentiallyFraudulent, FraudScore, CreatedDate, LastUpdatedDate) VALUES 
('CL001', 'P001', 'IA001', '2023-03-15 08:30:00', '2023-03-15 10:45:00', 'Collision', 'Rear-ended at stoplight', 'Open', '100 Main St', 'New York', 'NY', '10001', 'U002', FALSE, 0.05, '2023-03-15 10:45:00', '2023-03-15 10:45:00'),
('CL002', 'P002', 'IA002', '2023-04-10 23:15:00', '2023-04-11 08:30:00', 'Water Damage', 'Pipe burst in upstairs bathroom', 'Open', '456 Oak Ave', 'Los Angeles', 'CA', '90001', 'U002', FALSE, 0.10, '2023-04-11 08:30:00', '2023-04-11 08:30:00'),
('CL003', 'P003', 'IA003', '2023-03-20 14:45:00', '2023-03-20 15:30:00', 'Fire', 'Small electrical fire in break room', 'Closed', '789 Business Pkwy', 'Chicago', 'IL', '60601', 'U005', FALSE, 0.08, '2023-03-20 15:30:00', '2023-04-15 11:20:00'),
('CL004', 'P004', 'IA004', '2023-05-05 17:20:00', '2023-05-05 18:45:00', 'Theft', 'Vehicle stolen from shopping mall parking lot', 'Open', '200 Shopping Center Rd', 'Houston', 'TX', '77001', 'U005', TRUE, 0.65, '2023-05-05 18:45:00', '2023-05-05 18:45:00'),
('CL005', 'P005', 'IA005', '2023-02-12 11:30:00', '2023-02-12 13:15:00', 'Employee Injury', 'Worker fell from ladder', 'Closed', '654 Corporate Dr', 'Boston', 'MA', '02101', 'U002', FALSE, 0.12, '2023-02-12 13:15:00', '2023-03-30 09:45:00');

-- -----------------------------------------------------
-- Sample Data for Claimants Table
-- -----------------------------------------------------
INSERT INTO Claimants (ClaimantID, ClaimID, CustomerID, ClaimantType, FirstName, LastName, CompanyName, AddressLine1, City, State, ZipCode, PhoneNumber, EmailAddress, CreatedDate, LastUpdatedDate) VALUES 
('CLM001', 'CL001', 'C001', 'Insured', 'John', 'Doe', NULL, '123 Main St', 'New York', 'NY', '10001', '212-555-1234', 'john.doe@email.com', '2023-03-15 10:45:00', '2023-03-15 10:45:00'),
('CLM002', 'CL002', 'C002', 'Insured', 'Jane', 'Smith', NULL, '456 Oak Ave', 'Los Angeles', 'CA', '90001', '310-555-5678', 'jane.smith@email.com', '2023-04-11 08:30:00', '2023-04-11 08:30:00'),
('CLM003', 'CL003', 'C003', 'Insured', NULL, NULL, 'ABC Corporation', '789 Business Pkwy', 'Chicago', 'IL', '60601', '312-555-9012', 'contact@abccorp.com', '2023-03-20 15:30:00', '2023-03-20 15:30:00'),
('CLM004', 'CL004', 'C004', 'Insured', 'Robert', 'Johnson', NULL, '321 Pine St', 'Houston', 'TX', '77001', '713-555-3456', 'robert.johnson@email.com', '2023-05-05 18:45:00', '2023-05-05 18:45:00'),
('CLM005', 'CL005', NULL, 'Third Party', 'Michael', 'Wilson', NULL, '111 Worker Lane', 'Boston', 'MA', '02101', '617-555-7777', 'michael.wilson@email.com', '2023-02-12 13:15:00', '2023-02-12 13:15:00');

-- -----------------------------------------------------
-- Sample Data for ClaimCoverages Table
-- -----------------------------------------------------
INSERT INTO ClaimCoverages (ClaimCoverageID, ClaimID, PolicyCoverageID, Status, CreatedDate) VALUES 
('CC001', 'CL001', 'PC002', 'Active', '2023-03-15 10:45:00'),
('CC002', 'CL002', 'PC004', 'Active', '2023-04-11 08:30:00'),
('CC003', 'CL002', 'PC005', 'Active', '2023-04-11 08:30:00'),
('CC004', 'CL003', 'PC007', 'Active', '2023-03-20 15:30:00'),
('CC005', 'CL004', 'PC012', 'Active', '2023-05-05 18:45:00');

-- -----------------------------------------------------
-- Sample Data for ClaimReserves Table
-- -----------------------------------------------------
INSERT INTO ClaimReserves (ClaimReserveID, ClaimID, PolicyCoverageID, ReserveType, InitialReserveAmount, CurrentReserveAmount, ReserveSetDate, LastUpdatedDate, CreatedDate) VALUES 
('CR001', 'CL001', 'PC002', 'Property Damage', 5000.00, 5000.00, '2023-03-16', '2023-03-16 09:30:00', '2023-03-16 09:30:00'),
('CR002', 'CL002', 'PC004', 'Property Damage', 10000.00, 12500.00, '2023-04-12', '2023-04-20 14:15:00', '2023-04-12 10:45:00'),
('CR003', 'CL002', 'PC005', 'Personal Property', 5000.00, 5000.00, '2023-04-12', '2023-04-12 10:45:00', '2023-04-12 10:45:00'),
('CR004', 'CL003', 'PC007', 'Property Damage', 15000.00, 12000.00, '2023-03-21', '2023-04-10 11:30:00', '2023-03-21 08:15:00'),
('CR005', 'CL004', 'PC012', 'Theft', 22000.00, 22000.00, '2023-05-06', '2023-05-06 10:20:00', '2023-05-06 10:20:00');

-- -----------------------------------------------------
-- Sample Data for ClaimPayments Table
-- -----------------------------------------------------
INSERT INTO ClaimPayments (ClaimPaymentID, ClaimID, PolicyCoverageID, ClaimantID, PaymentType, PaymentAmount, PaymentDate, CheckNumber, PaymentMethod, Status, CreatedDate) VALUES 
('CP001', 'CL001', 'PC002', 'CLM001', 'Repair', 2500.00, '2023-04-01', 'CHK12345', 'Check', 'Completed', '2023-04-01 15:30:00'),
('CP002', 'CL002', 'PC004', 'CLM002', 'Emergency Repair', 3000.00, '2023-04-15', 'CHK12346', 'Check', 'Completed', '2023-04-15 11:45:00'),
('CP003', 'CL003', 'PC007', 'CLM003', 'Repair', 12000.00, '2023-04-10', 'CHK12347', 'Check', 'Completed', '2023-04-10 14:20:00'),
('CP004', 'CL005', 'PC014', 'CLM005', 'Medical Expenses', 5000.00, '2023-03-01', 'CHK12348', 'Check', 'Completed', '2023-03-01 09:15:00'),
('CP005', 'CL005', 'PC014', 'CLM005', 'Lost Wages', 2500.00, '2023-03-15', 'CHK12349', 'Check', 'Completed', '2023-03-15 10:30:00');

-- -----------------------------------------------------
-- Sample Data for ClaimSubrogations Table
-- -----------------------------------------------------
INSERT INTO ClaimSubrogations (SubrogationID, ClaimID, SubrogationTargetName, PotentialRecoveryAmount, AmountRecovered, Status, RecoveryDate, CreatedDate, LastUpdatedDate) VALUES 
('CS001', 'CL001', 'Driver at Fault Insurance', 5000.00, 0.00, 'In Progress', NULL, '2023-03-20 14:30:00', '2023-03-20 14:30:00'),
('CS002', 'CL003', 'Electrical Contractor Inc', 8000.00, 8000.00, 'Recovered', '2023-04-25', '2023-03-25 10:15:00', '2023-04-25 16:45:00'),
('CS003', 'CL004', 'Unknown Third Party', 22000.00, 0.00, 'Pending Investigation', NULL, '2023-05-10 09:30:00', '2023-05-10 09:30:00'),
('CS004', 'CL005', 'Ladder Manufacturer', 7500.00, 0.00, 'In Progress', NULL, '2023-02-20 11:45:00', '2023-02-20 11:45:00'),
('CS005', 'CL002', 'Plumbing Company', 10000.00, 5000.00, 'Partial Recovery', '2023-05-01', '2023-04-15 13:20:00', '2023-05-01 15:30:00');

-- -----------------------------------------------------
-- Sample Data for ClaimNotes Table
-- -----------------------------------------------------
INSERT INTO ClaimNotes (ClaimNoteID, ClaimID, NoteText, CreatedByUserID, CreatedDate) VALUES 
('CN001', 'CL001', 'Initial claim report received. Vehicle has damage to rear bumper and trunk.', 'U002', '2023-03-15 10:45:00'),
('CN002', 'CL001', 'Contacted insured to schedule inspection.', 'U002', '2023-03-16 09:15:00'),
('CN003', 'CL001', 'Inspection completed. Estimate for repairs: $4,800.', 'U002', '2023-03-18 14:30:00'),
('CN004', 'CL002', 'Initial claim report received. Water damage to ceiling, walls, and flooring.', 'U002', '2023-04-11 08:30:00'),
('CN005', 'CL002', 'Emergency mitigation service dispatched.', 'U002', '2023-04-11 09:45:00'),
('CN006', 'CL003', 'Claim closed. All repairs completed and final payment issued.', 'U005', '2023-04-15 11:20:00'),
('CN007', 'CL004', 'Police report obtained. Vehicle entered into stolen vehicle database.', 'U005', '2023-05-06 10:15:00'),
('CN008', 'CL005', 'Claim closed. All medical expenses and lost wages paid.', 'U002', '2023-03-30 09:45:00'),
('CN009', 'CL005', 'Subrogation initiated against ladder manufacturer for potential product defect.', 'U002', '2023-02-20 11:45:00'),
('CN010', 'CL002', 'Received partial recovery from plumbing company responsible for faulty installation.', 'U002', '2023-05-01 15:30:00');




WITH __policies AS (\n  SELECT\n    createddate,\n    totalpremium\n  FROM streamlit_apps.llm_apps_sch.policies\n)\nSELECT\n  SUM(totalpremium) AS total_premium_amount,\n  MIN(createddate) AS start_date,\n  MAX(createddate) AS end_date\nFROM __policies\n -- Generated by Cortex Analyst\n;"