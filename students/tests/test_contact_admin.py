from django.core import mail
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
# from django.test import override_settings

class ContactAdminFormTests(TestCase):

	fixtures = ['students_test_data.json']

	# @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
	def test_email_sent(self):
		"""Check if email is being sent"""
		# prepare client and login as administrator
		client = Client()
		client.login(username='admin', password='admin')

		# make from submit
		response = client.post(reverse('contact_admin'), {
			'email': 'from@gmail.com',
			'name': 'sender name',
			'body': 'test email message'
			})

		# check if test email backend catched our email to admin
		msg = mail.outbox[0].message()
		message = msg.get_payload().split('\n')
		# check subject 
		self.assertEqual(msg.get('subject'), 'message from sender name')
		# check name field
		self.assertEqual(message[0], 'sender name')
		# check email field
		self.assertEqual(message[1], u'from@gmail.com')
		# check body field
		self.assertEqual(message[2], 'test email message',)
