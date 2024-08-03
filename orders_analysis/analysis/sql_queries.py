GET_INVENTORY_DATA = """
    select distinct
       i.source
      ,i.loc
      ,i.item
      ,i.sscov
      ,round(i.u_bucketforecast/7,2) as forecast
      ,i.inventorydate
      ,i.oh
      ,i.ALTCONSTRPOH             
      ,i.SS
      ,i.PRESENTATIONQTY
      ,case when i.ALLINTRANSIN=0
          then null
             else i.ALLINTRANSIN
       end as INTRANSIN
      ,i.PROMOID
      ,i.U_SOURCING
      ,i.majorshipqty
      ,i.ALTCONSTRCOVDUR
from buf.jda_out_jda_inventory i
where i.loc = :store and i.item = :item 
    and trunc(i.inventorydate) between to_date(:date_from, 'yyyy-mm-dd') and to_date(:date_to, 'yyyy-mm-dd')
"""

GET_RECOMMENDATION_DATA = """
select  rs.DEST
       ,rs.ITEM
       ,rs.ORDERPLACEDATE
       ,rs.arrivdate
       ,rs.LOADID
       ,rs.SAPORDERID
       ,round(rs.Arrivdate-rs.ORDERPLACEDATE,1) as LT    
       ,rs.QTY_LOG
       ,rs.MUSTGOQTY
       ,rs.RECQTY
       ,rs.TOTDMD1
       ,rs.TOTDMD2
       ,rs.MAXSS
       ,case when rs.TOTDMD2 is not null
          then rs.NEXTARRIVDATE-rs.ARRIVDATE
             else null
        end as NOZ
       ,rs.pushruleid as PUSH
from buf.jda_out_jda_recommendations rs
where rs.sendstatus = 1 
	 and rs.item = :item 
	 and rs.dest = :store 
	 and trunc(rs.orderplacedate) between to_date(:date_from, 'yyyy-mm-dd') and to_date(:date_to, 'yyyy-mm-dd')
"""

GET_SOURCING_DATA = """
select so.dest
      ,so.item
      ,case when so.u_centr = 1 then 'X' else null end as CZ
from scpomgr.sourcing so 
where so.u_promo_ind = 0 
	 and so.dest = :store
	 and so.item = :item
"""

GET_SKU_DATA = """
select s.u_dmpsw as DMP
from SCPOMGR.SKU s
WHERE s.loc = :store 
	 and s.item = :item
"""

GET_SALES_DATA = """
select sl.store_num
	 ,sl.item_code
	 ,sl.sale_date
	 ,sl.sales_sum
from (select store_num
            ,item_code
            ,sale_date
            ,sum(qty) as sales_sum
      from mdi.ut_sales
      where store_num = :store 
	       and item_code = :item 
            and sale_date between to_date(:date_from, 'yyyy-mm-dd') and to_date(:date_to, 'yyyy-mm-dd')
      group by store_num, item_code, sale_date
)sl
"""

GET_ITEM_DATA = """
select it.item
    	 ,it.u_shelf_life as SG
from scpomgr.item it
where it.item = :item  
"""

GET_CLOSED_CASH_DATA = """
select c.item       
      ,c.loc
      ,c.sday_closed as CLOSED_CASSA
from BUF.JDA_IN_INVENTORY_STORE_arch c
where c.item = :item 
	 and c.loc = :store 
	 and trunc(to_date(c.inventory_date, 'yyyy-mm-dd')) between to_date(:date_from, 'yyyy-mm-dd') and to_date(:date_to, 'yyyy-mm-dd')
"""