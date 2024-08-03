GET_INVENTORY_DATA = """
select /*+ parallel(8) */ distinct
       i.source as "Источник"
      ,i.loc as "ТТ"
      ,i.item as "Товар"
      ,i.sscov||'D' as "СВ"
    	 ,round(i.u_bucketforecast/7,2) as "Ср.дн.прогноз"
    	 ,i.inventorydate as "Дата заказа"
      ,i.oh as "Остаток"
      ,i.ALTCONSTRPOH as "Прогн.ост."                  
      ,i.SS as "СЗ"
      ,i.PRESENTATIONQTY as "ПЗ"
      ,case when i.ALLINTRANSIN=0
          then null
             else i.ALLINTRANSIN
       end as "В пути"
      ,i.PROMOID as "Промо"
      ,i.U_SOURCING as "ЦП"
      ,i.majorshipqty as "Квант"
      ,i.ALTCONSTRCOVDUR as "ТЗ в дн.»
from buf.jda_out_jda_inventory as i
where i.loc = :store and i.item = :item and trunc(i.inventorydate) between :date_from and :date_to;
"""

GET_RECOMMENDATION_DATA = """
select  rs.DEST
       ,rs.ITEM
       ,rs.ORDERPLACEDATE AS "Дата заказа"
       ,rs.arrivdate as "Дата_поставки"
       ,rs.LOADID as "BTL"
       ,rs.SAPORDERID as "№ заказа"
       ,round(rs.Arrivdate-rs.ORDERPLACEDATE,1) as "LT"    
       ,rs.QTY_LOG as "Факт заказ"
       ,rs.MUSTGOQTY as "Заказ"
       ,rs.RECQTY as "Реко"
       ,rs.TOTDMD1
       ,rs.TOTDMD2
       ,rs.MAXSS
       ,case when rs.TOTDMD2 is not null
          then rs.NEXTARRIVDATE-rs.ARRIVDATE
             else null
        end as "НОЗ"
       ,rs.pushruleid as "Push"
from buf.jda_out_jda_recommendations as rs
where rs.sendstatus = 1 
	 and rs.item = :item 
	 and rs.dest = :store 
	 and trunc(rs.orderplacedate) between :date_from and :date_to;  
"""

GET_SOURCING_DATA = """
select so.dest
    	 ,so.item
      ,so.u_centr as "ЦЗ"
from scpomgr.sourcing as so 
where so.u_promo_ind = 0 
	 and so.dest = :store 
	 and so.item = :item;  
"""

GET_SKU_DATA = """
select s.u_dmpsw as "DMP"
from scpomgr.SKU as s
WHERE s.loc = :store 
	 and s.item = :item;    
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
            and sale_data between :date_from and :date_to
      group by store_num, item_code, sale_date
)sl;  
"""

GET_ITEM_DATA = """
select it.item
    	 ,it.u_shelf_life as "СГ"
from scpomgr.item it
where it.item = :item;   
"""

GET_CLOSED_CASH_DATA = """
select c.item       
      ,c.loc
      ,c.sday_closed as "Закрытие кассы"
from BUF.JDA_IN_INVENTORY_STORE_arch as c
where c.item = :item 
	 and c.loc = :store 
	 and c.inventory_date between :date_from and :date_to;
"""