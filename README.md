# Waste Management System

## Overview

The Waste Management System is a comprehensive solution aimed at transforming waste collection, processing, and recycling practices to achieve enhanced efficiency and environmental sustainability. This system is developed using Python and Django. It addresses the challenges of the existing waste management system, which include inadequate record-keeping, limited user incentives, and a lack of accountability for waste collectors. The proposed system integrates cutting-edge technologies and user-centric features to optimize waste management and foster active user participation.

## Objectives

The main objectives of the proposed Waste Management System are as follows:

1. **Centralized Database**: Establish a centralized database for real-time tracking of waste collection activities, types of waste, and quantities collected.

2. **Accountability for Collectors**: Enhance accountability by implementing performance metrics for waste collectors.

3. **User Engagement**: Engage users actively through a rewards program that incentivizes waste contributors to participate in recycling efforts.

4. **Data-Driven Planning**: Improve planning for recycling and waste processing facilities by analyzing data on waste types and quantities collected.

## Key Features

The key features of the proposed Waste Management System include:

1. **User Registration and Types**: Different functionalities for customers, waste collectors, and administrators.

2. **Rewards Program**: Provides rewards to users based on their recycling efforts, offering points that can be redeemed for discounts or eco-friendly products.

3. **Facility Information**: Maintains crucial details about facility locations, capacities, and accepted waste types.

4. **Collector Performance Evaluation**: Evaluates waste collector performance based on successful pickups, average collection time, and user ratings.

5. **User Feedback**: Encourages users to provide feedback and ratings, contributing to improved service quality and overall user satisfaction.

## Advantages

The proposed Waste Management System offers several advantages, including:

- Streamlined Record-Keeping: Through the centralized database, the system simplifies record-keeping.

- Increased User Engagement: Incentives and rewards encourage active user participation in recycling efforts.

- Improved Collection Efficiency: The system focuses on waste collector performance, leading to more efficient waste collection.

## Installation

To run this project locally, follow these steps:

1. Clone this repository to your local machine.

   ```
   git clone <repository-url>
   ```

2. Create a virtual environment and activate it.

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the project dependencies.

   ```
   pip install -r requirements.txt
   ```

4. Set up the Django database and run migrations.

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser account to access the admin panel.

   ```
   python manage.py createsuperuser
   ```

6. Start the development server.

   ```
   python manage.py runserver
   ```

7. Access the admin panel at `http://localhost:8000/admin/` and use your superuser credentials to log in.

## Usage

Once the project is set up and the server is running, users can access the Waste Management System through the web interface. Different user types (customers, waste collectors, and administrators) will have access to their respective functionalities.

## License

This project is licensed under the [MIT License](LICENSE).
