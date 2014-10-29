-- Start of DDL Script for Package Body ASSET2.PCK_REPORT
-- Generated 30-Oct-2014 0:04:04 from ASSET2@ORCL

CREATE OR REPLACE 
PACKAGE pck_report
  IS


  FUNCTION convert_integer_to_roman(p_num in number)
  return varchar2;

  FUNCTION report_asset (p_capital_id   IN NUMBER,
                                           p_use_date        DATE,
                                           p_status          VARCHAR2)
      RETURN t_report_asset_tab;

  FUNCTION report_asset_summarize (p_capital_id   IN NUMBER)
      RETURN t_report_asset_sum_tab;

END; -- Package spec
/


CREATE OR REPLACE 
PACKAGE BODY pck_report
IS


FUNCTION convert_integer_to_roman(p_num in number)
return varchar2
is
v_result varchar2(10):='';
type array_t_char is varray(7) of varchar2(3);
type array_t_number is varray(7) of number(4);
roman_array array_t_char:=array_t_char('L','XL','X','IX','V','IV','I');
int_array array_t_number:=array_t_number(50,40,10,9,5,4,1);
v_match number(4);
v_num number(4);
begin
    v_num:=p_num;
    for i in 1..int_array.count
    loop
        v_match:=trunc(v_num/int_array(i));
        if(v_match<>0) then

        for j in 1..v_match
        loop
            v_result:=v_result||roman_array(i);
        end loop;
        v_num:= mod(v_num,int_array(i));
         end if;
    end loop;
    return v_result;
end;

FUNCTION report_asset (p_capital_id   IN NUMBER,
                                         p_use_date        DATE,
                                         p_status          VARCHAR2)
    RETURN t_report_asset_tab
AS
    l_tab         t_report_asset_tab := t_report_asset_tab ();
    --l_sum_tab     t_sum_asset_tab:=t_sum_asset_tab();
    v_max_level   NUMBER(1):=0;
    v_r_level     NUMBER(1);
    v_cur_parent_id number(10);
    v_cur_child_id number(10);

    CURSOR c_data
    IS
        SELECT   b.id serial_id,
                 a.id,
                 a.parent_id,
                 a.code,
                 b.name,
                 a.asset_level,
                 b.serial,
                 b.capital_id_new capital_id,
                 b.use_date,
                 (SELECT   name
                    FROM   list
                   WHERE   list_type = '4' AND id = b.state_id)
                     status,
                 b.unit,
                 (SELECT   supplier_name
                    FROM   supplier
                   WHERE   id = b.supplier_id)
                     supplier,
                  nvl(b.original_value_new,0) acc_original,
                 nvl(b.remain_value_new,0) acc_remain,
                 nvl(C.original_value_new,0) inv_original,
                 nvl(c.remain_value_new,0) inv_remain,
                 b.note_new note,
                 b.goal_id,
                 b.country_id,
                 b.product_date,
                 b.power,
                 b.INTERVAL,
                 d.name place,
               (SELECT dept_name FROM dept WHERE dept.id=d.dept_id) dept,
                 (select name from ap_domain where type='SOURCE' and code=b.source) source,
                  b.decision_no,
                 b.decision_date,
                 a.account_no,
                 b.document_status
          FROM   (    SELECT   id,
                               code,
                               name,
                               parent_id,
                               LEVEL asset_level,account_no
                        FROM   asset
                  START WITH   parent_id IS NULL
                  CONNECT BY   PRIOR id = parent_id) a,
                ( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from stock_asset_serial m ,capital_value n where m.id=n.stock_asset_serial_id(+)) b,
                 ( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from check_stock_asset_serial m ,check_capital_value n where m.id=n.check_stock_asset_serial_id(+) and m.stock_asset_serial_id=n.stock_asset_serial_id(+))  c
                     ,stock d
         WHERE       1 = 1
                 AND b.id = c.stock_asset_serial_id(+)
                 AND a.id = b.asset_id
                 AND b.stock_id=d.stock_id
                 AND b.parent_id IS null
                 AND (p_capital_id IS NULL OR b.capital_id = p_capital_id)
                 AND (p_status IS NULL OR b.state_id = p_status)
                 AND (p_use_date IS NULL OR b.use_date >= TRUNC (p_use_date));

    CURSOR c_data_serial(p_parent_id number)
    IS
        SELECT m.*,LEVEL asset_level FROM (SELECT   b.id serial_id,
                 NULL id,
                 b.parent_id,
                 a.code,
                 b.name,

                 b.serial,
                 b.capital_id,
                 b.use_date,
                 (SELECT   name
                    FROM   list
                   WHERE   list_type = '4' AND id = b.state_id)
                     status,
                 b.unit,
                 (SELECT   supplier_name
                    FROM   supplier
                   WHERE   id = b.supplier_id)
                     supplier,
                 nvl(b.original_value_new,0) acc_original,
                 nvl(b.remain_value_new,0) acc_remain,
                 nvl(C.original_value_new,0) inv_original,
                 nvl(c.remain_value_new,0) inv_remain,
                 b.note_new note,
                 b.goal_id,
                 b.country_id,
                 b.product_date,
                 b.power,
                 b.INTERVAL,
                 d.name place,
               (SELECT dept_name FROM dept WHERE dept.id=d.dept_id) dept,
                 (select name from ap_domain where type='SOURCE' and code=b.source) source,
                  b.decision_no,
                 b.decision_date,
                a. account_no,
                 b.document_status
          FROM   asset a,( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from stock_asset_serial m ,capital_value n where m.id=n.stock_asset_serial_id(+)) b,
                 ( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from check_stock_asset_serial m ,check_capital_value n where m.id=n.check_stock_asset_serial_id(+) and m.stock_asset_serial_id=n.stock_asset_serial_id(+))  c
                     ,stock d
         WHERE       1 = 1
                 AND b.id = c.stock_asset_serial_id(+)
                 AND a.id=b.asset_id
                 AND b.stock_id=d.stock_id
                 AND (p_capital_id IS NULL OR b.capital_id = p_capital_id)
                 AND (p_status IS NULL OR b.state_id = p_status)
                 AND (p_use_date IS NULL OR b.use_date >= TRUNC (p_use_date))
              ) m
              START WITH   parent_id=p_parent_id
              CONNECT BY   PRIOR serial_id = parent_id;


    v_row_num number(4):=0;
    v_cur_row_num number(4);
    v_child_row_num number(4);

    cursor c_check(p_asset_id number) is
    select nvl(r,0) from (select asset_id,rownum r from table(l_tab)) where (p_asset_id is null and asset_id is null) or asset_id=p_asset_id;
    cursor c_get_parent_info(p_asset_id number)
    is select id,code,name from asset where id=p_asset_id;
    v_parent_code varchar2(10);
    v_parent_name varchar2(250);
    v_parent_id number(10);
    v_sum_acc_org number(20);
    v_sum_inv_org number(20);
    v_sum_acc_remain number(20);
    v_sum_inv_remain number(20);

    cursor c_get_sum(p_asset_id number) is
    select sum(acc_original),sum(acc_remain),sum(inven_original),sum(inven_remain) from table(l_tab) where parent_id=p_asset_id;

    type array_t_number is varray(10) of number(4);
    array_level  array_t_number:=array_t_number(1);
    v_count_in_stock number(4):=0;
    v_no varchar2(10);
    v_parent_no varchar2(10);
    v_num_child number(4);
    cursor c_get_parent_no(p_parent_id number)
    is select no from table(l_tab) where asset_id=p_parent_id;
    v_serial_name varchar2(500);

    CURSOR c_check_leaf_is_high_level(p_parent_id NUMBER)
     IS  SELECT nvl(max(lv),-1) FROM
            (SELECT asset_id,LEVEL lv FROM table(l_tab)
                START WITH parent_id=p_parent_id
                CONNECT BY PRIOR asset_id=parent_id);
    v_max_level_to_check NUMBER;
    v_count_parent NUMBER;
BEGIN

    FOR r_data in c_data
    LOOP
       v_count_in_stock:=v_count_in_stock+1;
       v_r_level:=r_data.asset_level;
       if(v_r_level > v_max_level) then
            v_max_level:=v_r_level;
       end if;
        if(array_level.count<v_max_level) then
                    for j in array_level.count..v_max_level-1
                    LOOP
                        array_level.extend;
                        array_level(array_level.last):=1;
                    end loop;
       end if;
       l_tab.extend;
       v_row_num:=v_row_num+1;
       v_child_row_num:=v_row_num;
       begin
       l_tab(l_tab.last):=t_report_asset_row(v_row_num,v_count_in_stock,r_data.serial_id,NULL,
                                                     r_data.id,
                                                     r_data.name,
                                                     r_data.code,
                                                     r_data.serial,
                                                     r_data.capital_id,
                                                     r_data.use_date,
                                                     r_data.status,
                                                     r_data.unit,
                                                     r_data.supplier,
                                                     r_data.acc_original,
                                                     r_data.acc_remain,
                                                     r_data.inv_original,
                                                     r_data.inv_remain,
                                                     r_data.note,
                                                     v_r_level,
                                                     null,1,1,
                                                     r_data.goal_id  ,
                                                     r_data.country_id ,
                                                     r_data.product_date  ,
                                                     r_data.power  ,
                                                     r_data.INTERVAL  ,
                                                     r_data.place ,
                                                     r_data.dept ,
                                                     r_data.source ,
                                                     r_data.decision_no ,
                                                     r_data.decision_date  ,
                                                     r_data.account_no,
                                                     r_data.document_status,'0' );

        exception when others then
            dbms_output.put_line(r_data.parent_id||'\n'||
                                                     r_data.name||'\n'||
                                                     r_data.code||'\n'||
                                                     r_data.serial||'\n'||
                                                     r_data.capital_id||'\n'||
                                                     r_data.use_date||'\n'||
                                                     r_data.status||'\n'||
                                                     r_data.unit||'\n'||
                                                     r_data.supplier||'\n'||
                                                     r_data.acc_original||'\n'||
                                                     r_data.acc_remain||'\n'||
                                                     r_data.inv_original||'\n'||
                                                     r_data.inv_remain||'\n'||
                                                     r_data.note||'\n'||
                                                     v_r_level||'\n'||

                                                     r_data.goal_id  ||'\n'||
                                                     r_data.country_id ||'\n'||
                                                     r_data.product_date  ||'\n'||
                                                     r_data.power  ||'\n'||
                                                     r_data.INTERVAL  ||'\n'||
                                                     r_data.place ||'\n'||
                                                     r_data.dept ||'\n'||
                                                     r_data.source ||'\n'||
                                                     r_data.decision_no ||'\n'||
                                                     r_data.decision_date  ||'\n'||
                                                     r_data.account_no||'\n'||
                                                     r_data.document_status );
       end;
       v_cur_parent_id:=r_data.id;
--       dbms_output.put_line('loop level from '||1||'to '||(v_r_level-1));
       v_parent_id:=r_data.id;
       v_count_parent:=0;
       WHILE(true)
       LOOP
          v_cur_row_num:=0;
          v_count_parent:=v_count_parent+1;
            select parent_id,code,name into v_parent_id,v_parent_code,v_parent_name from asset where id=v_cur_parent_id;
             open c_check(v_cur_parent_id);
            fetch c_check into v_cur_row_num;
          close  c_check;
          open c_get_sum(v_cur_parent_id);
            fetch c_get_sum into v_sum_acc_org,v_sum_acc_remain,v_sum_inv_org,v_sum_inv_remain;
          close c_get_sum;

          if(v_cur_row_num=0) THEN
              v_parent_no:=null;
              v_no:='';
              l_tab.extend;
              v_row_num:=v_row_num+1;

              for m in 1..v_count_parent
              loop

                l_tab(l_tab.count-m+1):=l_tab(l_tab.count-m);
              end loop;

              l_tab(l_tab.count-v_count_parent):=t_report_asset_row(v_row_num,null,null,v_cur_parent_id,
                                                     v_parent_id,
                                                     v_parent_name,
                                                     v_parent_code,
                                                     null,
                                                     null,
                                                     null,
                                                     null,
                                                     null,
                                                     null,
                                                     v_sum_acc_org,
                                                     v_sum_acc_remain,
                                                     v_sum_inv_org,
                                                     v_sum_inv_remain,
                                                     null,
                                                     v_r_level+1-v_count_parent,
                                                     null,0,0,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,'0');
         else

            l_tab(v_cur_row_num).acc_original:=v_sum_acc_org;
           l_tab(v_cur_row_num).acc_remain:=v_sum_acc_remain;
          l_tab(v_cur_row_num).inven_original:=v_sum_inv_org;
          l_tab(v_cur_row_num).inven_remain:=v_sum_inv_remain;
          end if;
          v_cur_parent_id:=v_parent_id;
          EXIT WHEN v_parent_id IS NULL;
       END LOOP;


--xu ly them cha con trong stock_asset_serial
       FOR r_data_serial IN c_data_serial(r_data.serial_id)
       LOOP
           v_serial_name:=r_data_serial.name;
           FOR x IN 1..r_data_serial.asset_level
           LOOP
                v_serial_name:='+ '||v_serial_name;
           END LOOP;
           l_tab.extend;
           l_tab(l_tab.last):=t_report_asset_row(null,null,r_data_serial.serial_id,r_data_serial.id,
                                                         r_data_serial.parent_id,
                                                         v_serial_name,
                                                         r_data_serial.code,
                                                         r_data_serial.serial,
                                                         r_data_serial.capital_id,
                                                         r_data_serial.use_date,
                                                         r_data_serial.status,
                                                         r_data_serial.unit,
                                                         r_data_serial.supplier,
                                                         r_data_serial.acc_original,
                                                         r_data_serial.acc_remain,
                                                         r_data_serial.inv_original,
                                                         r_data_serial.inv_remain,
                                                         r_data_serial.note,
                                                         null,
                                                         null,NULL ,1,
                                                         r_data_serial.goal_id  ,
                                                         r_data_serial.country_id ,
                                                         r_data_serial.product_date  ,
                                                         r_data_serial.power  ,
                                                         r_data_serial.INTERVAL  ,
                                                         r_data_serial.place ,
                                                         r_data_serial.dept ,
                                                         r_data_serial.source ,
                                                         r_data_serial.decision_no ,
                                                         r_data_serial.decision_date  ,
                                                         r_data_serial.account_no,
                                                         r_data_serial.document_status,'1' );
       END LOOP;
--

    END LOOP;


    --init number no

     array_level(1):=1;

     for i in 1..l_tab.count
       loop
           if(l_tab(i).cur_level=1) then
                l_tab(i).no:=convert_integer_to_roman(array_level(1));
                array_level(1):=array_level(1)+1;
           elsif(l_tab(i).cur_level IS NOT NULL ) then
                if(l_tab(i).flag_in_stock=0) then
                    open c_get_parent_no(l_tab(i).parent_id);
                        fetch c_get_parent_no into v_parent_no;
                    close c_get_parent_no;
                    select count(parent_id) into v_num_child from table(l_tab) where parent_id=l_tab(i).parent_id and is_leaf=0 and no is not null;
                    l_tab(i).no:= v_parent_no||'.'||(v_num_child+1);
                end if;
           end if;
       end loop;
    RETURN l_tab;
END;

FUNCTION report_asset_summarize (p_capital_id   IN NUMBER)
    RETURN t_report_asset_sum_tab
AS
    l_tab         t_report_asset_sum_tab := t_report_asset_sum_tab ();
    --l_sum_tab     t_sum_asset_tab:=t_sum_asset_tab();
    v_max_level   NUMBER(1):=0;
    v_r_level     NUMBER(1);
    v_cur_parent_id number(10);
    v_cur_child_id number(10);

    CURSOR c_data
    IS
        SELECT   b.id serial_id,
                 a.id,
                 a.parent_id,
                 a.code,
                 b.name,
                 a.asset_level,
                 b.capital_id_new capital_id,
                  b.serial,
                 b.use_date,
                 (SELECT   name
                    FROM   list
                   WHERE   list_type = '4' AND id = b.state_id)
                     status,
                 b.unit,
                 (SELECT   supplier_name
                    FROM   supplier
                   WHERE   id = b.supplier_id)
                     supplier,
                                 case when   b.state_id in (select id from list where list_type='4' and code='10') then b.original_value_new else 0 end org_10,
                 case when   b.state_id in (select id from list where list_type='4' and code='20') then b.original_value_new else 0 end org_20,
                 case when   b.state_id in (select id from list where list_type='4' and code='30') then b.original_value_new else 0 end org_30,
                 case when   b.state_id in (select id from list where list_type='4' and code='40') then b.original_value_new else 0 end org_40,
                 case when   b.state_id in (select id from list where list_type='4' and code='50') then b.original_value_new else 0 end org_50,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='10') then c.remain_value_new else 0 end remain_10,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='20') then c.remain_value_new else 0 end remain_20,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='30') then c.remain_value_new else 0 end remain_30,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='40') then c.remain_value_new else 0 end remain_40,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='50') then c.remain_value_new else 0 end remain_50,
                 b.note_new note,
                  b.goal_id,
                 b.country_id,
                 b.product_date,
                 b.power,
                 b.INTERVAL,
                 d.name place,
               (SELECT dept_name FROM dept WHERE dept.id=d.dept_id) dept,
                 (select name from ap_domain where type='SOURCE' and code=b.source) source,
                  b.decision_no,
                 b.decision_date,
                 a.account_no,
                 b.document_status
          FROM   (    SELECT   id,
                               code,
                               name,
                               parent_id,
                               LEVEL asset_level,account_no
                        FROM   asset
                  START WITH   parent_id IS NULL
                  CONNECT BY   PRIOR id = parent_id) a,
                ( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from stock_asset_serial m ,capital_value n where m.id=n.stock_asset_serial_id(+)) b,
                 ( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from check_stock_asset_serial m ,check_capital_value n where m.id=n.check_stock_asset_serial_id(+) and m.stock_asset_serial_id=n.stock_asset_serial_id(+))  c
                     ,stock d
         WHERE       1 = 1
                 AND b.id = c.stock_asset_serial_id(+)
                 AND a.id = b.asset_id
                 AND b.stock_id=d.stock_id
                 AND b.parent_id IS NULL
                 AND (p_capital_id IS NULL OR b.capital_id = p_capital_id);
     CURSOR c_data_serial(p_parent_id number)
    IS
        SELECT m.*,LEVEL asset_level FROM (SELECT b.id serial_id,
                 NULL id,
                 b.parent_id,
                 a.code,
                 b.name,

                 b.capital_id_new capital_id,
                  b.serial,
                 b.use_date,
                 (SELECT   name
                    FROM   list
                   WHERE   list_type = '4' AND id = b.state_id)
                     status,
                 b.unit,
                 (SELECT   supplier_name
                    FROM   supplier
                   WHERE   id = b.supplier_id)
                     supplier,
                 case when   b.state_id in (select id from list where list_type='4' and code='10') then b.original_value_new else 0 end org_10,
                 case when   b.state_id in (select id from list where list_type='4' and code='20') then b.original_value_new else 0 end org_20,
                 case when   b.state_id in (select id from list where list_type='4' and code='30') then b.original_value_new else 0 end org_30,
                 case when   b.state_id in (select id from list where list_type='4' and code='40') then b.original_value_new else 0 end org_40,
                 case when   b.state_id in (select id from list where list_type='4' and code='50') then b.original_value_new else 0 end org_50,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='10') then c.remain_value_new else 0 end remain_10,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='20') then c.remain_value_new else 0 end remain_20,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='30') then c.remain_value_new else 0 end remain_30,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='40') then c.remain_value_new else 0 end remain_40,
                 case when   c.check_state_id in (select id from list where list_type='4' and code='50') then c.remain_value_new else 0 end remain_50,
                 b.note_new note,
                  b.goal_id,
                 b.country_id,
                 b.product_date,
                 b.power,
                 b.INTERVAL,
                 d.name place,
               (SELECT dept_name FROM dept WHERE dept.id=d.dept_id) dept,
                 (select name from ap_domain where type='SOURCE' and code=b.source) source,
                  b.decision_no,
                 b.decision_date,
                 a.account_no,
                 b.document_status
          FROM   asset a,( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from stock_asset_serial m ,capital_value n where m.id=n.stock_asset_serial_id(+)) b,
                 ( select m.*,n.capital_id capital_id_new,n.original_value original_value_new,
                    n.remain_value remain_value_new,n.description note_new
                     from check_stock_asset_serial m ,check_capital_value n where m.id=n.check_stock_asset_serial_id(+) and m.stock_asset_serial_id=n.stock_asset_serial_id(+))  c
                     ,stock d
         WHERE       1 = 1
                 AND b.id = c.stock_asset_serial_id(+)
                 AND a.id=b.asset_id
                 AND b.stock_id=d.stock_id
                 AND (p_capital_id IS NULL OR b.capital_id = p_capital_id)
              ) m
              START WITH   parent_id=p_parent_id
              CONNECT BY   PRIOR serial_id = parent_id;

    v_row_num number(4):=0;
    v_cur_row_num number(4);
    v_child_row_num number(4);

    cursor c_check(p_asset_id number) is
    select nvl(r,0) from (select asset_id,rownum r from table(l_tab)) where (p_asset_id is null and asset_id is null) or asset_id=p_asset_id;
    cursor c_get_parent_info(p_asset_id number)
    is select id,code,name from asset where id=p_asset_id;
    v_parent_code varchar2(10);
    v_parent_name varchar2(250);
    v_parent_id number(10);
    v_sum_org_10 number(20);
    v_sum_org_20 number(20);
    v_sum_org_30 number(20);
    v_sum_org_40 number(20);
    v_sum_org_50 number(20);
    v_sum_remain_10 number(20);
    v_sum_remain_20 number(20);
    v_sum_remain_30 number(20);
    v_sum_remain_40 number(20);
    v_sum_remain_50 number(20);

    cursor c_get_sum(p_asset_id number) is
    select sum(original_10),sum(original_20),sum(original_30),sum(original_40),sum(original_50),
            sum(remain_10),sum(remain_20),sum(remain_30),sum(remain_40),sum(remain_50)
         from table(l_tab) where parent_id=p_asset_id;

    type array_t_number is varray(10) of number(4);
    array_level  array_t_number:=array_t_number();
    v_count_in_stock number(4):=0;
    v_no varchar2(10);
    v_parent_no varchar2(10);
    v_num_child number(4);
    cursor c_get_parent_no(p_parent_id number)
    is select no from table(l_tab) where asset_id=p_parent_id;
    v_serial_name varchar2(500);
     CURSOR c_check_leaf_is_high_level(p_parent_id NUMBER)
     IS  SELECT nvl(max(lv),-1) FROM
            (SELECT asset_id,LEVEL lv FROM table(l_tab)
                START WITH parent_id=p_parent_id
                CONNECT BY PRIOR asset_id=parent_id);
    v_max_level_to_check NUMBER;
    v_count_parent NUMBER;
BEGIN

    FOR r_data in c_data
    LOOP
       v_count_in_stock:=v_count_in_stock+1;
       v_r_level:=r_data.asset_level;
       if(v_r_level > v_max_level) then
            v_max_level:=v_r_level;
       end if;
       if(array_level.count<v_max_level) then
                    for j in array_level.count..v_max_level-1
                    LOOP
                        array_level.extend;
                        array_level(array_level.last):=1;
                    end loop;
       end if;
       l_tab.extend;
       v_row_num:=v_row_num+1;
       v_child_row_num:=v_row_num;
       l_tab(l_tab.last):=t_report_asset_sum_row(v_row_num,v_count_in_stock,null,
                                                     r_data.id,
                                                     r_data.name,
                                                     r_data.code,
                                                     r_data.capital_id,
                                                     r_data.org_10,
                                                     r_data.org_20,
                                                     r_data.org_30,
                                                     r_data.org_40,
                                                     r_data.org_50,
                                                     r_data.remain_10,
                                                     r_data.remain_20,
                                                     r_data.remain_30,
                                                     r_data.remain_40,
                                                     r_data.remain_50,
                                                     null,
                                                     v_r_level,
                                                     null,1,1,
                                                     r_data.goal_id  ,
                                                     r_data.country_id ,
                                                     r_data.product_date  ,
                                                     r_data.power  ,
                                                     r_data.INTERVAL  ,
                                                     r_data.place ,
                                                     r_data.dept ,
                                                     r_data.source ,
                                                     r_data.decision_no ,
                                                     r_data.decision_date  ,
                                                     r_data.account_no,
                                                     r_data.document_status,
                                                     r_data.serial,
                                                     r_data.use_date,
                                                     r_data.unit,
                                                     r_data.supplier,
                                                     r_data.status,'0');


       v_cur_parent_id:=r_data.id;
      -- dbms_output.put_line('loop level from '||1||'to '||(v_r_level-1));
       v_parent_id:=r_data.id;
       v_count_parent:=0;
      WHILE(true)
       LOOP
        v_cur_row_num:=0;
          v_count_parent:=v_count_parent+1;
            select parent_id,code,name into v_parent_id,v_parent_code,v_parent_name from asset where id=v_cur_parent_id;
             open c_check(v_cur_parent_id);
            fetch c_check into v_cur_row_num;
          close  c_check;
          open c_get_sum(v_cur_parent_id);
           fetch c_get_sum into v_sum_org_10,v_sum_org_20,v_sum_org_30,v_sum_org_40,v_sum_org_50
                ,v_sum_remain_10,v_sum_remain_20,v_sum_remain_30,v_sum_remain_40,v_sum_remain_50;
          close c_get_sum;
           if(v_cur_row_num=0) THEN
              v_no:='';
              v_parent_no:=null;
              l_tab.extend;
              v_row_num:=v_row_num+1;

              for m in 1..v_count_parent
              loop

                l_tab(l_tab.count-m+1):=l_tab(l_tab.count-m);
              end loop;


              l_tab(l_tab.count-v_count_parent):=t_report_asset_sum_row(v_row_num,v_no,v_cur_parent_id,
                                                     v_parent_id,
                                                     v_parent_name,
                                                     v_parent_code,
                                                     null,
                                                     v_sum_org_10,
                                                     v_sum_org_20,
                                                     v_sum_org_30,
                                                     v_sum_org_40,
                                                     v_sum_org_50,
                                                     v_sum_remain_10,
                                                     v_sum_remain_20,
                                                     v_sum_remain_30,
                                                     v_sum_remain_40,
                                                     v_sum_remain_50,
                                                     null,
                                                     v_r_level+1-v_count_parent,
                                                     null,0,0,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,
                                                     NULL,'0');

         else

            l_tab(v_cur_row_num).original_10:=v_sum_org_10;
            l_tab(v_cur_row_num).original_20:=v_sum_org_20;
            l_tab(v_cur_row_num).original_30:=v_sum_org_30;
            l_tab(v_cur_row_num).original_40:=v_sum_org_40;
            l_tab(v_cur_row_num).original_50:=v_sum_org_50;
            l_tab(v_cur_row_num).remain_10:=v_sum_remain_10;
            l_tab(v_cur_row_num).remain_20:=v_sum_remain_20;
            l_tab(v_cur_row_num).remain_30:=v_sum_remain_30;
            l_tab(v_cur_row_num).remain_40:=v_sum_remain_40;
            l_tab(v_cur_row_num).remain_50:=v_sum_remain_50;
          end if;


         v_cur_parent_id:=v_parent_id;
          EXIT WHEN v_parent_id IS NULL;
       END LOOP;



--xu ly them cha con trong stock_asset_serial
       FOR r_data_serial IN c_data_serial(r_data.serial_id)
       LOOP
           v_serial_name:=r_data_serial.name;
           FOR x IN 1..r_data_serial.asset_level
           LOOP
                v_serial_name:='-'||v_serial_name;
           END LOOP;
           l_tab.extend;
           l_tab(l_tab.last):=t_report_asset_sum_row(null,null,r_data.id,
                                                     r_data_serial.parent_id,
                                                     v_serial_name,
                                                     r_data_serial.code,
                                                     r_data_serial.capital_id,
                                                     r_data_serial.org_10,
                                                     r_data_serial.org_20,
                                                     r_data_serial.org_30,
                                                     r_data_serial.org_40,
                                                     r_data_serial.org_50,
                                                     r_data_serial.remain_10,
                                                     r_data_serial.remain_20,
                                                     r_data_serial.remain_30,
                                                     r_data_serial.remain_40,
                                                     r_data_serial.remain_50,
                                                     null,
                                                     null,
                                                     null,null,1,
                                                     r_data_serial.goal_id  ,
                                                     r_data_serial.country_id ,
                                                     r_data_serial.product_date  ,
                                                     r_data_serial.power  ,
                                                     r_data_serial.INTERVAL  ,
                                                     r_data_serial.place ,
                                                     r_data_serial.dept ,
                                                     r_data_serial.source ,
                                                     r_data_serial.decision_no ,
                                                     r_data_serial.decision_date  ,
                                                     r_data_serial.account_no,
                                                     r_data_serial.document_status,
                                                     r_data_serial.serial,
                                                     r_data_serial.use_date,
                                                     r_data_serial.unit,
                                                     r_data_serial.supplier,
                                                     r_data_serial.status,'1' );
       END LOOP;
--------------

    END LOOP;

    --init number no
     array_level(1):=1;
     for i in 1..l_tab.count
       loop
           if(l_tab(i).cur_level=1) then
                l_tab(i).no:=convert_integer_to_roman(array_level(1));
                array_level(1):=array_level(1)+1;
           else
                if(l_tab(i).flag_in_stock=0) then
                    open c_get_parent_no(l_tab(i).parent_id);
                        fetch c_get_parent_no into v_parent_no;
                    close c_get_parent_no;
                    select count(parent_id) into v_num_child from table(l_tab) where parent_id=l_tab(i).parent_id and is_leaf=0 and no is not null;
                    l_tab(i).no:= v_parent_no||'.'||(v_num_child+1);
                end if;
           end if;
       end loop;
    RETURN l_tab;
END;
END;
/


-- End of DDL Script for Package Body ASSET2.PCK_REPORT

