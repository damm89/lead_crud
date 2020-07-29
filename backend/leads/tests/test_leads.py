from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from leads.models import Lead
from leads.serializers import LeadSerializer

LEADS_URL = reverse('leads:lead-list')

def get_lead_url(lead_id):
    """
    Get the URL for the Lead with id <lead_id>
    """
    return reverse('leads:lead-detail', args=[lead_id])

class PublicIngredientsApiTests(TestCase):
    """
    Test the public leads API
    """

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """
        Test that login is always required
        """
        response = self.client.get(LEADS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTests(TestCase):
    """
    Test the private leads api
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='hello1',
            email='test@test.com',
            password='hello',
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_leads_list(self):
        """
        Test retrieving list of leads
        """
        Lead.objects.create(
                created_by=self.user, 
                name='John Doe',
            )
        
        response = self.client.get(LEADS_URL)

        leads = Lead.objects.all().order_by('-name')
        serializer = LeadSerializer(leads, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_user_can_see_all_leads(self):
        """
        Test if user can see all leads
        """
        other_user = get_user_model().objects.create_user(
            name='hello2',
            email='test2@test.com',
            password='hello',
        )
        lead_other = Lead.objects.create(name='John Doe', created_by=other_user)
        lead_mine = Lead.objects.create(name='Jane Doe', created_by=self.user)

        response = self.client.get(LEADS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(set([response.data[0]['name'], response.data[1]['name']]), set([lead_mine.name, lead_other.name]))

    def test_create_lead_successful(self):
        """
        Test create a lead
        """
        payload = {'name': 'Jane Doe'}
        self.client.post(LEADS_URL, payload)

        exists = Lead.objects.filter(
            created_by = self.user,
            name = payload['name'],
        ).exists()
        self.assertTrue(exists)
    
    def test_create_lead_invalid(self):
        """
        Test creating an invalid lead fails
        """
        payload = {'name': ''}
        response = self.client.post(LEADS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_view_lead_detail(self):
        """
        Test viewing lead detail
        """
        lead = Lead.objects.create(
                name='Jane Doe',
                credit_score=800,
                created_by=self.user,
            )
        url = get_lead_url(lead.id)
        response = self.client.get(url)
        serializer = LeadSerializer(lead)
        self.assertEqual(response.data, serializer.data)

    def test_patch_own_lead(self):
        """
        Test updating lead created_by user
        """
        lead = Lead.objects.create(
                name='Jane Doe',
                credit_score=800,
                created_by=self.user,
            )

        payload = {'credit_score': 750}
        self.client.patch(get_lead_url(lead.id), payload)

        lead.refresh_from_db()
        self.assertEqual(lead.credit_score, payload['credit_score'])
    
    def test_put_own_lead(self):
        """
        Test updating lead created_by user
        """
        lead = Lead.objects.create(
                name='Jane Doe',
                credit_score=800,
                created_by=self.user,
            )

        payload = {'name': 'John Doe',
                    'credit_score': 750}

        self.client.put(get_lead_url(lead.id), payload)

        lead.refresh_from_db()
        self.assertEqual(lead.credit_score, payload['credit_score'])
        self.assertEqual(lead.name, payload['name'])

    def test_patch_other_lead(self):
        """
        Test updating lead created_by user
        """
        other_user = get_user_model().objects.create_user(
            name='hello2',
            email='test2@test.com',
            password='hello',
        )

        lead = Lead.objects.create(
                name='Jane Doe',
                credit_score=800,
                created_by=other_user,
            )

        payload = {'credit_score': 750}
        response = self.client.patch(get_lead_url(lead.id), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_other_lead(self):
        """
        Test updating lead created_by user
        """
        other_user = get_user_model().objects.create_user(
            name='hello2',
            email='test2@test.com',
            password='hello',
        )

        lead = Lead.objects.create(
                name='Jane Doe',
                credit_score=800,
                created_by=other_user,
            )

        payload = {'credit_score': 750}
        response = self.client.put(get_lead_url(lead.id), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
