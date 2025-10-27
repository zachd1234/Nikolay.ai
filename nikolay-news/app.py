#!/usr/bin/env python3
"""
FastAPI backend for Nikolay.ai Hack Event Registration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Nikolay.ai Hack Event Registration", description="API for hack event registration")

# Mount static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Database configuration
db_config = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", ""),
    'database': os.getenv("DB_NAME", "nikolay_hack_event")
}

# Pydantic model for registration
class Registration(BaseModel):
    email: EmailStr
    name: str = None
    organization: str = None

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

# Create database and table if they don't exist
def setup_database():
    connection = get_db_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")
        
        # Create registrations table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255),
                organization VARCHAR(255),
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
        return True
    except Error as e:
        print(f"Error setting up database: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# Root endpoint to serve the HTML invitation
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Read the HTML invitation file
    try:
        with open("hack_event_invitation.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="HTML invitation file not found")

# Registration endpoint
@app.post("/api/register")
async def register(registration: Registration):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor()
    
    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM registrations WHERE email = %s", (registration.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Insert new registration
        query = "INSERT INTO registrations (email, name, organization) VALUES (%s, %s, %s)"
        cursor.execute(query, (registration.email, registration.name, registration.organization))
        connection.commit()
        
        return {"message": "Registration successful", "status": "success"}
    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Get all registrations (admin endpoint)
@app.get("/api/registrations")
async def get_registrations():
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM registrations ORDER BY registration_date DESC")
        registrations = cursor.fetchall()
        return {"registrations": registrations, "count": len(registrations)}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    if not setup_database():
        print("Warning: Failed to set up database. Registration functionality may not work.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
