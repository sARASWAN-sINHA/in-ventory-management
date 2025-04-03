# Asset Inventory Management

This project is a **Django-based web application** designed to manage and track assets efficiently. It provides features for adding, updating, and monitoring assets, ensuring streamlined inventory management.

## Features

### Core Features
- **Asset Management**: Create, update, and manage assets and their types.
- **User Management**: Custom user model with roles like Admin, Moderator, and Normal User.
- **Requisition System**: Assign assets to users with validation for quantity and dates.
- **File Upload**: Upload CSV files to bulk assign assets with validation checks.
- **Ownership History**: Track the ownership history of assets.
- **Custom Permissions**: Role-based access control for different actions.

### API Features
- **RESTful APIs**: Built using Django REST Framework (DRF).
- **JWT Authentication**: Secure authentication using JSON Web Tokens.
- **Swagger Documentation**: Auto-generated API documentation using DRF Spectacular.

---

### Prerequisites
- Python 3.10 or higher
- Docker and Docker Compose
- PostgreSQL (if not using Docker)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/asset-inventory-management.git
   cd asset-inventory-management
2. **Set Up Environment Variables**

- Create a .env.postgres file in the env/ directory with the following content
    ```POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres```

3. **Run Database Migrations**

- Open a terminal inside the web container:
    - Generate DB migration files.
        ``` docker-compose run --rm web sh -c " python manage.py makemigrations" ```


3. **Build and Run the Docker Containers**

- Build and start the containers using Docker Compose
    ``` docker-compose up --build ```
- This will
    - Wait for the DB in the database container to be ready to accept connections.
    - Perform all the migrations
    - Start the following services:
        - Web: Django application running on http://localhost:8000.
        - Database: PostgreSQL database running on localhost:5432.

4. **Create a superuser**
- Open terminal and cd to the project path. (Make sure that the continer is running)
    ``` docker-compose run --rm web sh -c " python manage.py createsuperuser" ```
5. **Accessing the Application**
    - Open your browser and navigate to http://localhost:8000/admin to access the Django admin panel.
    - The API documentation is available at:
        - Swagger UI: http://localhost:8000/api/doc
        - ReDoc: http://localhost:8000/api/redoc

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or support, please contact:
- **Email**: support@example.com
- **GitHub**: [your-username](https://github.com/your-username)
