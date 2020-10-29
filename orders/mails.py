from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from django.urls import reverse

class Mail:

  @staticmethod
  def get_absolute_url(url):
    if settings.DEBUG:  #En modo desarrollo
      return 'http://127.0.0.1:8000{}'.format(
        reverse(url)
      )

  @staticmethod
  def send_complete_order(orden, user):
    subject = 'Tu pedido ha sido enviado'
    # El template contiene el mensaje mque se enviará por correo
    template = get_template('orders/mails/complete.html') # Permite obtener un template
    content = template.render({
      'user': user,
      'orden': orden,
      'next_url': Mail.get_absolute_url('orders:completeds')
    })

    message = EmailMultiAlternatives(subject,
                                      'Mensaje importante',
                                      settings.EMAIL_HOST_USER,
                                      [user.email],
                                      #cc=[] #Copia a
                                    )

    message.attach_alternative(content, 'text/html')
    message.send()

