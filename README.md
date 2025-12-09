# ETL Pipeline & OLAP System for Game Analytics
A complete data engineering project integrating heterogeneous sources (CSV, MongoDB, MySQL) into a unified game analytics data warehouse. Includes a KNIME-built ETL workflow and OLAP operations for multidimensional reporting.

## Features
### ETL Pipeline
- Integrates data from CSV, MongoDB, and MySQL
- Cleans, transforms, and standardizes 20+ interconnected datasets
- Generates surrogate keys and normalized schema mappings
- Outputs consolidated fact and dimension tables for warehouse ingestion
- Built using KNIME Analytics Platform

### OLAP Operations
Implemented using Python + SQL:
- Slice
- Dice
- Roll-up
- Drill-down
- Custom analytical reports (retention, engagement, sales trends)

## Technologies Used
- KNIME Analytics Platform
- Python, Pandas
- MySQL, MongoDB, CSVs
- Jupyter Notebook
