import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from typing import Dict

from ..config import CONFIG
from .schema import EmailPayload


def send_email(
    email_payload: EmailPayload,
    attachment_dict: Dict[str, BytesIO] = None
):
    # 設置SMTP服務器
    smtp_setting = CONFIG.mail_server
    smtp_server = smtp_setting.smtp_server
    smtp_port = smtp_setting.smtp_port
    sender_email_name = smtp_setting.email_from
    sender_email = smtp_setting.sender_email
    sender_password = smtp_setting.sender_password

    # 創建MIMEMultipart對象以構建郵件
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email_name
    msg['To'] = ', '.join(email_payload.recipient_list)
    msg['Subject'] = email_payload.subject

    # 如果有CC，設置CC字段
    if email_payload.CC_list:
        msg['CC'] = ', '.join(email_payload.CC_list)

    # 將HTML內容轉換爲MIMEText對象
    html_part = MIMEText(email_payload.html_content, 'html')
    # 將HTML部分添加到消息中
    msg.attach(html_part)

    for filename, attachment in attachment_dict.items():
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment)
        encoders.encode_base64(part)
        encoded_filename = Header(filename, 'utf-8').encode()  # 編碼中文文件名
        part.add_header('Content-Disposition',
                        f"attachment; filename = {encoded_filename}")
        msg.attach(part)

    try:
        # 連接SMTP服務器併發送郵件
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 如果使用SSL，請省略此行
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email,
                email_payload.recipient_list,
                msg.as_string()
            )
    except smtplib.SMTPConnectError as e:
        print('郵件發送失敗，連接失敗：', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('郵件發送失敗，認證錯誤：', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('郵件發送失敗，發件人被拒絕：', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('郵件發送失敗，收件人被拒絕：', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('郵件發送失敗，數據接收拒絕：', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('郵件發送失敗, ', e.message)
