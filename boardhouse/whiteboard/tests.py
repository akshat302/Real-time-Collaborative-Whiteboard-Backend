from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from whiteboard.models import WhiteBoard, UserBoardInformation

class WhiteBoardViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login') 
        self.create_board_url = reverse('create_whiteboard')
        self.list_all_boards = reverse('list_all_boards')
        self.list_board = reverse('list_board')
        self.list_all_actions = reverse('list_all_actions')
        self.logout_url = reverse('logout')

    def create_user_and_token(self):
        user = User.objects.create_user(username='akshat', password='akshat_123')
        token = Token.objects.create(user=user)
        return user, token

    def test_register_user(self):

        user_data = {
                "username": "akshat",
                "password": "ak@123456789",
                "email": "ak@test.com",
                "first_name": "akshat",
                "last_name": "gupta"
            }
        
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, user_data["username"])
        
        user_data = {}

        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):

        user_data = {
                "username": "akshat",
                "password": "ak@123456789",
                "email": "ak@test.com",
                "first_name": "akshat",
                "last_name": "gupta"
            }
        
        login_data = {
                "username": "akshat",
                "password": "ak@123456789"
            }
        
        User.objects.create_user(**user_data)
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['username'], user_data['username'])

    def test_create_board_authenticated(self):
        user, token = self.create_user_and_token()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        board_data = {
                "name": "notes",
                "description": "Used for daily notes"
            }

        response = self.client.post(self.create_board_url, board_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        board = WhiteBoard.objects.first()
        self.assertIsNotNone(board)
        self.assertEqual(board.name, board_data["name"])

    def test_list_all_boards_view(self):
        user, token = self.create_user_and_token()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        board_data_1 = {
                "name": "notes",
                "description": "Used for daily notes"
            }
        board_data_2 = {
                "name": "sketches",
                "description": "Used for drawing"
        }
        whiteboard_1 = WhiteBoard.objects.create(**board_data_1)
        whiteboard_2 = WhiteBoard.objects.create(**board_data_2)

        response = self.client.get(self.list_all_boards, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_list_all_actions_view(self):

        user, token = self.create_user_and_token()
        board = WhiteBoard.objects.create(name='notes', description='to write daily notes')
        user_board_info = UserBoardInformation.objects.create(user=user, board=board, action='write-text')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(self.list_all_actions, {'board_uuid': str(board.uuid)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_logout_user(self):
        user, token = self.create_user_and_token()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
