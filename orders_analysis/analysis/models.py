from django.db import models

class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return self.author


# Session = sessionmaker(bind=engine)

# class Report(models.Model):
#     store = models.CharField(max_length=4)
#     item = models.CharField(max_length=10)
#     date_from = models.DateField()
#     date_to = models.DateField()
#
#     @classmethod
#     def get_inventory_data(cls, store, item, date_from, date_to):
#         with Session() as session:
#             result = session.execute(text(GET_INVENTORY_DATA), {
#                 'store': store,
#                 'item': item,
#                 'date_from': date_from,
#                 'date_to': date_to
#             })
#             return result.fetchall()
#
#     @classmethod
#     def get_recommendation_data(cls, store, item, date_from, date_to):
#         with Session() as session:
#             result = session.execute(text(GET_RECOMMENDATION_DATA), {
#                 'store': store,
#                 'item': item,
#                 'date_from': date_from,
#                 'date_to': date_to
#             })
#             return result.fetchall()
#
#     @classmethod
#     def get_sourcing_data(cls, store, item):
#         with Session() as session:
#             result = session.execute(text(GET_SOURCING_DATA), {
#                 'store': store,
#                 'item': item
#             })
#             return result.fetchall()
#
#     @classmethod
#     def get_sku_data(cls, store, item):
#         with Session() as session:
#             result = session.execute(text(GET_SKU_DATA), {
#                 'store': store,
#                 'item': item
#             })
#             return result.fetchall()
#
#     @classmethod
#     def get_sales_data(cls, store, item, date_from, date_to):
#         with Session() as session:
#             result = session.execute(text(GET_SALES_DATA), {
#                 'store': store,
#                 'item': item,
#                 'date_from': date_from,
#                 'date_to': date_to
#             })
#             return result.fetchall()
#
#     @classmethod
#     def get_item_data(cls, item):
#         with Session() as session:
#             result = session.execute(text(GET_ITEM_DATA), {
#                 'item': item
#             })
#             return result.fetchall()
#
#     @classmethod
#     def get_closed_cash_data(cls, store, item, date_from, date_to):
#         with Session() as session:
#             result = session.execute(text(GET_CLOSED_CASH_DATA), {
#                 'store': store,
#                 'item': item,
#                 'date_from': date_from,
#                 'date_to': date_to
#             })
#             return result.fetchall()
#
#
#
