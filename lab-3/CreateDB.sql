CREATE TABLE [dbo].[DimDate] (
    [DateKey] INT PRIMARY KEY,
    [FullDate] DATE NOT NULL,
    [Year] INT NOT NULL,
    [Month] INT NOT NULL,
    [Day] INT NOT NULL,
    [Quarter] INT NOT NULL,
    [MonthName] NVARCHAR(20) NOT NULL,
    [DayOfWeek] NVARCHAR(20) NOT NULL,
    [IsWeekday] BIT NOT NULL
);

CREATE TABLE [dbo].[DimProduct] (
    [ProductKey] INT IDENTITY(1,1) PRIMARY KEY,
    [ProductId] INT NOT NULL,
    [ProductName] NVARCHAR(200) NOT NULL,
    [Price] MONEY NOT NULL,
    [ValidFrom] DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    [ValidTo] DATE NOT NULL DEFAULT '9999-12-31',
    [IsCurrent] BIT NOT NULL DEFAULT 1,
    CONSTRAINT UQ_DimProduct_SCD UNIQUE ([ProductId], [ValidFrom])
);
GO

CREATE TABLE [dbo].[DimCustomer] (
    [CustomerKey] INT IDENTITY(1,1) PRIMARY KEY,
    [CustomerId] INT NOT NULL,
    [CompanyName] NVARCHAR(60) NOT NULL,
    [Phone] NVARCHAR(20) NOT NULL,
    [Address] NVARCHAR(MAX) NOT NULL,
    [Email] NVARCHAR(60) NOT NULL,
    [UserName] NVARCHAR(450) NULL,
    [NormalizedEmail] NVARCHAR(256) NULL,
    [IsStaff] BIT NULL,
    [IsGenerated] BIT NULL,
    [ValidFrom] DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    [ValidTo] DATE NOT NULL DEFAULT '9999-12-31',
    [IsCurrent] BIT NOT NULL DEFAULT 1,
    CONSTRAINT UQ_DimCustomer_SCD UNIQUE ([CustomerId], [ValidFrom])
);
GO

CREATE TABLE [dbo].[DimSupplier] (
    [SupplierKey] INT IDENTITY(1,1) PRIMARY KEY,
    [SupplierId] INT NOT NULL,
    [CompanyName] NVARCHAR(60) NOT NULL,
    [Phone] NVARCHAR(20) NOT NULL,
    [Address] NVARCHAR(MAX) NOT NULL,
    [Email] NVARCHAR(60) NOT NULL,
    [UserName] NVARCHAR(450) NULL,
    [NormalizedEmail] NVARCHAR(256) NULL,
    [IsStaff] BIT NULL,
    [IsGenerated] BIT NULL,
    [ValidFrom] DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    [ValidTo] DATE NOT NULL DEFAULT '9999-12-31',
    [IsCurrent] BIT NOT NULL DEFAULT 1,
    CONSTRAINT UQ_DimSupplier_SCD UNIQUE ([SupplierId], [ValidFrom])
);

CREATE TABLE [dbo].[FactSales] (
    [FactSalesKey] BIGINT IDENTITY(1,1) PRIMARY KEY,
    [SalesOrderId] INT NOT NULL,               
    [CustomerKey] INT NOT NULL,
    [ProductKey] INT NOT NULL,
    [OrderDateKey] INT NOT NULL,               
    [PlannedDateKey] INT NOT NULL,             
    [Quantity] INT NOT NULL,
    [UnitPrice] MONEY NOT NULL,
    [TotalAmount] MONEY NOT NULL,
    CONSTRAINT FK_FactSales_Customer FOREIGN KEY ([CustomerKey]) REFERENCES [dbo].[DimCustomer]([CustomerKey]),
    CONSTRAINT FK_FactSales_Product FOREIGN KEY ([ProductKey]) REFERENCES [dbo].[DimProduct]([ProductKey]),
    CONSTRAINT FK_FactSales_OrderDate FOREIGN KEY ([OrderDateKey]) REFERENCES [dbo].[DimDate]([DateKey]),
    CONSTRAINT FK_FactSales_PlannedDate FOREIGN KEY ([PlannedDateKey]) REFERENCES [dbo].[DimDate]([DateKey])
);

CREATE TABLE [dbo].[FactSupplies] (
    [FactSuppliesKey] BIGINT IDENTITY(1,1) PRIMARY KEY,
    [SupplyOrderId] INT NOT NULL,              
    [SupplierKey] INT NOT NULL,
    [ProductKey] INT NOT NULL,
    [ArrivalDateKey] INT NOT NULL,             
    [PlannedDateKey] INT NOT NULL,
    [Quantity] INT NOT NULL,
    [UnitPrice] MONEY NOT NULL,
    [TotalAmount] MONEY NOT NULL,
    CONSTRAINT FK_FactSupplies_Supplier FOREIGN KEY ([SupplierKey]) REFERENCES [dbo].[DimSupplier]([SupplierKey]),
    CONSTRAINT FK_FactSupplies_Product FOREIGN KEY ([ProductKey]) REFERENCES [dbo].[DimProduct]([ProductKey]),
    CONSTRAINT FK_FactSupplies_ArrivalDate FOREIGN KEY ([ArrivalDateKey]) REFERENCES [dbo].[DimDate]([DateKey]),
    CONSTRAINT FK_FactSupplies_PlannedDate FOREIGN KEY ([PlannedDateKey]) REFERENCES [dbo].[DimDate]([DateKey])
);