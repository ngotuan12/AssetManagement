SELECT rownum ROW_NO,d.code asset_code, a.serial, a.original_value,
       a.remain_value, a.import_date, to_char(a.use_date,'mm') use_month, to_char(a.use_date,'yyyy') use_year, a.change_date,
       a.state_id, a.goal_id, a.country_id, a.supplier_id, a.capital_id,
       nvl(a.project_id,-1) project_id,(select name from list where list_type='7' and id=a.project_id) project_name,a.unit, to_char(a.product_date,'yyyy') product_date,
       a.power,  (select name from ap_domain where type='SOURCE' and code=a.source) source, decode(a.document_status,'1','Có','Không') document_status,
       a.name, a.note, decode(a.status,'1','X','') status,
       a.quantity, a.model, a.seri,d.interval,a.decision_no,to_char(a.decision_date,'yyyy') decision_date,
       d.account_no,b.name place,c.dept_name
  FROM stock_asset_serial a,stock b,dept c,asset d
  where a.stock_id=b.stock_id
  and b.dept_id=c.id
  and a.asset_id=d.id
  and (<%p_project_id%> is null or a.project_id=<%p_project_id%>)