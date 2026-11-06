# Online Event Registration and Management System

Simple demo built with HTML, CSS, JavaScript and LocalStorage.

## Demo admin credentials
- Email: admin@event.com
- Password: admin123

## Run with Docker
```bash
docker build -t online-event-management .
docker run --name event-app -p 8081:80 -d online-event-management
```
Open http://localhost:8081

Stop container:
```bash
docker rm -f event-app
```

## Selenium tests
Needs Python 3, Google Chrome, Docker and Selenium:
```bash
python -m pip install -r requirements.txt
docker build -t online-event-management .
docker run -d --name online-event-management -p 8081:80 online-event-management
python -m unittest discover -s tests -p "test_*.py" -v
docker rm -f online-event-management
```

Jenkins agent requirements: Docker CLI/daemon, Python 3, pip, Google Chrome and permission to run Docker commands. The supplied Jenkinsfile expects a Linux agent with `sh`.

## Limitations
LocalStorage is browser-specific and not shared across devices. Demo passwords and admin credentials are not secure. Clearing browser data removes saved project data. Add a backend API and database if you later need real multi-user functionality.
