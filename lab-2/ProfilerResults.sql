USE tempdb;
GO

IF OBJECT_ID('dbo.ProfilerResults', 'U') IS NOT NULL DROP TABLE dbo.ProfilerResults;
CREATE TABLE dbo.ProfilerResults
(
    ID INT IDENTITY PRIMARY KEY,
    EventClass NVARCHAR(100),
    TextData NVARCHAR(MAX),
    ApplicationName NVARCHAR(256),
    NTUserName NVARCHAR(256),
    LoginName NVARCHAR(256),
    ClientProcessID INT,
    SPID INT,
    StartTime DATETIME2,
    CPU INT,
    Reads BIGINT,
    Writes BIGINT,
    Duration BIGINT,
    DatabaseID INT,
    DatabaseName NVARCHAR(256),
    HostName NVARCHAR(256)
);