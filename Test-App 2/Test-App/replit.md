# Business Inventory Management System

## Overview

This is a Streamlit-based inventory management system designed for small to medium businesses. The application helps track products, manage stock levels, record sales, handle purchase orders, and provide financial analytics. The system uses a relational database to maintain product inventory, sales history, and purchase order information with comprehensive reporting and visualization capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Visualization**: Plotly (Express and Graph Objects) for interactive charts and graphs
- **Navigation**: Sidebar-based menu system with multiple functional modules:
  - Product management (view, add, manage)
  - Sales recording and reporting
  - Purchase order tracking
  - Financial dashboard
  - Trends and analytics
- **Layout**: Wide-page configuration for optimal data visualization

### Backend Architecture
- **ORM**: SQLAlchemy for database abstraction and object-relational mapping
- **Session Management**: SQLAlchemy SessionLocal for database connection pooling
- **Database Models**: Three core entities with relationships:
  1. **Product**: Central entity storing inventory items with pricing, stock levels, and reorder thresholds
  2. **Sale**: Transaction records linking products to sales with pricing and profit tracking
  3. **PurchaseOrder**: Procurement records for restocking with status tracking and delivery management

### Data Model Design
- **Product-centric architecture**: Products are the core entity with one-to-many relationships to sales and purchase orders
- **Financial tracking**: Dual-price system (buying_price and selling_price) enables profit margin calculations
- **Inventory control**: Reorder level thresholds trigger low-stock alerts
- **Temporal data**: DateTime stamps on sales and purchase orders enable time-series analysis
- **Extensibility**: Image URL support for product visualization

### Database Architecture
- **Connection**: Environment-based DATABASE_URL configuration for deployment flexibility
- **Schema**: Declarative Base pattern with automatic table creation via init_db()
- **Relationships**: Bidirectional ORM relationships between Product, Sale, and PurchaseOrder entities
- **Indexing**: Primary key indexing on all core tables for query performance

### Application Logic Patterns
- **Database session management**: Context-based sessions with proper cleanup in finally blocks
- **Error handling**: Try-catch-finally pattern with rollback on failures
- **Transaction safety**: Commit/rollback mechanisms to maintain data integrity
- **Data aggregation**: SQLAlchemy func and extract for complex queries (monthly reports, trends)

## External Dependencies

### Required Python Packages
- **streamlit**: Web application framework for the user interface
- **pandas**: Data manipulation and analysis for reporting features
- **plotly**: Interactive visualization library (express and graph_objects modules)
- **sqlalchemy**: ORM and database toolkit
- **python-dateutil**: Extended datetime functionality (relativedelta for date calculations)

### Database
- **Type**: SQL-based relational database (connection string provided via DATABASE_URL environment variable)
- **Note**: The schema is database-agnostic through SQLAlchemy, supporting PostgreSQL, MySQL, SQLite, or other SQL databases

### Environment Variables
- **DATABASE_URL**: Required connection string for database access (format depends on database type chosen)

### Third-party Services
- Optional image hosting service for product images (URLs stored in Product.image_url field)

## Recent Changes

### November 7, 2024 - Replit Environment Setup
- **Setup completed**: Successfully migrated GitHub import to Replit environment
- **Python 3.11 installed**: Programming language and all dependencies installed
- **PostgreSQL database configured**: Database created with three tables (products, sales, purchase_orders)
- **Streamlit configuration**: Configured to run on port 5000 with proper host settings for Replit proxy
- **Workflow configured**: "BizTrackPro" workflow running Streamlit on port 5000
- **Deployment configured**: Autoscale deployment setup for production use
- **Git ignore added**: Python-specific .gitignore file created

## Running the Application

### Development
The application runs automatically via the "BizTrackPro" workflow. The Streamlit app is accessible on port 5000 and integrates with Replit's PostgreSQL database using the DATABASE_URL environment variable.

### Database Tables
- **products**: Stores product information including pricing, stock levels, and reorder thresholds
- **sales**: Records all sales transactions with profit tracking
- **purchase_orders**: Manages incoming stock orders with status tracking

### Key Features
- Product catalog with image support
- Inventory management with low-stock alerts
- Sales recording and reporting
- Purchase order tracking
- Financial dashboard with profit/revenue analytics
- Multi-month trend analysis
- CSV export functionality