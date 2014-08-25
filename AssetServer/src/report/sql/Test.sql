SELECT username area_code,email area_name,email device_name,email name,
       username device_code,is_superuser value,username symbol,username description,
       TO_CHAR (last_login, 'dd/MM/yyyy HH24:mi:ss') issue_date
  FROM auth_user