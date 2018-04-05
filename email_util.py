import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import traceback


class EmailUitl:

    # 初始化一些类变量
    sender = 'lirui_gydx@sina.com'
    password = ''
    receiver_list = None
    msg_root = MIMEMultipart('relate')
    msg_root['From'] = sender
    msg_root['Date'] = formatdate(localtime=True)
    mime_type = {
        'text/css': 'css',
        'html': 'htm,html',
        'text/plain': 'txt,bas',
        'image/gif': 'gif',
        'image/x-icon': 'ico',
        '如果还有找不到的请百度搜索:"MIME type"': ''
        }

    # 添加附件（此方法可解决outlook乱码的问题）
    @classmethod
    def add_app(cls, filename):
        att = MIMEApplication(open(filename, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename.split('/')[-1]))
        cls.msg_root.attach(att)

    # 添加文件正文内容
    @classmethod
    def add_content(cls, content, mime_type='html;css', _encode='gbk'):
        message = MIMEText(content, mime_type, _encode)
        cls.msg_root.attach(message)

    # 设置邮件头
    @classmethod
    def set_mail_header(cls, subject, receiver_list, cc_list=[], bcc_list=[]):
        cls.msg_root['Subject'] = subject
        cls.msg_root['To'] = ';'.join(receiver_list)
        cls.msg_root['Cc'] = ';'.join(cc_list)
        cls.msg_root['Bcc'] = ';'.join(bcc_list)
        cls.receiver_list = receiver_list + cc_list + bcc_list

    # 所有内容都提前配置好之后调用此方法
    @classmethod
    def send(cls):
        try:
            assert(cls.msg_root['Subject'])
            smtp = smtplib.SMTP()
            print('初始化服务完毕')
            smtp.connect('smtp.sina.com')
            print('连接到服务')
            smtp.login(cls.sender, cls.password)
            print('登录成功')
            smtp.sendmail(cls.sender, cls.receiver_list, cls.msg_root.as_string())
            print('发送成功')
        except Exception as e:
            print('发送失败，错误原因为：%s' % e)
            print(traceback.format_exc())
        finally:
            cls.msg_root = MIMEMultipart('relate')
            cls.receiver_list = None


if __name__ == '__main__':
    # 附件文件路径
    _filename = 'C:/Users/Administrator/Desktop/requirements.txt'
    # 邮件主题
    _subject = '我的邮件类'
    # 邮件正文
    _content = '12312313'
    # 收件人
    _receiver_list = ['lirui-pbj@hfax.com']
    # 抄送人员
    _cc_list = ['lirui-pbj@hfax.com']
    # 暗送人员
    _bcc_list = ['lirui-pbj@hfax.com']

    # 邮件添加附件
    EmailUitl.add_app(_filename)
    # 邮件添加正文
    EmailUitl.add_content(content=_content, mime_type='html', _encode='utf-8')
    # 邮件设置发送头信息（头信息包含主题，收件人，抄送人，暗送人）
    EmailUitl.set_mail_header(subject=_subject, receiver_list=_receiver_list, cc_list=_cc_list, bcc_list=_bcc_list)
    # 发送邮件
    EmailUitl.send()

