# Cyber Security Project 1

This is an insecure web application which contains at least five different flaws from the OWASP top ten list.

## Installation Instructions

1. Clone the directory
2. Run the server with: ``python manage.py runserver``

You can use the three premade users:

- ``username: piketulus``
``password: 0000``

- ``username: John``
``password: Doe``

- ``username: Billy``
``password: Bob``


## Flaw 1: Broken access control

Access control means enforcing policies so that users cannot do things they were not meant to do or should not be allowed to do. In this web application, there are two cases of broken access control. First, users should only be able to delete messages that they have sent in their conversations, but since the id of the message is put in the URL, a user can manually type the id of any message into the URL and it will be deleted, regardless of whether it was sent by them or if they are even a recipient. Second, when sending messages, the fields that identify who is sending and who is receiving the message are shown and editable, so a user can pose as any other user and send a message from their name to anyone.

### How to execute:
- For deleting a message with know id (for example, 9), just type in the address: localhost/deleteMessage/9
- To send a message from someone else to someone else or to yourself, just switch the names in the sender and receiver fields to valid users before sending a message.

LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/templates/message/messages.html#L25
LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L95

To fix the flaws, we need to make sure that the user is who they are meant to be. First, to fix message deleting, we can make sure that the sender of the message to be deleted is also the logged in user of the request. The fix to the second problem similar as we check that the sender of the new message is the logged in user of the request, and if not, don't make the new message.

FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L142
FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L109


## Flaw 2: Injection

Applications can be subject to injection flaws if they do not validate, filter, or sanitize user-supplied data, meaning hostile data may be used directly and have severe effects. Also, queries, such as SQL queries may have unsafe structures that allow for exploitation. In this web application there is an unsafe SQL query, which can be exploited to, for example, delete all the messages in the database from everyone. 

### How to execute:
- To delete all messages:
- Add on to the previous flaw, where we would delete a message with localhost/deleteMessage/(id) by putting in 0 OR 1=1 for id. 
-Use localhost/deleteMessage/0 OR 1=1, as this will put 0 OR 1=1 to the end of the SQL query, and since 1=1 is always true, every message will be deleted instead of just he one with the specified id.

LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L129

To fix this we can simply get rid of the SQL query and use the delete function from Django’s ORM. This way, if someone tries to put something funny into the URL, when trying to get the message with that id it would simply throw an error, as it is not valid. 

FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L143


## Flaw 3: Security Logging and Monitoring Failures

Security logging and monitoring failures happen when there is insufficient logging, detection, monitoring, and active response within the system. Auditable events such as logins should be logged and monitored to detect suspicious and malicious activity. Also, warnings and errors should generate sufficient logs to detect flaws or attempts to break into the system. This web application has this flaw, and it cannot be found in just some specific code, as the flaw is the omission of any logging within the system. Due to this there are no clear reports of what has been happening on the server. 

A fix to this problem is to create a logger. It is also necessary to generate sufficient logs whenever important events happen. 

FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L12-L13
FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L44
FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L83
FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L118


## Flaw 4: Identification and Authentication Failures

An application can be said to have identification and authentication weaknesses if it permits very weak or default passwords. It is also not ideal for an application to provide a list of all valid usernames to everyone, as this can be used as a base to try to hack into others’ accounts. This application has both faults. When creating a new account, the password can be anything. Even a singular number like ‘1’ would be accepted. This is not very secure. Also, the index page shows anyone who logs in every other user’s username for them to choose from to message. This can be valuable information for malicious users. 

LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L18-L21
LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/templates/message/index.html#L17-L18

To fix the first problem, we can create a check for the password every time someone tries to create a new account. It will make sure that the password meets certain specifications, such as being at least 8 characters long, has a combination of numbers, letters, and special characters, etc. If the password is not acceptable, tell the user and don’t create the account, making them try again. For the second flaw, instead of listing all the users to everyone, we can simply have an input field where users must input the username of the person they want to message. This way they must know the other person’s name and cannot just spam everyone.

FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L29-L32
FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/templates/message/index.html#L28


## Flaw 5: Security Misconfiguration

Security misconfiguration can be an issue in an application if, for example, unnecessary features are enabled of installed or error handling is not properly done, which can reveal sensitive error messages to users. The first premade user of this application (piketulus) still has admin privileges which were not taken away yet. This can be easily fixed by revoking the admin privileges. Also, if users try to send messages or access pages in ways they are not meant to (through URL manipulation or otherwise), the application will throw errors as certain data it receives may be lacking or invalid. These errors can give inside information of how the application is built which can lead to exploitation.

LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L54-L59
LINK: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L91-L95

A fix for the error messages is to put parts of the code in try/except blocks so the errors can be handled correctly. Connecting to flaw 3, these errors, can then also be logged properly to give insight into the actions that have taken place within the application.

FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L65
FIX: https://github.com/Piketulus/CyberSecurityProject/blob/5dd33b3b16cac878e32002f7b378a1182c2982aa/mysite/message/views.py#L103
