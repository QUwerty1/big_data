USE tempdb;
GO

WITH RankedQueries AS (
    SELECT
        Duration,
        CPU,
        Reads,
        Writes,
        TextData,
        ROW_NUMBER() OVER (
            PARTITION BY TextData
            ORDER BY Duration DESC
        ) AS rn
    FROM dbo.ProfilerResults
    WHERE TextData != N'' AND EventClass = N'sp_statement_completed'
)
SELECT
    Duration,
    CPU,
    Reads,
    Writes,
    TextData
FROM RankedQueries
WHERE rn = 1
ORDER BY Duration DESC;