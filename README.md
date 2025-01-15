# Crowdfund

Crowdfund is a Python project built using **FastAPI** and **PostgreSQL**. It provides a platform for managing crowdfunding projects. The project is containerized with **Docker** and hosted on **Fly.io** for easy deployment.

## Features
- Built with FastAPI for high-performance APIs.
- Uses PostgreSQL as the database.
- Provides auto-generated Swagger documentation for API exploration.
- Fully containerized with Docker for easy setup.

## Getting Started

### Prerequisites
Make sure you have the following installed on your system:
- **Docker** and **Docker Compose**: For running the project in a containerized environment.
- **Git**: To clone the repository.

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Daquiver1/crowdfund
   cd crowdfund
   ```

2. Start the project using Docker Compose:
   ```bash
   docker-compose up
   ```

3. Once the services are running, open your browser and go to:
   ```
   http://localhost:8008/docs
   ```

   You'll see the Swagger UI with the API documentation.

### Stopping the Project
To stop the running containers, use:
```bash
docker-compose down
```

## Deployment
This project is hosted on **Fly.io**, making it accessible online. The Docker configuration ensures smooth deployment.

## License
This project is licensed under [MIT License](LICENSE).

---
