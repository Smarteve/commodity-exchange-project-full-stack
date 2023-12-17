import web

login_form = web.form.Form(
    web.form.Textbox("username", web.form.notnull),
    web.form.Textbox("password", web.form.notnull),
    web.form.Button("Submit"),
)
create_user_form = web.form.Form(
    web.form.Textbox("username", web.form.notnull),
    web.form.Textbox("password", web.form.notnull),
    web.form.Button("Creat user"),
)

add_commodity_form = web.form.Form(
    web.form.Textbox("name", web.form.notnull),
    web.form.Textbox("unit", web.form.notnull),
    web.form.Textbox("exchange_price_time_pairs",web.form.notnull,description = "trading info in the order of exchange,price and time(yyyy-mm-dd),if multiple trading info separated by ';')"),
    web.form.Button("Add Commodity"),
)

delete_commodity_form = web.form.Form(
    web.form.Textbox("commodity_name", web.form.notnull),
    web.form.Button("Delete"),
)

