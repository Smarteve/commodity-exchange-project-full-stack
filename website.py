import web
from common.helper import (
    is_valid_username_password,
    is_valid_username,
    add_user,
    get_exchange_list,
)
import forms

urls = (
    "/",
    "Login",
    "/createuser",
    "CreateUser" "/selectexchange",
    "SelectExchange",
    "/selectassettype",
    "SelectAssetType" "/selectasset",
    "SelectAsset",
    "/addasset",
    "AddAsset",
    "/deleteasset",
    "DeleteAsset",
)

web.config.debug = False
render = web.template.render("templates/")
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"))


class Login:
    def GET(self):
        form = forms.login_form()
        return render.login_form(login_template)

    def POST(self):
        form = forms.login_form()
        i = form.d
        if is_valid_username_password(i.username, i.password):
            session.username = i.username
            session.logged_in = True
            raise web.seeother("/selectexchange")
        else:
            return "username or password does not exist"


class CreateUser:
    def GET(self):
        form = forms.create_user_form()
        return render.create_user_template(form)

    def POST(self):
        form = forms.create_user_form()
        if not form.validates():
            return render.create_user_template(form)
        i = form.d
        if is_valid_username(i.username):
            add_user(i.username, i.password)
            print("user created successfully")
            raise web.seeother("/")
        else:
            return "username already existed"


class SelectExchange:
    def GET(self):
        exchange_list = get_exchange_list()
        return render.select_exchange_html(exchange_list)
    
class SelectAssetType:
    def GET(self):
        data = web.input()
        exchange = data.exchange
        asset_types = ["commodity","currency"]
        return render.select_asset_type_template(exchange, asset_types)
class SelectAsset:
    


if __name__ == "__main__":
    app.run()
