CREATE UNIQUE NONCLUSTERED INDEX IX_Users_NormalizedUserName 
ON dbo.Users (NormalizedUserName);