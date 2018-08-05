# Item Catalog

This program allows users to access a catalog website using Google's Oauth2 authentication. Once users log in, they are able to add, edit and remove items from catagories listed on the catagories page. When the user is finished, they may logout of the system and they will no longer have access to CRUD operations.

## Getting Started

The following information will show how to get this program running on your local machine.

### Installing

To get the program up and running locally, first clone this repository: https://github.com/Cademcp/Item-Catelog

Navigate to the catalog subdirectory using cd

```
cd Item_Catelog_Project/vagrant
```

Once in the vagrant directory, run the following command to spin up the VM:

```
vagrant up
```

Once that command is finished, run this command to log into the machine:

```
vagrant ssh
```

Once you are successfully logged in, you can access the project files on the VM using:

```
cd /vagrant/catalog
```

To initialize the database and populate it with the data necessary for the program to run, use the following commands in order:

```
python dbsetup.py
```

```
python dbadddata.py
```

To start up the application run:

```
python application.py
```

To access the application in your browser, visit http://localhost:5000 or http://localhost:5000/catalog

## Built With

* [Python 2.7](https://docs.python.org/2/index.html) - Programming Language
* [SQLAlchemy](https://docs.sqlalchemy.org/en/latest/) - Database Management Tool
* [Flask](http://flask.pocoo.org/docs/1.0/) - API framework
* [OAuth 2.0](https://developers.google.com/identity/protocols/OAuth2) - Google's Authentication Services


## Authors

* **Cade McPartlin** - *Full Stack Development* - [GitHub](https://github.com/Cademcp)

See also the list of [contributors](https://github.com/Cademcp/Item-Catelog/graphs/contributors) who participated in this project.


## Acknowledgments

* Udacity Full Stack We Development Nanodegree program 
