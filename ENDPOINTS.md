# InternalInterviewService
This application is a file storage and management platform that helps you organize everything you need to get that job you've always wanted.

The goal of this application is to make it easier for a user to keep track of everything during their job search and to give tips and pointers on how to end their job search and finally land a job.

*InternalInterviewService is an Application Programming Interface (API) built using Django Rest Framework (DRF)
All requests require authentication.
## Base URL:
All endpoints begin with `https://meercat-question-box.onrender.com/`
NOTE: API Root is /api/
|  Method  |  Endpoint  |  Description |
| -------- | ---------- | ------------ |
|POST|[/auth/users/](#create-a-new-user)|Create a new user|
|POST|[/auth/token/login/](#login-user)|Login user|
|POST|[/auth/users/me/](#users-info)|User's info|
|GET|[auth/users/](#all_users)|List of all users|
|POST|[/auth/token/logout/](#logout-user)|Logout user|
|GET|[api/questions/](#list-of-all-questions)|returns a list of all questions|
|GET|[api/questions/{pk}/](#details-of-one-question)|details of one question|
|POST|[api/questions/](#create-a-question)|create a question|
|PATCH|[api/questions/{pk}/](#update-a-question)|update a question|
|DELETE|[api/questions/{pk}/](#delete-a-question)|delete a question|
|GET|[api/questions?search=<search_term>](#search-questions)|search question title and text|
|GET|[api/questions/{pk}/answers?search=<search_term>](#search-answers)|search answer text|
|GET|[api/questions/<int:question_pk>/answers/](#list-answers-per-question)|list answers per question|
|POST|[api/questions/<int:question_pk>/answers/](#create-answer)|create answer|
|GET|[api/user/<int:user_pk>/questions/](#user-questions)|user questions|
|GET|[api/myquestions/](#my-questions)|list all of the user's questions|
|GET|[api/myfavorites/](#list-favorites)|List a user's favorite questions
|PATCH|[api/questions/<int:question_pk>/favorites/](#add-remove-favorite)|turn favorite status on/off for question
|PATCH|[api/questions/<int:question_pk>/answers/<int:pk>/accept/](#accept-answer)|accept an answer
|GET|[api/myanswers/](#my-answers)|list all of the user's answers

## Create a new user
### Request
Required fields: username and password
Optional fields: email
```json
POST auth/users/
{
  "username": "Luke",
  "password": "Momentum1"
}
```
### Response
Response: If you receive the same info you provided, user creation was successful!
```json
201 Created
{
  "email": "",
  "username": "Luke",
  "id": 4,
}
```
## Login user
### Request
Required fields: username, password
```json
POST auth/token/login/
{
    "username": "Luke",
    "password": "Momentum1"
}
```
### Response
```json
200 OK
{
    "auth_token": "d99a2de1b0a09db0fc2da23c9fdb1fc2447fff5d"
}
```
NOTE: auth_token must be passed for all requests with the logged in user. It remains active till user is [logged out](#logout-user).
## User's info
Requirement: user must be logged in.
```json
GET /auth/users/me/
```
### Response
```json
200 OK
{
    "id": 4,
    "username": "Luke",
    "email": "",
}
```
## Logout user
### Request
Required fields: None
```json
POST /auth/token/logout/
```
### Response
```json
204 No Content
```
## list of all questions
Returns list of all questions.
### Request
Required fields: None
```json
GET api/questions/
```
### Response
```json
200 OK
[
	{
		"pk": 2,
		"title": "cat",
		"created_date": "2022-11-18T02:40:58.361845Z",
		"question": "test teat test question 2",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 1,
		"title": "Dog",
		"created_date": "2022-11-18T02:40:26.456804Z",
		"question": "test test test question 1",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 3,
		"title": "bird",
		"created_date": "2022-11-18T02:41:17.312426Z",
		"question": "test question 3",
		"user": "tim",
		"total_answers": 0
	}
]
```

## details of one question
Returns detail of one question.
### Request
Required fields: None
```json
GET api/questions/<pk>/
```
### Response
```json
200 OK
{
	"pk": 2,
	"title": "cat",
	"created_date": "2022-11-18T02:40:58.361845Z",
	"question": "test teat test question 2",
	"user": "tim",
	"total_answers": 0
}
```
## create a question
create a question.
### Request
Required fields:
```json
POST api/questions/
{
	
	"title": "snake",
	"question": "test teat test question 4"
}
```
### Response
```json
201 Created
{
	"pk": 3,
	"title": "snake",
	"created_date": "2022-11-18T03:10:55.709270Z",
	"question": "test teat test question 4",
	"user": "tim"
}
```
## update a question
update a question.
### Request
Required fields:
```json
PATCH api/questions/<pk>/
{
	
	"title": "bird",
	
}
```
### Response
```json
201 Created
{
	"pk": 3,
	"title": "bird",
	"created_date": "2022-11-18T03:10:55.709270Z",
	"question": "test teat test question 4",
	"user": "tim",
	"total_answers": 0
}
```
## delete a question
delete a question.
### Request
Required fields:None
```json
DELETE api/questions/<pk>/

```
### Response
```json
204 No Content

```
## search questions
Search term in question title and text.
### Request
Required fields: None
```json
GET api/questions?search=dog
```
### Response
```json
200 OK
[
	{
		"pk": 4,
		"title": "dog",
		"created_date": "2022-11-18T03:29:04.755255Z",
		"question": "test question 5",
		"user": "tim"
	}
]
```

## search answers
Search term in answer text.
### Request
Required fields: None
```json
GET api/questions/pk/answers?search=answer
```
### Response
```json
200 OK
[
	{
		"pk": 1,
		"answer": "test answer",
		"user": "admin",
		"created_date": "2022-11-22T20:30:59.793385Z",
		"question": 1,
		"favorite": [
			1
		]
	}
]
```

## list answers per question
list answers per question
### Request
Required fields:none
```json
GET api/questions/<int:question_pk>/answers/
```
### Response
```json
200 OK
[
	{
		"pk": 2,
		"answer": "most likely",
		"user": "user1",
		"created_date": "2022-11-18T19:02:07.162097Z",
		"question": 2
	}
]
```

## create answer
create answer
### Request
Required fields:none
```json
POST api/questions/<int:question_pk>/answers/
{
		"answer": "yeehaw"
}

```
### Response
```json
201 CREATED
{
	"pk": 4,
	"answer": "yeehaw",
	"user": "user1",
	"created_date": "2022-11-18T20:09:11.196559Z",
	"question": 4
}
```

## user questions
Returns list of users questions.
### Request
Required fields: None
```json
GET api/user/<int:user_pk>/questions/
```
### Response
```json
200 OK
[
	{
		"pk": 2,
		"title": "cat",
		"created_date": "2022-11-18T02:40:58.361845Z",
		"question": "test teat test question 2",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 1,
		"title": "Dog",
		"created_date": "2022-11-18T02:40:26.456804Z",
		"question": "test test test question 1",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 3,
		"title": "bird",
		"created_date": "2022-11-18T02:41:17.312426Z",
		"question": "test question 3",
		"user": "tim",
		"total_answers": 0
	}
]
```
## my questions
Returns list of all questions for logged in user.
### Request
Required fields: None
```json
GET api/myquestions/
```
### Response
```json
200 OK
[
	{
		"pk": 2,
		"title": "cat",
		"created_date": "2022-11-18T02:40:58.361845Z",
		"question": "test teat test question 2",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 1,
		"title": "Dog",
		"created_date": "2022-11-18T02:40:26.456804Z",
		"question": "test test test question 1",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 3,
		"title": "bird",
		"created_date": "2022-11-18T02:41:17.312426Z",
		"question": "test question 3",
		"user": "tim",
		"total_answers": 0
	}
]
```
## List user favorites
Returns list of a user's favorite questions
### Request
Required fields: None
```json
GET api/myfavorites/
```
### Response
```json
200 OK
[
	{
		"pk": 2,
		"title": "cat",
		"created_date": "2022-11-18T02:40:58.361845Z",
		"question": "test teat test question 2",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 1,
		"title": "Dog",
		"created_date": "2022-11-18T02:40:26.456804Z",
		"question": "test test test question 1",
		"user": "tim",
		"total_answers": 0
	},
	{
		"pk": 3,
		"title": "bird",
		"created_date": "2022-11-18T02:41:17.312426Z",
		"question": "test question 3",
		"user": "tim",
		"total_answers": 0
	}
]
```
### add remove favorite
Turns favorite status on/off for a question
### Request
Required fields: title
```json
PATCH api/questions/<int:question_pk>/favorites/
{
  "title": "snakes"
  
}
```
```json

### Response
```json
200 OK
[
	{
		"title": "snakes"
	},
]
```

## my answers
Returns list of all questions for logged in user.
### Request
Required fields: None
```json
GET api/myanswers/
```
### Response
```json
200 OK
[
	{
	
	}

]
```