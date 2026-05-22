SELECT TOP(1)
    [u].[Id], [u].[AccessFailedCount], [u].[ConcurrencyStamp], [u].[Email], [u].[EmailConfirmed], [u].[IsGenerated], [u].[IsStaff], [u].[LockoutEnabled], [u].[LockoutEnd], [u].[NormalizedEmail], [u].[NormalizedUserName], [u].[PasswordHash], [u].[PhoneNumber], [u].[PhoneNumberConfirmed], [u].[SecurityStamp], [u].[TwoFactorEnabled], [u].[UserName]
FROM [Users] AS [u]
WHERE [u].[NormalizedUserName] = 'ADMIN'