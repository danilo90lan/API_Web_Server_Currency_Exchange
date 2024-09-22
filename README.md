# T2A2 - API Webserver - Currency Exchange

## Application Overview
The developed application is a backend API with the sole purpose of facilitating currency exchange and account management more effectively. 
This application allows users to create multiple accounts, each assigned a unique currency (such as AUD, USD, EUR, GBP, and more). Users can deposit funds into their respective accounts, which hold only the designated currency. Additionally, users have the ability to transfer money between their accounts and to other users' accounts. If the accounts involved have different currencies, the application automatically performs the necessary currency conversions based on current exchange rates. This functionality streamlines financial management and enhances user flexibility.
The facilities to be provided include:

### Account Management:

Allows the user to open and manage multiple accounts in various forms of currency. This will ensure that balance tracking and activities related to several accounts are tracked in one place.

### Real-Time Currency Exchange:

It fetches current and updated exchange rates from a third-party API. In this way, it ensures that the users will see the latest exchanges' rates before making any transaction in order to make better financial decisions.

### Deposit and Exchange Operations:

The users can easily deposit money and do currency exchange within the app. The amount exchanged calculated by the application based on the updated current rate in order to avoid any potential user-side errors.

### History of Transactions:

This application records every deposit and exchange made in its history, allowing users to review their financial activities. This feature encourages users to develop the habit of tracking their spending to budget effectively.

### Authorization and Security

The application puts in place secure authentication of users via JSON Web Tokens (JWT) so that only the respective owners have access to perform transactions on their accounts.

## How Application Solves the Problem

### Reduced Cost:

This would minimize dependence on expensive third-party services, as it provides direct access to real-time exchange rates and has the possibility of users managing their transactions through the app, thus minimizing transaction costs.

### Ease for the User:

Since a lot of people have accounts in different currencies, they are unable to handle them. This makes many errors and misunderstandings while financial planning are concerned. Keeping the management of currencies on one platform simplifies the procedures, which the user can handle without any confusion in his financial matters.

### Real-Time Data:

Real-time exchange rates enable users to decide on time, saving financial costs.

### Efficient Record Keeping:

By maintaining a record of detailed transaction history, the application enables the user to track his or her financial activities for a certain time period, thereby helping in better budgeting and financial planning.

### Security and Trust

With strong security measures in place, users are safer when it comes to the app for their financial needs.

## Problem Statement
There is quite a high burden of multiple currency financial management both for individuals and enterprises. Following are the key problems that one can find with objective references and statistics.

### Complexity of Currency Management:

According to a report by McKinsey & Company, small and medium-scale companies find hard to handle multiple currencies and this affects their financial activities.

### Inaccessibility to Real-Time Data:

World Bank records show that those businesses which cannot access real-time financial information are at a disadvantage and might lose 10% or more on currency transactions due to the lag in information.

### Record Keeping:

According to QuickBooks' survey, small business owners said that one of the major difficulties is to maintain accurate financial records, especially when confronted with numerous other currencies.

### Conclusion
This application approachingly answers critical problems in managing different currencies with objective statistics, showing the importance of such issues. The app enhances financial wellbeing with this easy-to-use and secure means of real-time data, transaction management, and account oversight. This is important in the global economy in which efficient currency management could mean much to individuals and businesses.

## Third-party services and packages and dependencies
Description of all the third-party services, packages, or dependencies used in the developed application:

### Flask
A micro web framework written in Python that is designed to keep to build web applications easily. It offers the most fundamental features of a web framework - routing, request handling, response generation making it lightweight and easy to extend.
Allows the user to provide the skeleton of the application by defining routes for several endpoints, for user authentication, currency management, or deposit operations. Its simplicity makes it an excellent choice for rapid development.

### Flask-JWT-Extended
An extension for Flask that makes the implementation of JSON Web Tokens easier to implement for secure user authentication.
Provides decorators to protect routes, handle token creation and validation, and manage user sessions. Ensures sensitive endpoints can only be accessed by authenticated users, which enhances the security of the whole application.

### SQLAlchemy
A powerful Object Relational Mapper (ORM) that provides a full suite of tools for interacting with relational databases in Python.
Used for defining data models, like User, Account, Exchange and Deposit as Python classes. SQL queries, data manipulation and schema migrations are possible via Python code.

### Marshmallow
A serialization/deserialization library that is used to easily convert complex datatypes to and from native Python datatypes.
Input validation and response formatting. Marshmallow schemas define the structure of the data that will be supplied in requests and returned in responses, so the application only processes valid data and raising error messages when validation fails.

### PostgreSQL
Open source relational database management system offering strong support for complex queries nd data integrity.
Provides the backbone storage for the application, maintaining all user accounts, transactions history, and currency data. It allows the application to support a multitude of users.

### Psycopg2
Python's adapter for PostgreSQL databases, offering functionality for the application to connect and interact with PostgreSQL databases.
Allows the execution of raw SQL queries and provides a robust method for handling database connections. Psycopg2 ensures that the application can manipulate databases effectively and securely.

### Python Dotenv
A module that loads environment variables from a .env file into the environment of the running application for better handling of the configuration settings in a secure manner.
Used to keep sensitive information, such as database credentials and API keys, out of source control. This practice reinforces security by not exposing sensitive data in the codebase.

### Requests
A simple HTTP library for Python, designed to make it easy to send HTTP requests and handle responses.
Used to interact with external APIs, such as fetching real-time currency exchange rates. Requests simplifies error handling and response parsing, as well as supports a number of different authentication methods that make it a useful tool for API interactions.

### bcrypt
A password hashing library which implements the bcrypt hashing algorithm to securely hash passwords.
It is used to secure users' passwords before putting it in the database. If there is a breach, bcrypt will prevent any user credentials from being exposed by hashing passwords, adding extra security.
 
### APScheduler
A powerful Python library to run Python functions periodically. It allows the user to automate tasks, like updating the currency exchange rates on schedule, time of day or each hour/day. By doing this, the application will always have the most recent data about currency rates creating a very accurate financial management.

### Open Exchange Rates API
https://openexchangerates.org/

A third-party API providing current and historical foreign exchange rates.
Pulls new currency exchange rates for use in the application to carry out conversions accurately and keeps the user updated with the latest information on the currency market.
The value addition that the application will get from the use of the Open Exchange Rates API is huge, in terms of precision and reliability in the provision of updated information on currencies, which is great in financial management.