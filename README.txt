README
========


Extract
--------------------------------------------------------------
Extract manav-vishwas-9131332447.zip




Change Directory
-------------------------------------------------------------
Change current working directory to manav-vishwas-9131332447




Run DynamoDB Local
---------------------------------------------------------------
Change the current working directory to  """./manav-vishwas-9131332447/dynamo_db_schema"""  and run the following command to run local DynamoDB

--NOTE--
To run DynamoDB on your computer, you must have the Java Runtime Environment (JRE) version 8.x or newer. The application doesn't run on earlier JRE versions.


CMD--> java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb   (In linux OS)

---NOTE--
If you're using Windows PowerShell, be sure to enclose the parameter name or the entire name and value like this:

CMD--> java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -sharedDb (In windows OS)

DynamoDB processes incoming requests until you stop it. To stop DynamoDB, press Ctrl+C at the command prompt.

DynamoDB uses port 8000 by default. If port 8000 is unavailable, this command throws an exception. For a complete list of DynamoDB runtime options, including -port, enter this command.

java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -help




Install python requirement.txt package
-------------------------------------------------------------
After run the local DynamoDB install python packages default python version is 3.8.6

Change the current working directory to """./manav-vishwas-91313332447/python_code/""" and run the following commands-

CMD-->  pip install -r requirement.txt
			OR
You can manually install or require package by-

CMD--> pip install <package_name==version>




Run the project
-----------------------------------------------------------
After done this run the following command-

CMD--> python view.py

The view.py present in ./manav-vishwas-91313332447/python_code/




Users in project
-----------------------------------------------------------
By default I created only two user in this project

username-demo@gmail.com
password-demo

You can add new user by run following command-

CMD-->python put_item.py









