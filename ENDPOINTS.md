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
## Create a win
### Request
requirements: user must be logged in
required fields: title, win
```json
POST /wins/
{
	"title": "Example title",
	"win": "Example win",
	"occured_date": "2022-12-25"

}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"title": "Example title",
	"win": "Example win",
	"win_picture": null,
	"created_date": "2022-12-14T22:15:58.544331Z",
	"occured_date": "2022-12-25",
}
```
## Win info
### Request
Requirement: user must be logged in
```json
GET /wins/
```
### Response
```json
200 OK
{
	"pk": 1,
	"title": "Example Title",
	"win": "Example Win",
	"win_picture": "This-will-be-a-file.jpeg",
	"created_date": "2022-12-14T16:04:04.967360Z",
	"occured_date": "2022-06-29",
}
```
NOTE: This will be a list of all the users wins
## Win Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /wins/pk    Ex: /wins/1
```
### Response
```json
{
	"pk": 1,
	"title": "Example title",
	"win": "Example win",
	"win_picture": null,
	"created_date": "2022-12-14T22:15:58.544331Z",
	"occured_date": "2022-12-25"
}
```
## Edit a Win
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /wins/pk
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"title": "Example title",
	"win": "Example win",
	"win_picture": null,
	"created_date": "2022-12-14T22:15:58.544331Z",
	"occured_date": "2022-12-25"
}
```
## Edit a Win(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: Title, Win
```json
PUT /wins/pk
{
	"title": "Example title",
	"win": "Example win",
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a Win
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /wins/pk
```
## Response
```json
204 No Content
```

## Create a Starr Story
### Request
requirements: user must be logged in
required fields:  "Question"
```json
POST /starr-stories/
{
	"question": "What?",
	"summary": "A summary of what",
	"situation": "What is the situation",
	"task": "What tast",
	"action": "What action",
	"reflection": "What reflection",
	"result": "What result"
}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"question": "What?",
	"summary": "A summary of what",
	"situation": "What is the situation",
	"task": "What tast",
	"action": "What action",
	"reflection": "What reflection",
	"result": "What result"
}
```
## Starr Story list
### Request
Requirement: user must be logged in
```json
GET /starr-stories/
```
### Response
```json
200 OK
{
	"pk": 1,
	"question": "What?",
	"summary": "A summary of what",
	"situation": "What is the situation",
	"task": "What tast",
	"action": "What action",
	"reflection": "What reflection",
	"result": "What result"
}
```
NOTE: This will be a list of all the users Starr Stories
## Starr Story Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /starr-stories/pk    Ex: /starr-stories/1
```
### Response
```json
{
	"pk": 1,
	"question": "What?",
	"summary": "A summary of what",
	"situation": "What is the situation",
	"task": "What tast",
	"action": "What action",
	"reflection": "What reflection",
	"result": "What result"
}
```
## Edit a Starr Story
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /starr-stories/pk
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"question": "What?",
	"summary": "A summary of what",
	"situation": "What is the situation",
	"task": "What tast",
	"action": "What action",
	"reflection": "What reflection",
	"result": "What result"
}
```
NOTE: Response should reflect changes
## Edit a Starr story(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: Question
```json
PUT /starr-stories/pk
{
	"question": "What?",
	"summary": "A summary of what",
	"situation": "What is the situation",
	"task": "What tast",
	"action": "What action",
	"reflection": "What reflection",
	"result": "What result"
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a Starr Story
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /starr-stories/pk
```
## Response
```json
204 No Content
```

## Create a Target Company
### Request
requirements: user must be logged in
required fields: company_name, website
```json
POST /target-company/
{
	"pk": 1,
	"company_name": "google",
	"rank": 1,
	"website": "http://google.com",
	"job_page": "http://google.com/job",
	"comments": "They're alright",
	"created_at": "2022-12-14T20:10:54.796051Z",
	"updated_at": "2022-12-14T20:10:54.796064Z"
}
```
NOTE: Rank has a choice to be 1-5 but users can select multiple companies to a single rank
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"company_name": "google",
	"rank": null,
	"website": "http://google.com",
	"job_page": "http://google.com/job",
	"comments": "They're alright",
	"created_at": "2022-12-14T20:10:54.796051Z",
	"updated_at": "2022-12-14T20:10:54.796064Z"
}
```
## Target Company list
### Request
Requirement: user must be logged in
```json
GET /target-company/
```
### Response
```json
200 OK
{
	"pk": 1,
	"company_name": "google",
	"rank": null,
	"website": "http://google.com",
	"job_page": "http://google.com/job",
	"comments": "They're alright",
	"created_at": "2022-12-14T20:10:54.796051Z",
	"updated_at": "2022-12-14T20:10:54.796064Z"
}
```
NOTE: This will be a list of all the users Target Companies
## Target Company Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /target-comapny/pk    Ex: /target-company/1
```
### Response
```json
{
	"pk": 1,
	"company_name": "google",
	"rank": null,
	"website": "http://google.com",
	"job_page": "http://google.com/job",
	"comments": "They're alright",
	"created_at": "2022-12-14T20:10:54.796051Z",
	"updated_at": "2022-12-14T20:10:54.796064Z"
}
```
## Edit a Target Company
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /target-company/pk
{
	"company_name": "momentum",
}
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"company_name": "momentum",
	"rank": null,
	"website": "http://google.com",
	"job_page": "http://google.com/job",
	"comments": "They're alright",
	"created_at": "2022-12-14T20:10:54.796051Z",
	"updated_at": "2022-12-14T20:10:54.796064Z"
}
```
NOTE: Response should reflect changes
## Edit a Target Company(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: company_name, website
```json
PUT /target-company/pk
{
	"company_name": "google",
	"rank": null,
	"website": "http://google.com",
	"job_page": "http://google.com/job",
	"comments": "They're alright",
	"created_at": "2022-12-14T20:10:54.796051Z",
	"updated_at": "2022-12-14T20:10:54.796064Z"
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a Target Company
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /target-company/pk
```
## Response
```json
204 No Content
```
## Create a Company Contact
### Request
requirements: user must be logged in
required fields: company, name
```json
POST /target-company/contact
{
	"company": 1,
	"name": "joe",
	"email": "joe@example.com",
	"notes": "Joe likes to make his own deodorant"
}
```
NOTE: company needs to be a pk referring to an existing company within the app
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"company": 1,
	"name": "joe",
	"email": "joe@example.com",
	"notes": "Joe likes to make his own deodorant"
}
```
## Company Contact list
### Request
Requirement: user must be logged in
```json
GET /target-company/contacts
```
### Response
```json
200 OK
{
	"pk": 1,
	"company": 1,
	"name": "joe",
	"email": "joe@example.com",
	"notes": "Joe likes to make his own deodorant"
}
```
NOTE: This will be a list of all the users company contacts
## Company Contact Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /target-comapny/contact/pk    Ex: /target-company/contact/1
```
### Response
```json
{
	"pk": 1,
	"company": 1,
	"name": "joe",
	"email": "joe@example.com",
	"notes": "joe likes blueberry muffins"
}
```
## Edit a Comany Contact
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /target-company/contact/pk
{
	"notes": "Joe hates blueberry muffins",
}
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"company": 1,
	"name": "joe",
	"email": "joe@example.com",
	"notes": "Joe hates blueberry muffins"
}
```
NOTE: Response should reflect changes
## Edit a Company Contact(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: company, name
```json
PUT /target-company/contact/pk
{
	"pk": 1,
	"company": 1,
	"name": "joe",
	"email": "joe@example.com",
	"notes": "joe likes blueberry muffins"
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a Company Contact
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /target-company/contact/pk
```
## Response
```json
204 No Content
```

## Create a Short Personal Pitch
### Request
requirements: user must be logged in
required fields: title, pitch
```json
POST /personal-pitch/short/
{
	"title": "Example title",
	"pitch": "I am great! You should hire me",

}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"title": "Example title",
	"pitch": "I am great! You should hire me",
}
```
## Short Personal Pitch info
### Request
Requirement: user must be logged in
```json
GET /person-pitch/short
```
### Response
```json
200 OK
{
	"pk": 1,
	"title": "Example title",
	"pitch": "I am great! You should hire me",
}
```
NOTE: This will be a list of all the users short personal pitch
## Short Personal Pitch Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /personal-pitch/short/pk    
```
### Response
```json
{
	"pk": 1,
	"title": "Example title",
	"pitch": "I am great! You should hire me"
}
```
## Edit a Short personal pitch
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /personal-pitch/short/pk
{
	"title": "Number one pitch"
}
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"title": "Number one pitch",
	"pitch": "I am great! You should hire me",
}
```
NOTE: Response should reflect changes
## Edit a short personal pitch(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: title, pitch
```json
PUT /personal-pitch/short/pk
{
	"title": "Number one pitch",
	"pitch": "I am great! You should hire me",
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a short personal pitch
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /personal-pitch/short/pk
```
## Response
```json
204 No Content
```
## Create a Long Personal Pitch
### Request
requirements: user must be logged in
required fields: title, pitch
```json
POST /personal-pitch/long/
{
	"title": "Example title",
	"pitch": "I am great! You should hire me",

}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"title": "Example title",
	"pitch": "I am great! You should hire me",
}
```
## Long Personal Pitch info
### Request
Requirement: user must be logged in
```json
GET /person-pitch/long/
```
### Response
```json
200 OK
{
	"pk": 1,
	"title": "Example title",
	"pitch": "I am great! You should hire me",
}
```
NOTE: This will be a list of all the users long personal pitch
## long Personal Pitch Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /personal-pitch/long/pk    
```
### Response
```json
{
	"pk": 1,
	"title": "Example title",
	"pitch": "I am great! You should hire me"
}
```
## Edit a long personal pitch
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /personal-pitch/long/pk
{
	"title": "Number one pitch"
}
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"title": "Number one pitch",
	"pitch": "I am great! You should hire me",
}
```
NOTE: Response should reflect changes
## Edit a long personal pitch(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: title, pitch
```json
PUT /personal-pitch/long/pk
{
	"title": "Number one pitch",
	"pitch": "I am great! You should hire me",
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a long personal pitch
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /personal-pitch/long/pk
```
## Response
```json
204 No Content
```
## Create a Link
### Request
requirements: user must be logged in
required fields: title, link
```json
POST /user/link/
{
	"title": "Github",
	"link": "https://github.com/IIS-app/",

}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"title": "Github",
	"link": "https://github.com/IIS-app/",
}
```
## link info
### Request
Requirement: user must be logged in
```json
GET /user/link/
```
### Response
```json
200 OK
{
	"pk": 1,
	"title": "Github",
	"link": "https://github.com/IIS-app/",
}
```
NOTE: This will be a list of all the users wins



## Link Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /user/link/pk    
```
### Response
```json
{
	"pk": 1,
	"title": "Github",
	"link": "https://github.com/IIS-app",
}
```
## Edit a link
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /user/link/pk
{
	"link": "https://github.com/IIS-app/IIS-backend"
}
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"title": "Github",
	"link": "https://github.com/IIS-app/IIS-backend",
}
```
NOTE: Response should reflect changes
## Edit a link(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: title, link
```json
PUT /user/link/pk
{
	"title": "Github",
	"link": "https://github.com/IIS-app/IIS-backend",
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a link
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /user/link/pk
```
## Response
```json
204 No Content
```

## Create a Job
### Request
requirements: user must be logged in
required fields: title, job_listing, company
```json
POST /target-job/
{
	"title": "Google Software Engineer",
	"job_listing": "http://google.com",
	"company": 1
}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"title": "Google Software Engineer",
	"notes": null,
	"job_listing": "http://google.com",
	"company": 1
}
```
## job info
### Request
Requirement: user must be logged in
```json
GET /target-job/
```
### Response
```json
200 OK
{
	"pk": 1,
	"title": "Google Software Engineer",
	"notes": null,
	"job_listing": "http://google.com",
	"company": 1
}
```
NOTE: This will be a list of all the users jobs
## Job Detail
### Request
Requirement: user must be logged in, must be owner
```json
GET /target-job/pk    
```
### Response
```json
{
	"pk": 1,
	"title": "Google Software Engineer",
	"notes": null,
	"job_listing": "http://google.com",
	"company": 1
}
```
## Edit a Job
### Request
Requirement: user must be logged in, must be owner
```json
PTCH /target-job/pk
{
	"link": "https://google.com/joblistings"
}
```
NOTE: "Only add the fields you want to change."
## Response
```json
200 OK
{
	"pk": 1,
	"title": "Google Software Engineer",
	"notes": null,
	"job_listing": "http://google.com/joblistings",
	"company": 1
}
```
NOTE: Response should reflect changes
## Edit a job(Second way)
### Request
Requirement: user must be logged in, must be owner
Required fields: title, link
```json
PUT /target-job/pk
{
	"pk": 1,
	"title": "Google Software Engineer",
	"job_listing": "http://google.com",
	"company": 1
}
```
NOTE: This is essentially rebuilding the card you will still have to input other fields if you want to change them.
## Delete a link
### Request
Requirement: user must be logged in, must be owner
```json
DELETE /target-job/pk
```
## Response
```json
204 No Content
```




## Create a Compant Comment
### Request
requirements: user must be logged in
required fields: company(pk), notes
```json
POST /target-company/comments/
{
	"company": 1,
	"notes": "They didnt hire me :(",

}
```
### Response
response: If response is the same as the information you provided creation was successful
```json
200 OK
{
	"pk": 1,
	"created_at": "2022-12-26T22:52:13.309049Z",
	"updated_at": "2022-12-26T22:52:13.309084Z",
	"company": 1,
	"notes": "They didnt hire me :(",
	"important_date": null,
	"contact": null
}
```
## Company Comments info
### Request
Requirement: user must be logged in
```json
GET /target-company/comments/
```
### Response
```json
200 OK
{
		"pk": 1,
		"created_at": "2022-12-26T22:52:13.309049Z",
		"updated_at": "2022-12-26T22:52:13.309084Z",
		"company": 1,
		"notes": "They didnt hire me :(",
		"important_date": null,
		"contact": null
}
```
NOTE: This will be a list of all the users jobs




