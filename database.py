"""
Database module for Doctor Appointment Booking and Management System.

Handles all SQLite database operations for:
- User management (registration, login)
- Doctor records
- Patient records
- Appointment records

Uses parameterized queries to prevent SQL injection.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Database:
    """
    Manages SQLite database operations for the Doctor Appointment System.
    """
    
    def __init__(self, db_path='instance/doctor_appointment.db'):
        """
        Initialize the database.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        
        # Ensure the instance directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create tables if they don't exist
        self.create_tables()
        
        # Seed realistic hospital data if empty
        self.seed_sample_data()
    
    def get_connection(self):
        """
        Get a connection to the SQLite database.
        
        Returns:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    
    def create_tables(self):
        """Create all required tables in the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Users table for authentication
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('Admin', 'Patient')) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Doctors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INTEGER PRIMARY KEY,
                    doctor_name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    available_day TEXT,
                    available_time TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Patients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY,
                    patient_name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date TEXT NOT NULL,
                    appointment_time TEXT NOT NULL,
                    status TEXT CHECK(status IN ('Booked', 'Cancelled', 'Completed')) DEFAULT 'Booked',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            conn.commit()
            print("[OK] Database tables created successfully")
        
        except Exception as e:
            print(f"[ERROR] Error creating tables: {e}")
        
        finally:
            conn.close()
    
    # ========== USER OPERATIONS ==========
    
    def register_user(self, full_name, email, password, role):
        """
        Register a new user.
        
        Args:
            full_name (str): User's full name
            email (str): User's email (must be unique)
            password (str): User's password (will be hashed)
            role (str): User's role ('Admin' or 'Patient')
        
        Returns:
            dict: {'success': bool, 'message': str, 'user_id': int or None}
        """
        try:
            # Check if email already exists
            if self.get_user_by_email(email):
                return {'success': False, 'message': 'Email already registered'}
            
            # Hash the password
            hashed_password = generate_password_hash(password)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (full_name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', (full_name, email, hashed_password, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': 'User registered successfully', 'user_id': user_id}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def login_user(self, email, password):
        """
        Authenticate a user.
        
        Args:
            email (str): User's email
            password (str): User's password (plain text)
        
        Returns:
            dict: {'success': bool, 'message': str, 'user': dict or None}
        """
        try:
            user = self.get_user_by_email(email)
            
            if not user:
                return {'success': False, 'message': 'Email not found'}
            
            # Check password
            if not check_password_hash(user['password'], password):
                return {'success': False, 'message': 'Invalid password'}
            
            # Return user info (without password)
            user_data = {
                'id': user['id'],
                'full_name': user['full_name'],
                'email': user['email'],
                'role': user['role']
            }
            
            return {'success': True, 'message': 'Login successful', 'user': user_data}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_user_by_email(self, email):
        """
        Get user by email.
        
        Args:
            email (str): User's email
        
        Returns:
            dict: User record if found, None otherwise
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()
            
            return dict(user) if user else None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    # ========== DOCTOR OPERATIONS ==========
    
    def get_next_doctor_id(self):
        """Get next available doctor ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(doctor_id) FROM doctors')
            max_id = cursor.fetchone()[0]
            conn.close()
            return (max_id + 1) if max_id else 101
        except Exception:
            return 101

    def add_doctor(self, doctor_id, doctor_name, specialization, phone, email, available_day, available_time):
        """
        Add a new doctor.
        
        Args:
            doctor_id (int): Unique doctor ID (or None to auto-generate)
            doctor_name (str): Doctor's name
            specialization (str): Doctor's specialization
            phone (str): Doctor's phone number
            email (str): Doctor's email
            available_day (str): Available day
            available_time (str): Available time
        
        Returns:
            dict: {'success': bool, 'message': str, 'doctor_id': int}
        """
        try:
            if not doctor_id:
                doctor_id = self.get_next_doctor_id()
            else:
                doctor_id = int(doctor_id)

            # Check if doctor ID already exists
            if self.get_doctor_by_id(doctor_id):
                return {'success': False, 'message': f'Doctor ID {doctor_id} already exists'}
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO doctors 
                (doctor_id, doctor_name, specialization, phone, email, available_day, available_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (doctor_id, doctor_name, specialization, phone, email, available_day, available_time))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': f'Doctor {doctor_name} added successfully (ID: {doctor_id})', 'doctor_id': doctor_id}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM doctors WHERE doctor_id = ?', (doctor_id,))
            doctor = cursor.fetchone()
            conn.close()
            
            return dict(doctor) if doctor else None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_all_doctors(self):
        """Get all doctors."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM doctors ORDER BY doctor_id')
            doctors = cursor.fetchall()
            conn.close()
            
            return [dict(doc) for doc in doctors]
        
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def delete_doctor(self, doctor_id):
        """Delete a doctor and associated appointments."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM appointments WHERE doctor_id = ?', (doctor_id,))
            cursor.execute('DELETE FROM doctors WHERE doctor_id = ?', (doctor_id,))
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Doctor deleted successfully'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ========== PATIENT OPERATIONS ==========
    
    def get_next_patient_id(self):
        """Get next available patient ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(patient_id) FROM patients')
            max_id = cursor.fetchone()[0]
            conn.close()
            return (max_id + 1) if max_id else 201
        except Exception:
            return 201

    def add_patient(self, patient_id, patient_name, age, gender, phone, email):
        """
        Add a new patient.
        
        Args:
            patient_id (int): Unique patient ID (or None to auto-generate)
            patient_name (str): Patient's name
            age (int): Patient's age
            gender (str): Patient's gender
            phone (str): Patient's phone number
            email (str): Patient's email
        
        Returns:
            dict: {'success': bool, 'message': str, 'patient_id': int}
        """
        try:
            if not patient_id:
                patient_id = self.get_next_patient_id()
            else:
                patient_id = int(patient_id)

            # Check if patient ID already exists
            if self.get_patient_by_id(patient_id):
                return {'success': False, 'message': f'Patient ID {patient_id} already exists'}
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO patients 
                (patient_id, patient_name, age, gender, phone, email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (patient_id, patient_name, age, gender, phone, email))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': f'Patient {patient_name} registered successfully (ID: {patient_id})', 'patient_id': patient_id}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_patient_by_id(self, patient_id):
        """Get patient by ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            patient = cursor.fetchone()
            conn.close()
            
            return dict(patient) if patient else None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_all_patients(self):
        """Get all patients."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM patients ORDER BY patient_id')
            patients = cursor.fetchall()
            conn.close()
            
            return [dict(patient) for patient in patients]
        
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def delete_patient(self, patient_id):
        """Delete a patient and associated appointments."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM appointments WHERE patient_id = ?', (patient_id,))
            cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Patient deleted successfully'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ========== APPOINTMENT OPERATIONS ==========
    
    def get_next_appointment_id(self):
        """Get next available appointment ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(appointment_id) FROM appointments')
            max_id = cursor.fetchone()[0]
            conn.close()
            return (max_id + 1) if max_id else 1
        except Exception:
            return 1

    def add_appointment(self, appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status='Booked'):
        """
        Add a new appointment.
        
        Args:
            appointment_id (int): Unique appointment ID (or None to auto-generate)
            patient_id (int): Patient's ID
            doctor_id (int): Doctor's ID
            appointment_date (str): Appointment date
            appointment_time (str): Appointment time
            status (str): Appointment status (default: 'Booked')
        
        Returns:
            dict: {'success': bool, 'message': str, 'appointment_id': int}
        """
        try:
            if not appointment_id:
                appointment_id = self.get_next_appointment_id()
            else:
                appointment_id = int(appointment_id)

            # Check if appointment ID already exists
            if self.get_appointment_by_id(appointment_id):
                return {'success': False, 'message': f'Appointment ID {appointment_id} already exists'}
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO appointments 
                (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': f'Appointment booked successfully (ID: #{appointment_id})', 'appointment_id': appointment_id}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_appointment_by_id(self, appointment_id):
        """Get appointment by ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM appointments WHERE appointment_id = ?', (appointment_id,))
            appointment = cursor.fetchone()
            conn.close()
            
            return dict(appointment) if appointment else None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_all_appointments(self):
        """Get all appointments."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM appointments ORDER BY appointment_id')
            appointments = cursor.fetchall()
            conn.close()
            
            return [dict(appt) for appt in appointments]
        
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def cancel_appointment(self, appointment_id):
        """Cancel an appointment."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', ('Cancelled', appointment_id))
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': 'Appointment cancelled successfully'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def complete_appointment(self, appointment_id):
        """Mark an appointment as completed."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', ('Completed', appointment_id))
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': f'Appointment #{appointment_id} marked as Completed'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def update_appointment_status(self, appointment_id, status):
        """Update appointment status (Booked, Completed, Cancelled)."""
        try:
            if status not in ('Booked', 'Completed', 'Cancelled'):
                return {'success': False, 'message': 'Invalid status'}
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', (status, appointment_id))
            conn.commit()
            conn.close()
            return {'success': True, 'message': f'Appointment #{appointment_id} updated to {status}'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def delete_appointment(self, appointment_id):
        """Delete an appointment."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM appointments WHERE appointment_id = ?', (appointment_id,))
            conn.commit()
            conn.close()
            
            return {'success': True, 'message': 'Appointment deleted successfully'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def seed_sample_data(self):
        """Seed realistic hospital doctors, patients, appointments, and admin account if empty."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 1. Admin and Demo Patients
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Admin'")
            has_admin = cursor.fetchone()[0] > 0
            if not has_admin:
                self.register_user("Hospital Administrator", "admin@hospital.com", "admin123", "Admin")

            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                self.register_user("Alice Smith", "alice@example.com", "password123", "Patient")
            
            # 2. Doctors across clinical & surgical divisions
            cursor.execute("SELECT COUNT(*) FROM doctors")
            if cursor.fetchone()[0] == 0:
                doctors = [
                    (101, "Dr. Sarah Jenkins", "Cardiology", "555-0101", "jenkins@hospital.com", "Monday - Friday", "09:00 - 14:00"),
                    (102, "Dr. Michael Chen", "Neurology", "555-0102", "chen@hospital.com", "Tuesday - Saturday", "10:00 - 16:00"),
                    (103, "Dr. Emily Taylor", "Orthopedics", "555-0103", "taylor@hospital.com", "Monday - Thursday", "08:30 - 13:30"),
                    (104, "Dr. Robert Patel", "General Medicine", "555-0104", "patel@hospital.com", "Daily", "09:00 - 17:00"),
                    (105, "Dr. Amanda Ross", "General Surgery", "555-0105", "ross@hospital.com", "Wednesday - Sunday", "11:00 - 18:00")
                ]
                for doc in doctors:
                    self.add_doctor(*doc)
            
            # 3. Patients
            cursor.execute("SELECT COUNT(*) FROM patients")
            if cursor.fetchone()[0] == 0:
                patients = [
                    (201, "Johnathan Doe", 45, "Male", "555-0201", "john.doe@email.com"),
                    (202, "Maria Gonzalez", 38, "Female", "555-0202", "maria.g@email.com"),
                    (203, "David Miller", 62, "Male", "555-0203", "d.miller@email.com"),
                    (204, "Sophia Patel", 29, "Female", "555-0204", "spatel@email.com")
                ]
                for p in patients:
                    self.add_patient(*p)
            
            # 4. Appointments
            cursor.execute("SELECT COUNT(*) FROM appointments")
            if cursor.fetchone()[0] == 0:
                appts = [
                    (1, 201, 101, "2026-10-10", "10:00 AM"),
                    (2, 202, 102, "2026-10-10", "11:30 AM"),
                    (3, 203, 103, "2026-10-11", "09:15 AM"),
                    (4, 204, 104, "2026-10-11", "02:00 PM")
                ]
                for a in appts:
                    self.add_appointment(*a)
            
            conn.close()
        except Exception as e:
            print(f"[ERROR] Seeding error: {e}")


# Create a global database instance
db = Database()
