# IT Task Manager

IT Task Manager is an internal task management tool designed to efficiently organise the work of teams of developers, designers, project managers, and quality assurance (QA) specialists. This task manager allows the team to create tasks, assign them to team members, and mark the completion of tasks. The main goal of the project is to simplify the task management process and increase team productivity.

## Installing / Getting started

Follow these steps to get started with IT Task Manager:
Requirements

Python 3.8 or later

PostgreSQL 16

### Installation instructions

* Clone this repository
* Create and activate a virtual environment
* Configure the `.env` file using the example of `.env_example` and activate it
* Execute `build.sh` file

### Getting started

Now everything is ready to launch the server
```shell
./manage.py runserver
```

If a port or network is busy, you can change it by example:
```shell
./manage.py runserver 0.0.0.0:80
```

If you need a superuser, then:
```shell
./manage.py createsuperuser
```

## Developing

To develop in debug mode, you need to specify `DEBUG=False` in `.env`

To test app run:
```shell
./manage.py test
```

## Features






What's all the bells and whistles this project can perform?
* Create and assign tasks: Team members with team_staff permissions can create new tasks and assign them to other team members.
* Tracking tasks: A separate list of completed and outstanding tasks is displayed for each employee.
* Tags for tasks: The ability to add tags (for example, ‘landing-page-layout’ or ‘python-refactoring’) for tasks that support Many-to-Many communication.
* Support for projects and teams: Support for working with multiple projects and teams, where different teams can work on different projects. Multiple tasks can be created within each project.

## Contributing

When you publish something as open source, one of the 
biggest motivations is that anyone can just jump in 
and start contributing to your project.

In addition, this project is licensed under the WTFPL,
which gives you a lot of freedom to use and modify the software. 
If you would like to contribute, please branch the repository and 
use the functionality branch. We warmly welcome pull requests.

## Links


- Repository: https://github.com/CharmNiovi/it_company_task_manager
- Issue tracker: https://github.com/CharmNiovi/it_company_task_manager/issues
- Project homepage: https://it-company-task-manager-v9l3.onrender.com/ (Test user: username=TestUser, password=qwe123QWE!@#)

## Licensing

"The code in this project is licensed under WTFPL license."
