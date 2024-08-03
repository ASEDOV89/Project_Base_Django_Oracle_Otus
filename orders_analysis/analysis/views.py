import csv
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .models import Comment
from .connect_data import (
    DIALECT,
    SQL_DRIVER,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    SERVICE
)
from .sql_queries import (
    GET_INVENTORY_DATA,
    GET_RECOMMENDATION_DATA,
    GET_SOURCING_DATA,
    GET_SKU_DATA,
    GET_SALES_DATA,
    GET_ITEM_DATA,
    GET_CLOSED_CASH_DATA
)

CONNECTION_URI = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
engine = create_engine(CONNECTION_URI)


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class CommentsView(View):
    def get(self, request):
        return render(request, 'comments.html')

class SubmitCommentView(View):
    def post(self, request):
        author = request.POST['author']
        email = request.POST['email']
        comment = request.POST['comment']
        Comment.objects.create(author=author, email=email, comment=comment)
        return redirect('comments')


class GenerateReportView(View):
    def get(self, request):
        store: str = request.GET['store']
        item = request.GET['item']
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']

        report_data = self.generate_report_data(store, item, date_from, date_to)

        # def format_dates(report_data):
        #     for row in report_data:
        #
        #         if 'inventorydate' in row and row['inventorydate']:
        #             date_object = datetime.strptime(row['inventorydate'], '%Y-%m-%d')
        #             row['inventorydate'] = date_object.strftime('%d.%m.%Y')
        #
        #         if 'arrivdate' in row and row['arrivdate']:
        #             date_object = datetime.strptime(row['arrivdate'], '%Y-%m-%d')
        #             row['arrivdate'] = date_object.strftime('%d.%m.%Y')
        #
        #     return report_data
        #
        # formatted_data = format_dates(report_data)

        return render(request, 'report.html', report_data)

    def generate_report_data(self, store, item, date_from, date_to):

        Session = sessionmaker(bind=engine)

        with Session() as session:
            inventory_data = session.execute(text(GET_INVENTORY_DATA), {'store': store, 'item': item, 'date_from': date_from, 'date_to': date_to})
            recommendation_data = session.execute(text(GET_RECOMMENDATION_DATA), {'store': store, 'item': item, 'date_from': date_from, 'date_to': date_to})
            sourcing_data = session.execute(text(GET_SOURCING_DATA), {'store': store, 'item': item})
            sku_data = session.execute(text(GET_SKU_DATA), {'store': store, 'item': item})
            sales_data = session.execute(text(GET_SALES_DATA), {'store': store, 'item': item, 'date_from': date_from, 'date_to': date_to})
            item_data = session.execute(text(GET_ITEM_DATA), {'item': item})
            closed_cash_data = session.execute(text(GET_CLOSED_CASH_DATA), {'store': store, 'item': item, 'date_from': date_from, 'date_to': date_to})

        df_inventory = pd.DataFrame(inventory_data.fetchall())
        df_recommendation = pd.DataFrame(recommendation_data.fetchall())
        df_sourcing = pd.DataFrame(sourcing_data.fetchall())
        df_sku = pd.DataFrame(sku_data.fetchall())
        df_sales = pd.DataFrame(sales_data.fetchall())
        df_item = pd.DataFrame(item_data.fetchall())
        df_closed_cash = pd.DataFrame(closed_cash_data.fetchall())

        report_df = df_inventory.merge(df_recommendation, left_on=['item', 'loc', 'inventorydate'], right_on=['item', 'dest', 'orderplacedate'], how='left')
        report_df = report_df.merge(df_sourcing, left_on=['loc', 'item'], right_on=['dest', 'item'], how='left')
        # report_df = report_df.merge(df_sku, left_on=['item', 'loc'], right_on=['item', 'loc'], how='left')
        report_df = report_df.merge(df_sales, left_on=['inventorydate', 'loc', 'item'], right_on=['sale_date', 'store_num', 'item_code'], how='left')
        report_df = report_df.merge(df_item, left_on='item', right_on='item', how='left')
        # report_df = report_df.merge(df_closed_cash, left_on=['item', 'loc', 'inventorydate'], right_on=['item', 'loc', 'inventory_date'], how='left')

        selected_columns = [
            'inventorydate',
            'source',
            'loc',
            'item',
            'sscov',
            'oh',
            'ss',
            'presentationqty',
            'intransin',
            'promoid',
            'u_sourcing',
            'majorshipqty',
            'altconstrcovdur',
            'arrivdate',
            'loadid',
            'saporderid',
            'lt',
            'qty_log',
            'mustgoqty',
            'recqty',
            'totdmd1',
            'totdmd2',
            'maxss',
            'noz',
            'push',
            'cz',
            'sales_sum',
            'sg',
            'altconstrpoh'
        ]

        filtered_report_df = report_df[selected_columns]

        # def format_dates(filtered_report_df):
        #     for row in filtered_report_df:
        #         # Преобразуем 'inventorydate'
        #         if 'inventorydate' in row and row['inventorydate']:
        #             date_object = datetime.strptime(row['inventorydate'], '%Y-%m-%d')
        #             row['inventorydate'] = date_object.strftime('%d.%m.%Y')
        #
        #         # Преобразуем 'push'
        #         if 'push' in row and row['push']:
        #             date_object = datetime.strptime(row['push'], '%Y-%m-%d')
        #             row['push'] = date_object.strftime('%d.%m.%Y')
        #
        #     return filtered_report_df

        # formatted_data = format_dates(filtered_report_df)

        translation_dict = {
            'inventorydate': 'Дата расчёта',
            'source': 'Источник',
            'loc': 'Получатель',
            'item': 'Товар',
            'sscov': 'СВ',
            'oh': 'Остаток',
            'ss': 'СЗ',
            'presentationqty': 'ПЗ',
            'intransin': 'ТВП',
            'promoid': 'РМ',
            'u_sourcing': 'ЦП',
            'majorshipqty': 'Квант',
            'altconstrcovdur': 'ТЗ в днях',
            'arrivdate': 'Дата поставки',
            'loadid': 'BTL',
            'saporderid': '№ заказа в SAP',
            'lt': 'LT',
            'qty_log': 'Фактически заказано',
            'mustgoqty': 'Заказ',
            'recqty': 'Рекомендация к заказу',
            'totdmd1': 'Прогноз от заказа до поставки',
            'totdmd2': 'Прогноз от поставки до поставки',
            'maxss': 'Максимальный СЗ',
            'noz': 'НОЗ',
            'push': 'Правило Push',
            'cz': 'ЦЗ',
            'sales_sum': 'Продано',
            'sg': 'СГ',
            'altconstrpoh': 'Остаток на конец дня (прогнозный)'
        }

        filtered_report_df.rename(columns=translation_dict, inplace=True)

        context = {
            'report': filtered_report_df.to_html(index=False)
        }

        return context

    def post(self, request, *args, **kwargs):
        store = request.POST.get('store', '')
        item = request.POST.get('item', '')
        date_from = request.POST.get('date_from', '')
        date_to = request.POST.get('date_to', '')

        report_data = self.generate_report_data(store, item, date_from, date_to)

        return self.get_csv(report_data)

    def get_csv(self, report_data):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)

        if report_data:
            headers = report_data[0].keys()
            writer.writerow(headers)

            for row in report_data:
                writer.writerow(row.values())
        else:
            writer.writerow(['Нет данных для выгрузки'])

        return response

