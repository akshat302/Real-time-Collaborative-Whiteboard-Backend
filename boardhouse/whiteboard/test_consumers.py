from whiteboard.consumers import WhiteBoardConsumer
from channels.testing import WebsocketCommunicator
from whiteboard.models import WhiteBoard, UserBoardInformation
from django.contrib.auth.models import User
from django.test import TestCase
from channels.routing import URLRouter
from django.urls import re_path
from channels.db import database_sync_to_async


class WhiteBoardConsumerTestCase(TestCase):
    def set_up_data(self): 
        self.user = User.objects.create_user(username='akshat', password='ak@123')
        self.board = WhiteBoard.objects.create(name='my_board', description='Personal Work')

    async def test_consumer_connect(self):
        communicator = self.get_communicator()
        communicator.scope['user'] = self.user
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_consumer_receive_action(self):
        communicator = self.get_communicator()
        communicator.scope['user'] = self.user
        await communicator.connect()

        action_data = {
            'action': 'draw-line',
        }
        await communicator.send_json_to(action_data)

        response = await communicator.receive_json_from()
        user_board_info = self.get_user_board_info()
        self.assertIsNotNone(user_board_info)
        self.assertEqual(response['action'], action_data['action'])

        await communicator.disconnect()

    def get_communicator(self):
        application = URLRouter([re_path(r'^whiteboard/(?P<board_id>[0-9a-f\-]{32,})$', WhiteBoardConsumer.as_asgi())])
        return WebsocketCommunicator(application, f"/whiteboard/{self.board.uuid}")

    @database_sync_to_async
    def get_user_board_info(self):
        user_board_info = UserBoardInformation.objects.filter(user=self.user, board=self.board).first()
        return user_board_info