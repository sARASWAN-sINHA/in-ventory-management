# Asset Inventory Management

This project is a **Django-based web application** designed to manage and track assets efficiently. It provides features for adding, updating, and monitoring assets, ensuring streamlined inventory management. It provides a robust set of features to handle asset lifecycle management, user roles, and permissions, as well as requisition and ownership tracking.


## Overview of the Project

The system is built to address the challenges of managing organizational assets, such as tracking their types, quantities, locations, and ownership. It ensures efficient inventory management by providing tools for asset creation, updates, and monitoring, along with user role-based access control.


Below is a detailed overview of the features and its uses:


**Key Features and Their Uses**
- **Asset Management**
Purpose: Enables organizations to create, update, and manage assets and their types.
    - Uses:
Maintain a centralized database of all assets.
Categorize assets by type, subtype, and group for better organization.
Track asset details such as quantity, location, and manufacturer.
- **User Management**
Purpose: Provides a custom user model with roles such as Admin, Moderator, and Normal User.
    - Uses:
Assign specific roles to users to control their access and permissions.
Ensure that only authorized personnel can perform critical actions like asset creation or deletion.
- **Requisition System**
Purpose: Allows assets to be assigned to users with validation for quantity and requisition dates.
    - Uses:
Facilitate the allocation of assets to employees or departments.
Validate requisition requests to ensure that the requested quantity and dates are feasible.
Prevent over-allocation of assets by checking available quantities.
- **File Upload**
Purpose: Supports bulk asset assignments through CSV file uploads with validation checks.
    - Uses:
Simplify the process of assigning multiple assets at once.
Validate uploaded data to ensure accuracy and consistency.
Generate error logs for invalid entries, helping administrators correct issues.
- **Ownership History**
Purpose: Tracks the ownership history of assets over time.
    - Uses:
Maintain a record of which user owned an asset and for how long.
Provide accountability and traceability for asset usage.
Support audits by offering detailed ownership logs.
- **Custom Permissions**
Purpose: Implements role-based access control for different actions.
    - Uses:
Restrict sensitive operations (e.g., asset deletion) to Admins or Moderators.
Allow Normal Users to view or request assets without modifying them.
Enhance security by limiting access based on user roles.
- **RESTful APIs**
Purpose: Exposes the system's functionality through APIs built using Django REST Framework (DRF).
    - Uses:
Enable integration with external systems or applications.
Allow developers to build custom frontends or mobile apps using the APIs.
- **JWT Authentication**
Purpose: Secures the application using JSON Web Tokens for authentication.
    - Uses:
        Ensure secure access to the system's APIs.
Provide token-based authentication for seamless user sessions.
- **Swagger Documentation**
Purpose: Auto-generates API documentation using DRF Spectacular.
Uses:
Help developers understand and test the available APIs.
Provide a user-friendly interface for exploring API endpoints.


**Uses of the System**
- Streamlined Asset Management:
Organizations can efficiently manage their inventory of assets, ensuring that all assets are accounted for and properly categorized.

- Improved Accountability:
The ownership history feature ensures that every asset's usage is tracked, providing transparency and accountability.

- Enhanced Security:
Role-based access control and JWT authentication ensure that only authorized users can access or modify sensitive data.

- Bulk Operations:
The file upload feature simplifies bulk asset assignments, saving time and reducing manual errors.

- Audit and Compliance:
Detailed logs of asset ownership and requisitions support audits and compliance with organizational policies.

- Integration Capabilities:
The RESTful APIs allow the system to integrate with other tools, such as ERP systems or custom dashboards.

- User-Friendly Documentation:

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
