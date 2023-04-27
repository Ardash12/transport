from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.core.mail import mail_managers, mail_admins, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order


@receiver(post_save, sender=Order)
def order_signal(sender, instance, created, **kwargs):
    if created:
        if instance.senderEmail:
            # Если клиент оставил почту, отсылаем заказ
            subject = f'Заказ на доставку груза № UI0000{instance.id}'
            html_content_client= render_to_string( 
                'account/email/order_client.html',
                {
                    'appointment': instance,
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body='html_content',
                from_email=None,   # DEFAULT_FROM_EMAIL в settings.py
                to=[instance.senderEmail,],  
            )
            msg.attach_alternative(html_content_client, "text/html")  
            msg.send()  

        # Отправка заказа менеджеру
        subject = f'Новый заказ на доставку № UI0000{instance.id}'
        html_content_manager= render_to_string( 
            'account/email/order_manager.html',
            {
                'appointment': instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body='html_content',
            from_email=None,   # DEFAULT_FROM_EMAIL в settings.py
            to=[settings.DEFAULT_FROM_EMAIL,],  
        )
        msg.attach_alternative(html_content_manager, "text/html")  
        msg.send()  

