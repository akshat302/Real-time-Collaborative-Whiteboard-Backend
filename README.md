# SuperU-Backend
### Requirements

- Django==4.1.3
- daphne==4.0.0
- channels==4.0.0
- djangorestframework==3.14.0
- cryptography==41.0.3

### Steps to run

1. clone the github repo - git clone https://github.com/akshat302/SuperU-Backend.git
2. cd into the SuperU-Backend folder - cd SuperU-Backend/boardhouse
3. run python manage.py migrate in the terminal.
4. run python manage.py runserver in the terminal to run the server.
5. To run test corresponding to the API's run `python manage.py test` in the terminal.

### Entities 

1. User
2. WhiteBoard
3. UserBoardInformation

### Database Models

UserInformation:

	uuid: unique identity of each whiteboard
	name: name of the whiteboard
	description: about the whiteboard
	created_at: timestamp at which the whiteboard is created

UserBoardInformation

  	user: ForeignKey to the user model
    board: ForeignKey to the whiteboard model
    action: Action performed on that particular whiteboard by the particular user
    undo: status whether the action has been undo or redo
    created_at: timestamp at which the entry is created
    updated_at: timestamp at which the undo entry is updated

### API Details 

register_user -

    URL - "http://127.0.0.1:8000/register/"
    Type - POST
    Request Body - {
                    "username": "akk",
                    "password": "ak@123456789",
                    "email": "ak@test.com",
                    "first_name": "akshat",
                    "last_name": "gupta"
                  }
    Description: 
      1. Allows the users to successfully register.
    Response -    {
                  "message": "User registered successfully"
                  }

login - 
    
    URL - "http://127.0.0.1:8000/login/"
    Type - POST
    Request Body - {
                    "username": "akk",
                    "password": "ak@123456789"
                    }
    Description :
      1. Allows the user to login to the website
      2. Generates an authentication token for the user currently logged in

    Response - {
                "token": "35f12dfc24fad92df1442769d64b0fcef9ee3738",
                "username": "akk"
                }

create_whiteboard - 

    URL - "http://127.0.0.1:8000/create_whiteboard/"
    Type - POST
    Headers - {
              "Authentication" : "Token {token_value}"
              }  
    Request Body - {
                    "name": "notes",
                    "description": "Used for notes"
                    }
          
    Description :
      1. Allows an authenticated user to create a whiteboard
      2. Generates a unique uuid for each whiteboard
      
    Response - {
                "message": "White Board Created Successfully",
                "uuid": "917c3ab9-dda6-451c-a92c-9f66db47320c"
                }

list_all_boards - 

    URL - "http://127.0.0.1:8000/list_all_boards/"
    Type - GET
    Headers - {
              "Authentication" : "Token {token_value}"
              }  

    Description : 
      1. Lists all the whiteboards created till now and their details
      
    Response - {
                   {
                      "name": "My_whiteboard",
                      "description": "Used for drawing sketches",
                      "created_at": "2023-08-20T18:19:22.405914Z"
                    },
                    {
                      "name": "notes",
                      "description": "Used for notes",
                      "created_at": "2023-08-20T18:24:12.980299Z"
                    }
                }

  list_board - 

    URL - "http://127.0.0.1:8000/list_board/"
    Type - GET
    Headers - {
              "Authentication" : "Token {token_value}"
              }  
    Request Params - {
                    "board_uuid":"917c3ab9-dda6-451c-a92c-9f66db47320c"
                  }
    Description : 
      1. Lists the specific whiteboard details for a given whiteboard uuid
      
    Response - {
                "name": "notes",
                "description": "Used for notes",
                "created_at": "2023-08-20T18:24:12.980299Z"
                }

  list_all_actions - 

    URL - "http://127.0.0.1:8000/list_all_actions"
    Type - GET
    Headers - {
              "Authentication" : "Token {token_value}"
              }  
    Request Params - {
                    "board_uuid":"917c3ab9-dda6-451c-a92c-9f66db47320c"
                  }
    Description : 
      1. Lists all the actions performed on that specific whiteboard uuid
      
    Response - [
                  {
                      "username": "admin",
                      "board": "notes",
                      "action": "start",
                      "undo_status": false
                  },
                  {
                      "username": "admin",
                      "board": "notes",
                      "action": "draw-line",
                      "undo_status": false
                  },
                  {
                      "username": "admin",
                      "board": "notes",
                      "action": "draw-shape",
                      "undo_status": true
                  }
              ]
logout - 
    
    URL - "http://127.0.0.1:8000/logout/"
    Type - GET
    Headers - {
              "Authentication" : "Token {token_value}"
              }  
 
    Description :
      1. Allows the user to logout successfully
    
    Response - {
                "message": "Logged Out Successfully"
                }


whiteboard/{board_uuid}

    URL - "ws://127.0.0.1:8000/whiteboard/917c3ab9-dda6-451c-a92c-9f66db47320c"
    Type - WebSocket

 
    Description :
      1. Establishes WebSocket Connection and broadcast actions to all the user present in the room. 
