import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from whiteboard.models import UserBoardInformation, WhiteBoard
from django.db import transaction

class WhiteBoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['board_id']
        self.room_group_name = f'group_{self.room_name}'
        user = self.scope['user']

        if user.is_authenticated: 
            await self.channel_layer.group_add(
                self.room_group_name, 
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)
        user = self.scope['user']
        action = data['action']

        if self.is_valid_action(action):

            await self.save_action(user, data['action'], uuid.UUID(self.room_name))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_action',
                    'data': data,
                    'sender_channel_name': self.channel_name
                }
            )

    async def broadcast_action(self, event):        
        await self.send(text_data=json.dumps(event['data']))

    def is_valid_action(self, action):
        ACTIONS = ['start', 'draw-line', 'draw-shape', 'write-text', 'stop', 'undo', 'redo']
        return action in ACTIONS

    # Used @database_sync_to_async so that db operation does bot block the websocket connection
    # One drawback would be that is some error occurs during saving the booard_information it would still continue to broadcast the actions to the connected users.
    # Adding a retry to this method would be a probable solution
    @database_sync_to_async
    def save_action(self, user, action, board_uuid):

        with transaction.atomic():
            try:
                board = WhiteBoard.objects.filter(uuid=board_uuid).first()
                if board is not None:
                    if action == 'undo':
                        undo_entry = UserBoardInformation.objects.select_for_update().filter(board=board, undo=False).order_by('-created_at').first()
                        if undo_entry:
                            undo_entry.undo = True
                            undo_entry.save()
                    elif action == 'redo':
                        redo_entry = UserBoardInformation.objects.select_for_update().filter(board=board, undo=True).order_by('created_at').first()
                        if redo_entry:
                            redo_entry.undo = False
                            redo_entry.save()
                    else:
                        user_board = UserBoardInformation.objects.create(user=user, board=board, action=action)
            except Exception as e:
                raise e