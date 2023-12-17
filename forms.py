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
