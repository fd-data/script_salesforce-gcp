SELECT 
    Id,
    ParentId,
    Field,
    OldValue,
    NewValue,
    CreatedById,
    CreatedDate
FROM 
    Autorizacao__History
WHERE 
    CreatedDate >= {data_filtro}T00:00:00.000-03:00 AND
    Field = 'Status__c'
ORDER BY 
    CreatedDate DESC
