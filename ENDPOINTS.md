# InternalInterviewService
This application is a file storage and management platform that helps you organize everything you need to get that job you've always wanted.

The goal of this application is to make it easier for a user to keep track of everything during their job search and to give tips and pointers on how to end their job search and finally land a job.

*InternalInterviewService is an Application Programming Interface (API) built using Django Rest Framework (DRF)
All requests require authentication.
## Base URL:
All endpoints begin with `https://internal-interview-service.onrender.com`
NOTE: API Root is /api/
|  Method  |  Endpoint  |  Description |
| -------- | ---------- | ------------ |
|POST|[/auth/users/](#create-a-new-user)|Create a new user with email, first name, last name, codename, and password|
|DELETE|[/auth/users/me/](#delete-a-user)|Delete the current authorized user|
|POST|[/auth/token/login/](#login-user)|Login user|
|POST|[/auth/token/logout/](#logout-user)|Logout user|
|POST|[/auth/users/me/](#users-info)|User's info|
|GET|[auth/users/](#all_users)|List of all users|

## Create a new user
### Request
Required fields: username and password
Optional fields: email
```json
POST auth/users/
{
	"email":"email@example.com",
	"password":"pasword123",
	"first_name":"Lebron",
	"last_name":"James",
	"codename":"king"
}
```
### Response
Response: If you receive the same info you provided, user creation was successful!
```json
201 Created
{
	"first_name":"Lebron",
	"last_name":"James",
	"codename":"king",
	"email":"email@example.com",
	"id": 3
}
```
## Delete a user
### Request
Required fields: current password
```json
DELETE auth/users/me/
{
  "current_password": "Momentum1"
}
```
### Response
Response: If you receive the same info you provided, user creation was successful!
```json
204 No Content
```
## Login user
### Request
Required fields: username, password
```json
POST auth/token/login/
{
    "email": "email@example.com",
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
## User's info
Requirement: user must be logged in.
```json
GET /auth/users/me/
```
### Response
```json
200 OK
{
	"first_name": "Larry",
	"last_name": "Bird",
	"codename": "mycodename",
    "id": 4,
    "email": "email@example.com",
}
```