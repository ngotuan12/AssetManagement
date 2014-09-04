SELECT 
(SELECT name FROM asset WHERE id=(SELECT parent_id FROM asset WHERE id=s.asset_id)) Nhom1,
(SELECT name FROM asset WHERE id=s.asset_id) chi_tieu,
(SELECT code FROM asset WHERE id=s.asset_id) ma_so,
(SELECT code FROM LIST WHERE id=s.capital_id) ma_nguon_von,
sum(s.original_value) nguyen_gia,sum(s.remain_value) con_lai
,sum(CASE WHEN (state_id= 314 OR state_id= 315) THEN s.original_value ELSE 0 END) nguyen_gia_dang_su_dung,
sum(CASE WHEN (state_id= 314 OR state_id= 315) THEN s.remain_value ELSE 0 END) con_lai_dang_su_dung,
sum(CASE WHEN state_id= 316 THEN s.original_value ELSE 0 END) nguyen_gia_chua_dung,
sum(CASE WHEN state_id= 316 THEN s.remain_value ELSE 0 END) con_lai_chua_dung,
sum(CASE WHEN state_id= 316 THEN s.original_value ELSE 0 END) nguyen_gia_khong_dung,
sum(CASE WHEN state_id= 316 THEN s.remain_value ELSE 0 END) con_lai_khong_dung,
sum(CASE WHEN state_id= 319 THEN s.original_value ELSE 0 END) nguyen_gia_khong_dung,
sum(CASE WHEN state_id= 319 THEN s.remain_value ELSE 0 END) con_lai_khong_dung
FROM stock_asset_serial s
GROUP BY s.asset_id,s.capital_id