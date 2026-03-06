# Connectly API Project

## Table of Contents
- About the Project
- Key Features
- System Architecture
- Design Patterns
- API Endpoints
- Tech Stack
- System Diagrams

## About the Project

**Description**:
- This is the backend API for the social media called Connectly. It utilizes Django 6.0 and Django REST Framework (DRF), factories, and Google OAuth integration.


## Key Features:
- Factory Pattern Architecture: Decouples object creation from the view logic for Posts, Comments, and Likes.
- Singleton Layer: A centralized configuration and logging services.
- Feed System: Annotated query providing real-time metrics such as Likes and Comments, and a filter function.
- Secure Authentication: 2-Layer security utilizing Google OAuth and DRF Token authentication.
- RBAC: Object-level permissions ensuring users can only edit or delete their own posts.


## System Architecture:
- The system uses a layered approach where the Token Authentication protects the Views, and the system logic with RBAC. The logic is assigned to the Factories, and the global configurations with Singletons.  
![alt text](<docs/IPT Diagrams (Connectly) - System Architecture Diagram.png>)


## Design Patterns:
**Factory Pattern**  
Used to centralize entity creation.
- PostFactory: Handles creation of posts.
- CommentFactory: Handles post comments.
- LikeFactory: Handles post likes toggle.
  
**Singleton Pattern**  
Ensures resource efficiency and global consistency.  
- ConfigManager: Manages global settings.
- LoggerSingleton: Provides a standardized logs format for the system.
  
## API Endpoints  
**Users and Authentication**
| Endpoint     |  Method  |                   Description |
| :----------- | :------: | ----------------------------: |
| /users/      | POST/GET | User Registration and Listing |
| /users/id/   |   GET    |                  User Profile |
| auth/google/ |   POST   |            Google OAuth Login |
  
**Social Resources**
| Resource |      Create(POST)       | Read/Update/Delete(GET/PUT/DEL) |
| :------- | :---------------------: | ------------------------------: |
| Post     |     /posts/create/      |                  /posts/postid/ |
| Comments | /posts/comments/create/ |      /posts/comments/commentid/ |
| Likes    |  /posts/postid/likes/   |            /posts/postid/likes/ |

**Feed and Filters**
| Resource                |            Read(GET)             |                           Description |
| :---------------------- | :------------------------------: | ------------------------------------: |
| Feed                    |           /posts/feed/           |                         Get all posts |
| Comment Filter by User  | /posts/feed/?commented_by=userid |        Get posts commented by user id |
| Likes Filter by User    |   /posts/feed/?liked_by=userid   |            Get posts liked by user id |
| Filter by Comment Count | /posts/feed/?min_comment_count=# | Filter posts by minimum comment count |
| Filter by Like Count    |  /posts/feed/?min_like_count=#   |    Filter posts by minimum like count |


## Tech Stack  
**Framework**: 
- Django 
- Django REST Framework
    
**Patterns**: 
- Factory 
- Singleton 
- Serializer  
  
**Database**: 
- SQLite

**Requirements**:
pip install django
pip install djangorestframework  
pip install django-extensions  
pip install django-allauth
pip install dj-rest-auth
pip install requests
pip install PyJWT
pip install cryptography  
pip install Werkzeug    
pip install pyOpenSSL        
pip install django-sslserver


## System Diagrams
**Data Relationship Diagram**
![alt text](<docs/IPT Diagrams (Connectly) - Data Relationship Diagram.png>)  
**CRUD Interaction Flow Diagram**
![alt text](<docs/IPT Diagrams (Connectly) - CRUD Interaction Flow Diagram.png>)  
**Authentication and Authorization Flow Diagram**
![alt text](<docs/IPT Diagrams (Connectly) - Authentication and Authorization Flow Diagram.png>)  
