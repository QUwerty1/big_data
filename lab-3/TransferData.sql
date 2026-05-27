USE [StorageDWH];
GO

SET NOCOUNT ON;
SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRAN;

    DECLARE @StartDate DATE = '1900-01-01', @EndDate DATE = '2100-12-31';

    ;WITH N AS (
        SELECT TOP (DATEDIFF(DAY, @StartDate, @EndDate) + 1)
            n = ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1
        FROM sys.all_columns a CROSS JOIN sys.all_columns b
    )
    INSERT INTO [dbo].[DimDate] (DateKey, FullDate, Year, Month, Day, Quarter, MonthName, DayOfWeek, IsWeekday)
    SELECT 
        CONVERT(INT, CONVERT(VARCHAR(8), DATEADD(DAY, n, @StartDate), 112)),
        DATEADD(DAY, n, @StartDate),
        YEAR(DATEADD(DAY, n, @StartDate)),
        MONTH(DATEADD(DAY, n, @StartDate)),
        DAY(DATEADD(DAY, n, @StartDate)),
        DATEPART(QUARTER, DATEADD(DAY, n, @StartDate)),
        DATENAME(MONTH, DATEADD(DAY, n, @StartDate)),
        DATENAME(WEEKDAY, DATEADD(DAY, n, @StartDate)),
        CASE WHEN DATEPART(WEEKDAY, DATEADD(DAY, n, @StartDate)) BETWEEN 2 AND 6 THEN 1 ELSE 0 END
    FROM N;

    INSERT INTO [dbo].[DimProduct] (ProductId, ProductName, Price, ValidFrom, ValidTo, IsCurrent)
    SELECT 
        Id, ProductName, Price, 
        '1900-01-01', '9999-12-31', 1
    FROM [Storage].[dbo].[Products];

    INSERT INTO [dbo].[DimCustomer] (CustomerId, CompanyName, Phone, Address, Email, UserName, NormalizedEmail, IsStaff, IsGenerated, ValidFrom, ValidTo, IsCurrent)
    SELECT 
        c.Id, c.CompanyName, c.Phone, c.Address, c.Email,
        u.UserName, u.NormalizedEmail, u.IsStaff, u.IsGenerated,
        '1900-01-01', '9999-12-31', 1
    FROM [Storage].[dbo].[Customers] c
    LEFT JOIN [Storage].[dbo].[Users] u ON c.AppUserId = u.Id;

    INSERT INTO [dbo].[DimSupplier] (SupplierId, CompanyName, Phone, Address, Email, UserName, NormalizedEmail, IsStaff, IsGenerated, ValidFrom, ValidTo, IsCurrent)
    SELECT 
        s.Id, s.CompanyName, s.Phone, s.Address, s.Email,
        u.UserName, u.NormalizedEmail, u.IsStaff, u.IsGenerated,
        '1900-01-01', '9999-12-31', 1
    FROM [Storage].[dbo].[Suppliers] s
    LEFT JOIN [Storage].[dbo].[Users] u ON s.AppUserId = u.Id;

    INSERT INTO [dbo].[FactSales] (SalesOrderId, CustomerKey, ProductKey, OrderDateKey, PlannedDateKey, Quantity, UnitPrice, TotalAmount)
    SELECT 
        s.Id,
        dc.CustomerKey,
        dp.ProductKey,
        dReal.DateKey,
        dPlanned.DateKey,
        su.Amount,
        su.Price,
        CAST(su.Amount * su.Price AS MONEY)
    FROM [Storage].[dbo].[Sales] s
    JOIN [Storage].[dbo].[SaleSaleUnit] ssu ON s.Id = ssu.SalesId
    JOIN [Storage].[dbo].[SaleUnits] su ON ssu.SaleUnitsId = su.Id
    JOIN [dbo].[DimCustomer] dc ON s.CustomerId = dc.CustomerId AND dc.IsCurrent = 1
    JOIN [dbo].[DimProduct] dp ON su.ProductId = dp.ProductId 
        AND dp.ValidFrom <= CAST(s.RealDate AS DATE) 
        AND dp.ValidTo > CAST(s.RealDate AS DATE)
    JOIN [dbo].[DimDate] dReal ON dReal.FullDate = CAST(s.RealDate AS DATE)
    JOIN [dbo].[DimDate] dPlanned ON dPlanned.FullDate = CAST(s.PlannedDate AS DATE)
    WHERE NOT EXISTS (
        SELECT 1 FROM [dbo].[FactSales] fs WHERE fs.SalesOrderId = s.Id AND fs.ProductKey = dp.ProductKey
    );

    INSERT INTO [dbo].[FactSupplies] (SupplyOrderId, SupplierKey, ProductKey, ArrivalDateKey, PlannedDateKey, Quantity, UnitPrice, TotalAmount)
    SELECT 
        s.Id,
        ds.SupplierKey,
        dp.ProductKey,
        dReal.DateKey,
        dPlanned.DateKey,
        su.Amount,
        su.Price,
        CAST(su.Amount * su.Price AS MONEY)
    FROM [Storage].[dbo].[Supplies] s
    JOIN [Storage].[dbo].[SupplySupplyUnit] ssu ON s.Id = ssu.SuppliesId
    JOIN [Storage].[dbo].[SupplyUnits] su ON ssu.SupplyUnitsId = su.Id
    JOIN [dbo].[DimSupplier] ds ON s.SupplierId = ds.SupplierId AND ds.IsCurrent = 1
    JOIN [dbo].[DimProduct] dp ON su.ProductId = dp.ProductId 
        AND dp.ValidFrom <= CAST(s.RealDate AS DATE) 
        AND dp.ValidTo > CAST(s.RealDate AS DATE)
    JOIN [dbo].[DimDate] dReal ON dReal.FullDate = CAST(s.RealDate AS DATE)
    JOIN [dbo].[DimDate] dPlanned ON dPlanned.FullDate = CAST(s.PlannedDate AS DATE)
    WHERE NOT EXISTS (
        SELECT 1 FROM [dbo].[FactSupplies] fs WHERE fs.SupplyOrderId = s.Id AND fs.ProductKey = dp.ProductKey
    );

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRAN;
    THROW;
END CATCH
GO