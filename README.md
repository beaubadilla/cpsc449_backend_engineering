<br />
<p align="center">
  <h1 align="center">Microservice Architecture</h1>

  <p align="center">
    Practice developing application programming interfaces(APIs) under a microservice architecture.<br/>
    Project for <a href="http://www.fullerton.edu/">Cal State Fullerton</a>'s Back-End Engineer course(CPSC 449).
    <br />
    <a href="https://github.com/beaubadilla/cpsc449_backend_engineering/issues">Report Bug or Request Feature</a>
  </p>
</p>

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [License](#license)
* [Contact](#contact)

## About the Project

This project simulates the back-end for a music playlist creation app. It was split up into three parts for the duration of the semester. Every student grouped up with two other students because our professor wanted to imitate a realistic development team. In addition, each group member had a designated role(Developer, Developer, Operations) in which we would swap roles for each part of the project. It aimed to have us implement everything we learned about scalability: representation state transfer(REST) APIs,  database sharding and replication, caching, stateful v.s. stateless, SQL vs NoSQL.

* **microservices**: Assigned to the <ins>Developer</ins> role, my responsibility was implementing REST APIs for users and playlist descriptions.
* **microservices-2**: Assigned to the <ins>Operations</ins> role, my responsbility was configuring Kong Gateway and setting up the procfile.
* **microservices-3**: Assigned to the <ins>Developer</ins> role, my responsibility was creating a wide-column database and converting all our SQL queries into CQL queries.


### Built With
Languages: Python 3.x, SQL/CQL
* microservices - [Flask](https://flask.palletsprojects.com/en/1.1.x/), [PugSQL](https://pugsql.org/), [SQLite](https://docs.python.org/3/library/sqlite3.html)
* microservices-2 - [Kong Gateway](https://konghq.com/kong/)
* microservices-3 - [ScyllaDB](https://www.scylladb.com/)

## Getting Started

### Prerequisites

Download [Python 3.x](https://www.python.org/downloads/)

### Installation

1. Clone the repo
```sh
git clone https://github.com/beaubadilla/cpsc449_backend_engineering.git
```
2. Follow the README.md for each individual part.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Beau Jayme De Guzman Badilla - beau.badilla@gmail.com - [LinkedIn](https://www.linkedin.com/in/beau-jayme-badilla/)
