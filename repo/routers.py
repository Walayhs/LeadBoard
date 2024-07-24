# # repo/routers.py

# class MultiDBRouter:
#     def db_for_read(self, model, **hints):
#         """
#         Directs read operations to the appropriate database.
#         """
#         return 'default'

#     def db_for_write(self, model, **hints):
#         """
#         Directs write operations to the appropriate database.
#         """
#         return 'default'  # Use 'postgres' if you want to write to PostgreSQL

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allows relations between models in different databases.
#         """
#         return True

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Migrate only on the default database.
#         """
#         return db == 'default'
