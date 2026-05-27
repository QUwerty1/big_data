SELECT SUM(su.Amount * su.Price) AS TotalRevenue
FROM dbo.Sales s
JOIN dbo.SaleSaleUnit ssu ON s.Id = ssu.SalesId
JOIN dbo.SaleUnits su ON ssu.SaleUnitsId = su.Id;