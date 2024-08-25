from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import admin, db
from app.models import Birthday, User


class UserAdminView(ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password_hash',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password_hash',)

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.is_authenticated
    
class BirthdayAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(UserAdminView(User, db.session))
admin.add_view(BirthdayAdminView(Birthday, db.session))
