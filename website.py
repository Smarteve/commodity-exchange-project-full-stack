import web
from common.helper import (
    is_valid_username_password,
    is_valid_username,
    add_user,
    get_exchange_list,
    get_security_traded_in_exchange
)
from db_logic import view_commodity,view_currency,add_commodity,delete_commodity
import forms

urls = (
    "/",
    "Login",
    "/createuser",
    "CreateUser",
    "/selectexchange",
    "SelectExchange",
    "/selectassettype",
    "SelectAssetType",
    "/selectasset",
    "SelectAsset",
    "/viewasset",
    "ViewAsset",
    "/addasset",
    "AddCommodity",
    "/deleteasset",
    "DeleteCommodity",
)

web.config.debug = False
render = web.template.render("templates/")
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"))


class Login:
    def GET(self):
        form = forms.login_form()
        return render.login_template(form)

    def POST(self):
        form = forms.login_form()
        if not form.validates():
            return render.login_template(form)
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
        return render.select_exchange_template(exchange_list)


class SelectAssetType:
    def GET(self):
        data = web.input()
        exchange = data.exchange
        print(exchange)
        asset_types = ["commodity", "currency"]
        return render.select_asset_type_template(exchange, asset_types)


class SelectAsset:
    def GET(self):
        data = web.input()
        exchange = data.exchange
        asset_type = data.asset_type
        exchange_dict = get_security_traded_in_exchange(exchange)
        securities_list = exchange_dict[asset_type]
        return render.select_asset_template(securities_list,asset_type)
    
class ViewAsset:
    def GET(self):
        data = web.input()
        security_name = data.security 
        asset_type = data.asset_type
        if asset_type == "commodity":
            info = view_commodity(security_name)
            return "\n".join(info)
        elif asset_type == "currency":
            info = view_currency(security_name)
            return "\n".join(info)

class AddCommodity:
    def GET(self):
        form = forms.add_commodity_form() 
        return render.add_commodity_template(form)
    def POST(self):
        form = forms.add_commodity_form()
        if not form.validates():
            return render.create_user_template(form)
        i = form.d
        exchange_price_time_pairs = i.exchange_price_time_pairs.split(";")
        add_commodity(i.name,i.unit,exchange_price_time_pairs) 
        return f"adding {i.name} successfully"
    
class DeleteCommodity:
    def GET(self):
        form = forms.delete_commodity_form()
        return render.delete_commodity_tempalte(form)
    def POST(self):
        form = forms.delete_commodity_form()
        if not form.validates():
            return render.delete_commodity_template(form)
        i = form.d
        delete_commodity(i.commodity_name)
        return f"{i.commodity_name} successfully deleted"


        

                
        
  



if __name__ == "__main__":
    app.run()
