from django.test import TestCase, Client
from django.core import mail
from django.contrib.messages import get_messages
from django.urls import reverse
from .models import Client as ClientModel
from django.contrib.auth.models import User
from veterinary.models import Veterinary
from veterinary.models import User
from .models import Events
from veterinary.models import Pet




class SendEmailTestCase(TestCase):
    def test_send_email_envio(self):
        data = {
            'email': 'example@example.com',
            'Nombre': 'Freddo Romero',
            'message': 'Mensaje de prueba',
        }
        response = self.client.post(reverse('send_email'), data)
        
        self.assertEqual(response.status_code, 302)  # Verificar redireccionamiento
        self.assertRedirects(response, reverse('support'))  # Verificar redireccionamiento a la vista 'support'

        self.assertEqual(len(mail.outbox), 1)  # Verificar si se envió un correo
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'Solicitud de Soporte')  # Verificar asunto del correo
        self.assertIn('Hola, Freddo Romero', sent_email.body)  # Verificar contenido del correo
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Verificar si se muestra un mensaje de éxito
        self.assertEqual(str(messages[0]), 'La solicitud fue enviada correctamente')  # Verificar el contenido del mensaje de éxito

    def test_send_email_faltantes(self):
        data = {
        'email': '',  # Valor faltante
        'Nombre': 'Freddo Romero',
        'message': 'Mensaje de prueba',
    }
        response = self.client.post(reverse('send_email'), data)
    
        self.assertEqual(response.status_code, 302)  # Verificar que la respuesta tenga un código de estado válido

    def test_send_email_contenido(self):
        data = {
            'email': 'example@example.com',
            'Nombre': 'Freddo Romero',
            'message': 'Mensaje de prueba',
        }
        self.client.post(reverse('send_email'), data)
        
        sent_email = mail.outbox[0]
        self.assertIn('Hola, Freddo Romero', sent_email.body)  # Verificar contenido del correo
        self.assertIn('Puedes contactarlo a través de su correo electrónico: example@example.com', sent_email.body)  # Verificar contenido del correo

    def test_send_email_destinatario(self):
        data = {
            'email': 'example@example.com',
            'Nombre': 'Freddo Romero',
            'message': 'Mensaje de prueba',
        }
        self.client.post(reverse('send_email'), data)
        
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.to, ['godofreddo017@gmail.com'])  # Verificar destinatario del correo

    def test_send_email_error_interno(self):
    # Simular una configuración incorrecta del correo (por ejemplo, email_host_user incorrecto)
        with self.settings(EMAIL_HOST_USER='incorrect_host_user'):
            data = {
            'email': 'example@example.com',
            'Nombre': 'Freddo Romero',
            'message': 'Mensaje de prueba',
        }
            response = self.client.post(reverse('send_email'), data)
        
            self.assertEqual(response.status_code, 302)  # Verificar que la respuesta tenga un código de estado válido


class RegisterVetTestCase(TestCase):
    def test_register_vet_success(self):
        url = reverse('registerVet')
        data = {
            'nameVeterinary': 'Veterinary',
            'email': 'test@example.com',
            'nit': '123456789',
            'password': 'test123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Verificar redirección
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Veterinary.objects.count(), 1)  # Verificar creación de Veterinary
        self.assertEqual(User.objects.count(), 1)  # Verificar creación de User

    def test_register_vet_existing_name(self):
        # Preparar datos de prueba
        Veterinary.objects.create(nameVeterinary='ExistingVet')
        url = reverse('registerVet')
        data = {
            'nameVeterinary': 'ExistingVet',
            'email': 'test@example.com',
            'nit': '123456789',
            'password': 'test123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Verificar respuesta exitosa
        form = response.context['form']
        self.assertTrue(form.has_error('nameVeterinary'))  # Verificar error de nombre de veterinaria existente


class RegisterDateTestCase(TestCase):
    def setUp(self):
        self.veterinary = Veterinary.objects.create(nameVeterinary='Test Veterinary', cityVeterinary='bello', nit='122345', email='prueba@prueba.com', direccion='av 47c', password='123456')
        self.client_instance = ClientModel.objects.create(veterinary=self.veterinary, name='Freddo', last_name='Romero', document='34567', email='caso@caso.com', phone='5976461')
        self.client = Client()
        doctor_user = User.objects.create(username='freddo')
        self.pet = Pet.objects.create(client=self.client_instance, namePet='Scoby', species='gato', birthdate='2022-05-12', gender='masculino')
        # Configurar datos de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.veterinary_logued = self.user.veterinary
        self.event = Events.objects.create(name='Test Event', start='2023-05-25 22:00:00', end='2023-05-25 23:00:00', doctor=doctor_user, pet=self.pet)
        
    def test_render_page(self):
        # Prueba de renderizado de la página
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('registerDate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veterinary/registerDate.html')

    def test_submit_valid_form(self):
        # Prueba de envío de formulario válido
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': 'New Event',
            'start': '2023-05-26 09:00:00',
            'end': '2023-05-26 10:00:00',
        }
        response = self.client.post(reverse('registerDate'), data=form_data)
        self.assertEqual(response.status_code, 200)
        # Verificar si se crea una nueva cita en la base de datos
        self.assertEqual(Events.objects.count(), 1)

    def test_submit_invalid_form(self):
        # Prueba de envío de formulario inválido
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': '',
            'start': '2023-05-26 09:00:00',
            'end': '2023-05-26 10:00:00',
        }
        response = self.client.post(reverse('registerDate'), data=form_data)
        self.assertEqual(response.status_code, 200)
        

        
    def test_load_existing_data(self):
        # Prueba de carga de datos existentes
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('registerDate'))
        self.assertEqual(response.status_code, 200)

