USE tempdb;
GO

WITH RankedQueries AS (
    SELECT
        Duration,
        CPU,
        Reads,
        Writes,
        SUBSTRING(TextData, 0, 40) + '...' AS TextData,
        ROW_NUMBER() OVER (
            PARTITION BY TextData
            ORDER BY Duration DESC
        ) AS rn
    FROM dbo.ProfilerResults
    WHERE TextData != N'' AND EventClass = N'sp_statement_completed'
)
SELECT TOP 6
    Duration,
    CPU,
    Reads,
    Writes,
    TextData
FROM RankedQueries
WHERE rn = 1
ORDER BY Duration DESC;