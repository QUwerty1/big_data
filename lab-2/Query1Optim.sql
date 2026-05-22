CREATE NONCLUSTERED INDEX IX_Supplies_SupplierId_Covering
ON dbo.Supplies (SupplierId)
INCLUDE (Id, PlannedDate, RealDate);