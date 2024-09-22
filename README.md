# T2A2 - API Webserver - Currency Exchange

## Application Overview
The developed application is a backend API with the sole purpose of facilitating currency exchange and account management more effectively. 
This application allows users to create multiple accounts, each assigned a unique currency (such as AUD, USD, EUR, GBP, and more). Users can deposit funds into their respective accounts, which hold only the designated currency. Additionally, users have the ability to transfer money between their accounts and to other users' accounts. If the accounts involved have different currencies, the application automatically performs the necessary currency conversions based on current exchange rates. This functionality streamlines financial management and enhances user flexibility.  
The features provided include:

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

## Third-party services, packages and dependencies
Description of all the third-party services, packages, or dependencies used in the developed application:

### Flask
A micro web framework written in Python that is designed to keep to build web applications easily. It offers the most fundamental features of a web framework - routing, request handling, response generation making it lightweight and easy to extend.
Allows the user to provide the skeleton of the application by defining routes for several endpoints, for user authentication, currency management, or deposit operations. Its simplicity makes it an excellent choice for rapid development.
In this app Flask serves several keys roles:
* **Web Framework**
Flask provides the foundational structure for your web application, allowing you to define routes and handle HTTP requests and responses efficiently.
* **Routing**
It enables you to create specific endpoints (URLs) for various functionalities, such as retrieving currencies, managing accounts, and processing deposits and exchanges.
* **Request Handling**
Flask processes incoming requests, extracting data from HTTP methods (GET, POST, PATCH, DELETE) and passing it to the appropriate functions for processing.

### Flask-JWT-Extended
An extension for Flask that makes the implementation of JSON Web Tokens easier to implement for secure user authentication.
Provides decorators to protect routes, handle token creation and validation, and manage user sessions. Ensures sensitive endpoints can only be accessed by authenticated users, which enhances the security of the whole application.
Flask-JWT-Extended integrates smoothly with Flask, making it easy to set up and use in the application. It offers decorators like ```@jwt_required()``` to secure routes with minimal code.
The package provides features for creating, refreshing, and verifying JWTs. This includes handling expiration times for tokens, allowing users to maintain their session securely.

### SQLAlchemy
A powerful Object Relational Mapper (ORM) that provides a full suite of tools for interacting with relational databases in Python.
Used for defining data models, like User, Account, Exchange and Deposit as Python classes. SQL queries, data manipulation and schema migrations are possible via Python code.
SQLAlchemy allows defining Python classes that map directly to database tables. This means you can work with Python objects instead of writing raw SQL queries, making the code easier to maintain.
SQLAlchemy simplifies the process of creating, reading, updating, and deleting records in the PostgreSQL database.
With SQLAlchemy, it's possible to construct complex queries using a Python syntax. This allows easy filtering, ordering, and joining of tables without needing to write SQL manually.

### Marshmallow
A serialization/deserialization library that is used to easily convert complex datatypes to and from native Python datatypes.

* **Data Serialization**
Marshmallow converts complex data types, such as SQLAlchemy model instances, into native Python data types (like dictionaries). This process is essential for preparing data to be sent in JSON format to clients.  

* **Data Deserialization**
When receiving data from clients (e.g., through POST requests), Marshmallow validates and converts incoming JSON data into Python objects. This ensures that the data adheres to the expected schema before being processed or stored.

* **Schema Definition**
Marshmallow allows the user to define schemas that specify the structure and requirements of data. Specific rules can be set such as required fields, data types, and custom validation logic, making it easier to manage the data flow in the application.

* **Validation**
Marshmallow is also used to validate incoming data against the defined schemas, providing useful error messages if the data doesn't meet the specified criteria. This helps prevent invalid or malicious data from being processed.  

*Example:*  
In the currency application,  Marshmallow is used for the following tasks:

* When a user register an account it ensure that that account is registered with a unique currency code
* When a user deposits or exchange money, the incoming data is validated using a Marshmallow schema to ensure it includes the necessary fields (like amount and description).
* When retrieving transaction history, the data is serialized into a format suitable for sending back to the client.

### PostgreSQL
Open source relational database management system offering strong support for complex queries nd data integrity.
Provides the backbone storage for the application, maintaining all user accounts, transactions history, and currency data. It allows the application to support a multitude of users.
PostgreSQL stores all the application's data, including user accounts, financial transactions (deposits, exchanges), currency information, and account histories.
PostgreSQL ensures data integrity through features like constraints, foreign keys, and transactions.This helps maintain accurate and consistent data, preventing issues like orphaned records or invalid data states.

### Psycopg2
Python's adapter for PostgreSQL databases, offering functionality for the application to connect and interact with PostgreSQL databases.
Allows the execution of raw SQL queries and provides a robust method for handling database connections. Psycopg2 ensures that the application can manipulate databases effectively and securely.

### Python Dotenv
A module that loads environment variables from a .env file into the environment of the running application for better handling of the configuration settings in a secure manner.
Used to keep sensitive information, such as database credentials and API keys, out of source control. This practice reinforces security by not exposing sensitive data in the codebase.

### Requests
A simple HTTP library for Python, designed to make it easy to send HTTP requests and handle responses.
Requests is utilized to make API calls to the Open Exchange Rates API. This allows the application to retrieve up-to-date currency exchange rates, which are essential for performing accurate currency conversions and managing financial transactions across different currencies.  
Requests simplifies error handling and response parsing, as well as supports a number of different authentication methods that make it a useful tool for API interactions.

### bcrypt
A password hashing library which implements the bcrypt hashing algorithm to securely hash passwords.
It is used to secure users' passwords before putting it in the database. If there is a breach, bcrypt will prevent any user credentials from being exposed by hashing passwords, adding extra security.
* When a user creates an account or updates their password, bcrypt takes the plain-text password and generates a secure hash. This hash is a fixed-length string that represents the password but cannot be easily reversed to retrieve the original password.
* bcrypt automatically adds a unique salt to each password before hashing. A salt is a random string that is combined with the password to prevent attackers from using precomputed hash tables (rainbow tables) to crack passwords. Each password hash will be different, even if two users have the same password.
* Instead of storing plain-text passwords in the database, the application stores the hashed version. This means that even if the database is compromised, attackers will not have direct access to the users' actual passwords.
* When a user attempts to log in, the application retrieves the hashed password from the database and uses bcrypt to hash the input password again (with the same salt). It then compares the two hashes. If they match, the user is authenticated.
 
### APScheduler
A powerful Python library to run Python functions periodically. It allows the user to automate tasks, like updating the currency exchange rates on schedule, time of day or each hour/day. APScheduler periodically fetches updated currency exchange rates from the Open Exchange Rates API. This ensures that the application always has access to the latest financial data without requiring manual intervention. 

``` python
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_exchange_rates,
    trigger="interval", minutes=60, args=[app])
    scheduler.start()
```
By integrating APScheduler, the application enhances its functionality by providing up-to-date currency information, which is essential for accurate financial transactions and reporting. This ultimately improves user experience and ensures reliability in currency management.

### Open Exchange Rates API
https://openexchangerates.org/

A third-party API providing current and historical foreign exchange rates.
Pulls new currency exchange rates for use in the application to carry out conversions accurately and keeps the user updated with the latest information on the currency market.
The value addition that the application will get from the use of the Open Exchange Rates API is huge, in terms of precision and reliability in the provision of updated information on currencies, which is great in financial management.

## PostgreSQL Advantages and Disadvantages

### Advantages of PostgreSQL
* **ACID Compliance**: PostgreSQL is fully compliant with ACID (Atomicity, Consistency, Isolation, and Durability). 
**Atomicity** ensures that all operations within a transaction are treated as a single unit for example if a user deposits funds, the system guarantees that the transaction either completes fully (reflecting the balance change) or is rolled back without partial updates.  
**Consistency** ensures that the database always remains in a valid state after each transaction, maintaining financial integrity.  
**Isolation** means that simultaneous transactions do not interfere with each other. This is crucial when multiple users are depositing funds, transferring between accounts, or exchanging currencies simultaneously, without causing conflicts.  
**Durability** guarantees that once a transaction is committed, the changes are permanent, even in the event of a system failure. This is especially important in a financial context, ensuring no lost data.

These aspects makes the app very reliable in financial transactions concerning the currency application, ensuring every transaction goes through 100% or is rolled back for consistency and integrity of data. This is an important aspect when deposits, exchanges, and transfers take place, since even minimal errors can mean huge losses in finances.

* **Relational Integrity and Handling of Complex Queries**: This is what PostgreSQL is particularly good at. It handles relational data structures, giving support for Foreign Keys, Joins, and Complex Queries. For instance, in the currency application, it allows defining relationships between the users, accounts, and operations-such as deposits and exchanges-for efficient data retrieval and complex reports about transactions or balances. In this Currency-exchanging app, PostgreSQL enables performing multi-table joins to retrieve a user's complete financial history across multiple accounts, operations, and even foreign exchanges.


* **JSONB support for flexible data structures**: Although PostgreSQL is strict for a relational model, it does support JSONB for semi-structured data storage or flexible data storage. This can be utilized for storing data that perfectly does not fit into the relational model, such as user-specific settings, metadata on exchange rates, or any evolving requirements that may require schema-less structure.

* **Scalability and Performance**: PostgreSQL handles large datasets and high transaction volumes efficiently, essential for a currency app that may grow in terms of users and transactions. Its ability to scale vertically (by adding hardware resources) and horizontally (through replication and sharding) means the database can grow along with the application.  
**Vertical scaling** allows the app to increase resources such as RAM or CPU for better performance. As the user base grows, the app can handle increasing amounts of data.  
**Horizontal scaling** is possible via replication, allowing the database to spread read/write operations across multiple instances. In a high-demand financial application, this is vital for improving response times and ensuring reliability.


* **Advanced Security Features**: In particular, PostgreSQL has high-level security features like user roles, fine-grained access control, and encryption through SSL to securely transmit data. Such features are also relevant to the currency exchange application in safeguarding sensitive information related to account balances, personal information, and financial activities from leakage, with the addition of compliance with laws concerning protection against data breaches.
For a currency exchange app dealing with sensitive financial information, protecting user data is crucial. PostgreSQL ensures secure communication over networks with SSL encryption, protecting against eavesdropping or tampering.  
**Role-based access control** helps in assigning privileges to different types of users, limiting who can access or modify sensitive data like balances, accounts, and exchange rates.

* **Free and Extensible**: Being open-source, PostgreSQL is free to use and very extensible. This would suit a project that might need some custom extensions or optimizations.
The PostgreSQL community regularly contributes new features, performance improvements, and security patches, keeping the system up-to-date and secure.

## Drawbacks of PostgreSQL
* **Complexity**: Postgres can be complex for new users to set up and use. It has a large set of features and options, which can make it overwhelming for beginners.

* **Slower performance**: When finding a query, Postgres due to its relational database structure has to begin with the first row and then read through the entire table to find the relevant data which cause performance issues. 
PotgreSQL performs slower especially when there is a large number of data stored in the rows and columns of a table containing many fields of additional information to compare.

* **Resource Intensive**: Compared to other lighter databases like MySQL or SQLite, the PostgreSQL database is a bit heavy. It requires more memory and CPU resources. This makes it unsuitable for running applications that need less power for computation.

* **Horizontal Scaling Challenges**: Although replication in general is supported by PostgreSQL, it is best suited for vertical scaling, where upgrades are made to the hardware of the server, rather than for horizontal scaling, where data is spread across numerous servers.
Large-scale applications that require very high scalability need advanced techniques like sharding, with PostgreSQL often tending to be pretty complicated and not fully natively supported without third-party solutions.

* **Lack of built-in tools**: Compared to some other database systems, Postgres does not have built-in tools for backups, monitoring and management. However, there are many third-party tools available that can provide these features.

## Object-Relational Mapping (ORM) Features and Functionalities
An ORM, or Object-Relational Mapping, provides an abstraction layer between an application and the database. This enables the developer to interact with the database using object-oriented programming techniques. In Python, this is done with ORMs like SQLAlchemy, used to simplify complex database operations into table classes and row objects.

### Mapping Database Tables to Classes
One of the core features of an ORM is its ability to map relational database tables to Python classes. Each row in a table is represented as an instance of the mapped class, while columns are represented as class attributes.  
*Example*
Consider a table Account in a database with fields like *id, account_name, currency_code, balance and date*. Here's how you would define this using SQLAlchemy:
``` python
class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(20), nullable=False)
    currency_code = db.Column(db.String(3)),
    balance = db.Float, default=0)
    date_creation = db.Column(db.DateTime, default=datetime.now()) 

# creating a new account object
new_account = Account(currency_code="USD", balance = 1000, account_name="savings")
```
In this example the Account class maps to the accounts table.  
Each instance of Account represents a row in the table.  
The fields id, currency_code, account_name, balance and datetime in the class map to the respective columns in the table.

### Querying the Database with ORM
With an ORM, querying the database is intuitive and object-oriented. Instead of writing SQL queries, developers can query objects directly using the ORM's API.  

#### How to fetch all records
 Using SQLAlchemy, fetching all records from a table is straightforward. Each row in the database table will be represented as an object of the mapped class.
``` python
# Query all accounts from the Account table
statement = db.select(Account).all()
accounts = db.session.scalars(statement)
```
The above query is equivalent to this SQL query:
``` sql
SELECT * FROM accounts;
```
#### How to fetch data with condition and/or filter Records
To filter records based on specific conditions it's used the filter() or filter_by() method.
In this case we use the filter() method with multiple conditions.

``` python
# Fetch accounts where the currency is 'USD' balance greater than 1000
statement = db.select(Account).filter(Account.currency="USD", Account.balance > 1000)
usd_accounts = db.session.scalars(statement)

```
The above query is equivalent to
``` sql
SELECT * FROM accounts WHERE currency = 'USD' AND balance > 1000;
```

### Managing Relationships Between Tables
ORMs allows defining relationships between different tables using Python objects, abstracting the complexity of SQL JOIN statements. For example, a User can have multiple Account objects, which corresponds to a one-to-many relationship between User and Account.

#### Example of a One-to-Many Relationship:
```python
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)     
    email = db.Column(db.String, nullable=False, unique=True)      
    password = db.Column(db.String, nullable=False)     
    is_admin = db.Column(db.Boolean, default=False)

    accounts = db.relationship("Account", back_populates="user")

    class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100))  
    balance = db.Column(db.Numeric(precision=10, scale=2), default=0) 
    date_creation = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    user = db.relationship("User", back_populates="accounts")
```

In the above example
- User can have many Accounts objects but each Account belongs to a single User.
- The user_id column in Account is a **foreign key** that links back to the User table.
- The relationship() function creates a reference between the two tables, enabling to retrieve the data easily.

#### Example of query of how to retrieve related data
``` python
# Query to retrieve all accounts of a specific user
statement = db.session.query(
            Account.account_id, Account.account_name
        ).join(User, Account.user_id == User.user_id)

        user_accounts = statement.filter(User.user_id == some_user_id).all()
```
- Select: Retrieves the account_id and account_name from the Account table.
- Join: Combines Account with User based on matching user_id values.
- Filter: Limits the results to accounts where the User.user_id matches the specified some_user_id.
- All: Executes the query and returns all matching records.

### Creating and Updating Records
ORMs allows easily inserting new records or updating existing ones, simplifying the database manipulation process.

#### Example of Inserting records
``` python
# Create a new Account
new_account = Account(account_name = "SAVINGS", currency_code="EUR", balance=2000.0)
# Add to session and commit
session.add(new_account)
session.commit()
```
#### Example of Updating records
#### Fetch an account
```python
account = session.query(Account).filter_by(id=1)
# update name
accouunt.account_name="Euro-trip"
```
#### Deleting records
Deleting records from a database is as simple as querying for the record and passing it to the delete() method.

#### Example on how to delete a record
``` python
# Fetch the account to be deleted
account = session.query(Account).filter_by(id=1)

# Delete and commit the transaction
session.delete(account)
session.commit()
```
This removes the record from the database permanently.

### Transaction Management
Among the main advantages of an ORM is the fact that they come with built-in transaction management. Support for transaction management within ORMs such as SQLAlchemy is among the most important features, ensuring data integrity and coherence over various database operations. Particularly, ORMs have native capabilities of committing and rolling back a transaction. That makes them efficient in taking care of the so-called complex data interactions.
It is standard in SQLAlchemy to handle transaction management via a session object. Here's how it works:

1. **Creating a Session**: A session is an object that is the major interface to the database and transaction management. You create a session using a sessionmaker.

2. **Adding Objects**: You can add objects to the session. These objects are not written straightaway to the database but are, instead, staged for insertion.

3. **Committing a Transaction**: At the time of issuing session.commit(), whatever changes have taken place in the session are written by SQLAlchemy to the database. If this commit goes through successfully, then that transaction is complete and all changes are permanent.

4. **Rolling Back a Transaction**: i there is an error at any point in the course of the transaction, you are able to roll back all changes that have been made in this session by using session.rollback(). This reverts the database back to its previous state before the transaction started.

### Advanced Transaction Management Features
- **Savepoints**: SQLAlchemy supports savepoints, which allow you to roll back to a certain point in a transaction rather than rolling back the whole transaction. That's useful during complex operations where you might want to do partial undoing. 
- **Concurrency Control:** SQLAlchemy provides various mechanisms that help it to cope with concurrent transactions and resolve conflicts that may arise between these transactions.
- **Context Management**: Using Python's with statement, a context can be created for a session; this automatically handles the commit and rollback behavior in a much cleaner and easier-to-manage way.
like

### Performance Optimization: Lazy Loading
A common design pattern in many ORMs, including SQLAlchemy, is lazy loading. Instead of loading related data immediately, it defers the load until actually needed. This can reduce memory usage quite drastically and improve application response times on larger data sets or complex object relationships.  
Lazy Loading Key Details:
- **Lazy Loading of Data**: In the practice of lazy loading, entities are not fetched from the database until it is absolutely accessed.
- **Reduced Memory Consumption**: Lazy loading reduces memory usage, particularly on entities with a lot of relationships. It will only load the data that needs to be used. This comes in quite handy when there are hundreds or even thousands of users within an application, or when dealing with massive amounts of data.
- **Smart Querying**: Lazy loading can lead to better querying patterns, where instead of executing one big join query that retrieves all related data at once, separate queries are executed only when needed. This means only the relevant data is fetched from the database.
like
 
### Automatic Schema Creation
Most ORM frameworks, including SQLAlchemy, support the generation of schema automatically, enabling the developer to create and manage database schemas directly from the application code. In this way, the development process is eased, becoming much simpler to evolve the database schema with the application, without having to write SQL scripts manually.
Key Facts of Automated Schema Generation:

- **Model definition**: If one uses ORM, then database table representations become classes (models). Each class defines schema: table names, column names, data types, constraints, and relationships.

- **Database Initialization**: Using auto-schema generation, initialization of the database becomes very easy. One calls a method, such as create_all from SQLAlchemy, and the ORM will provide the appropriate SQL to create the tables given the models that you have defined.

- **Data types and Constraints**: ORM automatically maps Python types to database types. This includes the definition of constraints such as primary keys, foreign keys, unique constraints, and fields being nullable according to the model definition.  

*Example*
``` python
class Exchange(db.Model):
    __tablename__ = "exchanges"
    exchange_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)       
    amount_exchanged = db.Column(db.Float), nullable=False)  
    description = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, default=datetime.now())

    # foreign keys
    from_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id", ondelete='SET NULL'))
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id", ondelete='SET NULL'))
```

- **Development Efficiency**: Automatic schema creation right out of the box at the start of development pivots the speed to prototype and iterate on a database design. A developer can quickly change their models and immediately see the result in the database sans cumbersome migration steps.