SELECT * FROM payment_detail;
--advance
SELECT               
              p.receipt_no,
              NULL note,
               (SELECT   isdn
                  FROM   customer c
                 WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) resource1,
               (SELECT   cust_code
                  FROM   customer c
                 WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) customer_no,
              curr_type currency,
              substr((SELECT   NAME
                  FROM   ap_domain
                 WHERE   TYPE = 'PAYMENT_STATUS' AND code = p.status AND ROWNUM = 1), 1, 1) payment_status,
              nvl(
              CASE WHEN (SELECT   isdn FROM   customer c
                    WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) IS NULL THEN
                    (SELECT NAME FROM area
                    WHERE parent_code IS NULL AND area.area_code = (SELECT p3.province FROM staff p2, shop p3 WHERE p2.shop_id = p3.shop_id AND p2.staff_code = p.user_name AND ROWNUM = 1)AND ROWNUM = 1)
              ELSE
                  (SELECT NAME
                   FROM area
                   WHERE parent_code IS NULL AND area.area_code = (SELECT c2.province FROM customer c2 WHERE c2.isdn = (SELECT   isdn
                  FROM   customer c
                 WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) AND ROWNUM = 1))
                  END, 'LTC')  province_name,
             (SELECT st.NAME FROM staff st WHERE st.staff_code = p.man_staff_code AND ROWNUM = 1) cashier_name,
               CASE WHEN p.payment_type = '00' THEN
                  p.amount_left - (((p.amount_left * nvl(p.discount_rate, 0)) / 100))
               ELSE 0                   
               END cash,
               CASE WHEN p.payment_type = '05' THEN
                  p.amount_left - (((p.amount_left * nvl(p.discount_rate, 0)) / 100))
               ELSE 0                  
               END cheque,
               CASE WHEN p.payment_type = '01' THEN
                  p.amount_left - (((p.amount_left * nvl(p.discount_rate, 0)) / 100))
               ELSE 0                  
               END credit,
               CASE WHEN p.payment_type = '02' THEN
                  p.amount_left - (((p.amount_left * nvl(p.discount_rate, 0)) / 100))
               ELSE 0                  
              END bank,
              ((p.amount_left * nvl(p.discount_rate, 0)) / 100) discount_amount,
              p.amount_left advanced_amount,
              nvl(commission_amount,0),
              NULL product,
            'Advanced Payment' invoice_type              
 FROM payment p
WHERE amount_left>0 
AND status<>'0'
AND payment_type NOT IN ('10','09');
SELECT               
              p.receipt_no,
              p.invoice_no note,
               (SELECT   isdn
                  FROM   customer c
                 WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) resource1,
               (SELECT   cust_code
                  FROM   customer c
                 WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) customer_no,
              get_currency currency,
              substr((SELECT   NAME
                  FROM   ap_domain
                 WHERE   TYPE = 'PAYMENT_STATUS' AND code = p.status AND ROWNUM = 1), 1, 1) payment_status,
              nvl(
              CASE WHEN (SELECT   isdn FROM   customer c
                    WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) IS NULL THEN
                    (SELECT NAME FROM area
                    WHERE parent_code IS NULL AND area.area_code = (SELECT p3.province FROM shop p3 WHERE  ROWNUM = 1)AND ROWNUM = 1)
              ELSE
                  (SELECT NAME
                   FROM area
                   WHERE parent_code IS NULL AND area.area_code = (SELECT c2.province FROM customer c2 WHERE c2.isdn = (SELECT   isdn
                  FROM   customer c
                 WHERE   c.cust_id = p.cust_id AND ROWNUM = 1) AND ROWNUM = 1))
                  END, 'LTC')  province_name,
             (SELECT st.NAME FROM staff st WHERE st.staff_code = m.man_staff_code AND ROWNUM = 1) cashier_name,
               CASE WHEN p.payment_type = '00' THEN amount_vat
               ELSE 0                   
               END cash,
               CASE WHEN p.payment_type = '05' THEN amount_vat
               ELSE 0                  
               END cheque,
               CASE WHEN p.payment_type = '01' THEN amount_vat
               ELSE 0                  
               END credit,
               CASE WHEN p.payment_type = '02' THEN amount_vat
               ELSE 0                  
              END bank,
              0 discount_amount,
              0 advanced_amount,
              0 commission_amount,
              NULL product,
              (SELECT invoice_type FROM invoices WHERE invoice_id=p.cust_debit_detail_id) invoice_type              
 FROM payment_detail p,payment m
WHERE m.payment_id=p.payment_id
AND m.status<>'0'
AND m.payment_type NOT IN ('10','09');

