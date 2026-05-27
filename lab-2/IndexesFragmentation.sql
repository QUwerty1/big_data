SELECT 
    SCHEMA_NAME(t.schema_id) + '.' + t.name AS TableName,
    ips.avg_fragmentation_in_percent AS FragmentationPct,
    ips.fragment_count AS FragmentCount,
    i.type_desc AS IndexType
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes i 
    ON ips.object_id = i.object_id AND ips.index_id = i.index_id
JOIN sys.tables t 
    ON i.object_id = t.object_id
WHERE ips.index_id > 0
ORDER BY ips.avg_fragmentation_in_percent DESC;