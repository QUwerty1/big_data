USE Storage;
GO

SELECT [s1].[Id], [s1].[Address], [s1].[AppUserId], [s1].[CompanyName], [s1].[Email], [s1].[Phone], [s0].[Id], [s0].[PlannedDate], [s0].[RealDate], [s0].[SupplierId]
FROM (     SELECT [s].[Id], [s].[Address], [s].[AppUserId], [s].[CompanyName], [s].[Email], [s].[Phone]
    FROM [Suppliers] AS [s]
    ORDER BY [s].[Id]     OFFSET 0 ROWS ) AS [s1] LEFT JOIN [Supplies] AS [s0] ON [s1].[Id] = [s0].[SupplierId]
ORDER BY [s1].[Id]