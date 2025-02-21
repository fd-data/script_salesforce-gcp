SELECT 
    IsDeleted, 
    LastModifiedDate, 
    LastModifiedById, 
    Status__c, 
    Id, 
    SystemModstamp, 
    Codigo_formula__c, 
    CreatedById, 
    Conta__c, 
    CreatedDate 

FROM 
    Autorizacao__c 

WHERE 
    LastModifiedDate >= {data_filtro}T00:00:00.000-03:00 AND
    Status__c <> 'Novo - Não tratado'

ORDER BY 
    LastModifiedDate DESC