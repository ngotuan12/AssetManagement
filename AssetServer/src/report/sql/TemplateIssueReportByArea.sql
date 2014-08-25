SELECT d.area_code,d.`name` area_name,a.area_code,
       a.code device_code,a.name device_name,DATE_FORMAT(b.issue_date,'%d/%m/%Y %H:%i:%s') issue_date,
       `c`.name,b.value,c.symbol,b.description
FROM device a,device_issue b,device_properties `c`,area d
WHERE b.device_id = a.id 
AND a.area_id = d.id
AND `b`.device_pro_id = `c`.id
<%p_device_id%>
<%p_area_id%>
<%p_from_date%>
<%p_to_date%>
ORDER BY a.area_id,device_id,b.issue_date desc;