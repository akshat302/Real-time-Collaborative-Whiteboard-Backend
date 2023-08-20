import uuid

from django.contrib.auth import login, logout
from rest_framework.views import APIView   
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from whiteboard.serializers import UserSerializer, WhiteBoardSerializer, UserBoardInformationSerializer, LoginSerializer
from whiteboard.models import WhiteBoard, UserBoardInformation

# Create your views here.
class RegisterUserView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            validated_user = serializer.validated_data
            login(request, validated_user['user'])
            token, created = Token.objects.get_or_create(user=validated_user['user'])
            return Response({
                'token': token.key,
                'username': validated_user['username']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WhiteBoardCreationView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WhiteBoardSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save()
            ctx = {
                    'message': 'White Board Created Successfully',
                    'uuid': str(board.uuid)
                }
            return Response(ctx, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListAllBoardsView(APIView): 

    permission_classes = [IsAuthenticated]
    def get(self, request):

        try:
            whiteboards = WhiteBoard.objects.all()
            serializer = WhiteBoardSerializer(whiteboards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WhiteBoard.DoesNotExist:
            return Response({'error': 'whiteboard does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ListBoardView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):

        try:
            board_uuid_str = request.GET.get('board_uuid')
            board_uuid = uuid.UUID(board_uuid_str)
            board_details = WhiteBoard.objects.filter(uuid=board_uuid).first()
            white_board_serializer = WhiteBoardSerializer(board_details)
            return Response(white_board_serializer.data, status=status.HTTP_200_OK)
        except WhiteBoard.DoesNotExist:
            return Response({'error': 'whiteboard does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class ListAllActions(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):

        try:
            board_uuid_str = request.GET.get('board_uuid')
            board_uuid = uuid.UUID(board_uuid_str)
            user_board_details = UserBoardInformation.objects.filter(board__uuid=board_uuid).all()
            user_board_serializer = UserBoardInformationSerializer(user_board_details, many=True)
            action_information_list = []
            for user_board in user_board_serializer.data:
                user_board_info = {
                'username': user_board['user']['username'],
                'board': user_board['board']['name'],
                'action': user_board['action'],
                'undo_status': user_board['undo']
                }
                action_information_list.append(user_board_info)
            return Response(action_information_list, status=status.HTTP_200_OK)
        except UserBoardInformation.DoesNotExist:
            return Response({'error': 'whiteboard does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({'message': 'Logged Out Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   