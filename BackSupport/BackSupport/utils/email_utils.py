
from flask import current_app
'''
已经在 create_app 函数中正确地配置了邮件服务，并初始化了 mail 对象。
要使邮件发送代码能够工作，你需要确保在发送邮件的函数 send_mail 中可以访问到这个 mail 对象。
由于在 create_app 函数内部初始化了 mail 对象，我们可以通过 Flask 的应用上下文来访问它
然后，修改你的 send_mail 函数，让它使用 current_app 来获取 Mail 实例并发送邮件
'''
from flask_mail import Message

def send_mail(subject, body, recipients):
    msg = Message(subject, recipients=recipients, body=body)
    # 获取当前Flask应用的实例
    mail = current_app.extensions.get('mail')
    try:
        # 使用mail对象发送邮件
        mail.send(msg)
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败:', e)