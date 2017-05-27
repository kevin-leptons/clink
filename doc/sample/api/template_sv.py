from clink.service import TemplateSv
from clink.type import AppConf, AuthConf


app_conf = AppConf('dead-book', 'Hell Corporation', '1st Hell Street')

root_pwd = 'root-pwd'
root_email = 'root@email.com'
root_email_pwd = 'root-email-pwd'
root_email_server = 'smtp.email.com:578'
auth_conf = AuthConf(
    root_pwd, root_email, root_email_pwd, root_email_server,
    'jwt-key'
)

template_sv = TemplateSv(app_conf, auth_conf)

report_tpl = (
    'REPORT: MOTOCYCLE SPEC\n'
    'AUTHOR: $author\n\n'
    'Name       : $name\n'
    'Price      : $price\n'
    'Color      : $color\n'
    'Power      : $power'
)
values = {
    'author': 'Johnny Blaze',
    'name': 'Hell Cycle',
    'price': 'Not for Sale',
    'color': 'Black - Red Fire',
    'power': 'Unlimited'
}
report = template_sv.build_str(report_tpl, values)
print(report)
