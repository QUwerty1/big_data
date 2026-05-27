SELECT 
    DB_NAME() AS DatabaseName,
    SCHEMA_NAME(t.schema_id) + '.' + t.name AS TableName,
    i.name AS IndexName,
    MAX(ips.index_depth) AS TreeDepth,
    SUM(CASE WHEN ips.index_level = 0 THEN ips.page_count ELSE 0 END) AS LeafLevelPages,
    SUM(CASE WHEN ips.index_level > 0 THEN ips.page_count ELSE 0 END) AS NonLeafPages,
    SUM(ips.page_count) AS TotalPages,
    CAST(SUM(ips.page_count) * 8.0 / 1024 AS DECIMAL(10,2)) AS IndexSizeMB
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') ips
JOIN sys.indexes i 
    ON ips.object_id = i.object_id AND ips.index_id = i.index_id
JOIN sys.tables t 
    ON i.object_id = t.object_id
WHERE ips.index_id > 0 -- Исключаем кучи (HEAP)
GROUP BY t.schema_id, t.name, i.name
ORDER BY IndexSizeMB DESC;