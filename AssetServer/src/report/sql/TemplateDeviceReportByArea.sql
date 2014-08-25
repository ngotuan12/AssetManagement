SELECT a.`name` area_name,d.id,d.code,d.area_code,d.address,d.short_address,
(CASE WHEN d.`status` = '1' THEN 'Tốt' 
WHEN d.`status` = '2' THEN 'Có sự cố' 
ELSE 'Mất kết nối' END) `status`
FROM device d,area a
WHERE d.area_code=a.area_code 
<%p_area_code%> 
<%p_status%> 
ORDER BY d.area_code