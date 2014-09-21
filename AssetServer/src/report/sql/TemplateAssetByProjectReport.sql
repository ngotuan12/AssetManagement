SELECT a.id, a.stock_id, a.asset_id,(select code from asset where id=a.asset_id) asset_code, a.serial, a.original_value,
       a.remain_value, a.import_date, to_char(a.use_date,'mm') use_month, to_char(a.use_date,'yyyy') use_year, a.change_date,
       a.state_id, a.goal_id, a.country_id, a.supplier_id, a.capital_id,
       a.amortize_id, nvl(a.project_id,1) project_id,'Test' project_name, a.reason_id, a.unit, a.product_date,
       a.power, a.interval, a.source, a.decision_no, decode(a.document_status,'1','Có','Không') document_status,
       a.num_sub, a.parent_serial, a.name, a.note, decode(a.status,'1','X','') status,
       a.decision_date, a.quantity, a.model, a.seri,null amortized_date,null department,null decide_num,null decide_year,
       null account,'Test TT Viễn thông' place,'Test dept' department
  FROM stock_asset_serial a