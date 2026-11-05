# Doctor Appointment Booking and Hospital Management System

## Comprehensive Hospital Operations, Clinical Hierarchy & Indoor Navigation Platform

### Project Objective

The **Doctor Appointment Booking and Hospital Management System** is a full-featured clinical management and patient intake platform built with Python, Flask, and SQLite. The system coordinates hospital workflows: doctor scheduling, patient registrations, multi-tier clinical department hierarchies, waiting room triage calling, instant medical staff search, and campus indoor walking directions.

---

### Core Functional Modules

1. **User Authentication & Role-Based Access Control**
   - User registration (Admin and Patient roles)
   - Secure credential encryption and session management

2. **Doctor & Medical Specialist Management**
   - Register medical practitioners with specialization, consultation days, and hours
   - Interactive medical specialist directory with instant Staff ID lookup
   - Direct appointment booking from physician profiles

3. **Patient Registration & Records Register**
   - Register patient demographics, contact info, and medical records
   - Dynamic clinical record registers for real-time updates without system interruption

4. **Appointment Booking & Scheduling**
   - Schedule consultations with specialists
   - Manage appointment status (Booked, Cancelled, Completed)
   - Real-time activity log tracking bookings and cancellations with one-click undo

5. **Hospital Department & Medical Staff Hierarchy (`/tree-demo` / Departments)**
   - **Executive Medical Leadership:** Chief Medical Officer (CMO) overseeing hospital governance
   - **Clinical Divisions:** Clinical Services Wing (General Medicine, Cardiology) & Surgical Services Wing (Orthopedics, Neurology)
   - **Doctor Hierarchy in Departments:** Each department displays its Department Head / Lead Consultant, Attending Specialists, and Resident Doctors
   - **Operational Inspection Workflows:** Standard Clinical Walkthroughs, Executive Briefings, and Department Audit Rollups

6. **Indoor Hospital Navigation & Route Guide (`/graph-demo` / Hospital Map)**
   - **Interactive Route Finder:** Get turn-by-turn walking directions between any two departments (e.g. Reception &rarr; Cardiology &rarr; Pharmacy)
   - **Campus Corridor Directory:** View connected hallways for all 9 core hospital zones
   - **Campus Inspection Patrols:** Plan proximity-based or wing-by-wing staff rounds

7. **Patient Waiting Room & Triage Calling (`/queue-demo` / Live Queue)**
   - Orderly first-come, first-served consultation waiting line
   - Single-click "Call Next Patient" into physician examination rooms

8. **Medication Dosage & Prescription Validator (`/expression-handler`)**
   - Syntax verification for complex dosage notations, pediatric regimens, and compounding formulas
   - Real-time bracket enclosure validation `()`, `{}`, `[]` to prevent prescription errors

9. **Hospital Search Directory & Schedule Organizer (`/phase3`, `/search-demo`, `/sort-demo`)**
   - **Flexible Medical Search:** Universal text lookup across doctor names, specializations, and patient notes.
   - **Express ID Direct Lookup:** Instant terminal search pulling up patient files and staff records in 1 to 3 quick checks.
   - **Schedule Priority Organizer:** Fair, non-displacing chronological appointment sequencing that preserves original booking priority for same-hour slots.
   - **Fast Division Roster Sorter:** Ultra-fast in-memory sorting of physician rosters by department, wing, or doctor name.
   - **Walk-In Arrival Desk Sorter:** Instant incremental insertion of walk-in arrivals into daily clinic schedule sheets with zero wasted shifts.
   - **Active Workflow Integration:** Live interactive filter and sort controls across `/doctors`, `/patients`, and `/appointments`.
   - **High-Volume Reception Load Simulator:** Realistic stress tests on reception desk workloads from 50 to 10,000 active patient files.

10. **Clinical Algorithmic Planning (`/phase4`)**
   - **Greedy Appointment Selection:** Select the maximum number of non-overlapping visits for a clinic room.
   - **Dynamic Programming Capacity Optimizer:** Maximize case priority within a consultation-minute budget.
   - **Backtracking Doctor Assignment:** Assign specialty-matched cases without overlapping each doctor's schedule.
   - Interactive workbench and authenticated JSON endpoints demonstrate each algorithm with step traces.

---

### Technologies Used

- **Backend:** Python 3.x, Flask (Web framework), SQLite (Relational database), Werkzeug (Security)
- **Frontend:** HTML5, Modern CSS3 (Custom responsive styling), Jinja2 templates, JavaScript (Vanilla)
- **Architecture:** Model-View-Controller (MVC) with AJAX endpoints

---

### Hospital Leadership & Department Doctor Hierarchy

```
[Executive Leadership]
         │
  Chief Medical Officer (Dr. Arthur Pendelton, MD)
         │
 ┌───────┴────────────────────────┐
 │                                │
[Clinical Services Wing]      [Surgical Services Wing]
Head: Dr. Robert Patel        Head: Dr. Amanda Ross
 │                                │
 ├── General Medicine             ├── Orthopedics
 │   Lead: Dr. Robert Patel       │   Lead: Dr. Emily Taylor
 │   Staff: Dr. David Warner      │   Staff: Dr. James Morrison
 │          Dr. Chloe Bennett     │          Dr. Liam O'Connor
 │                                │
 └── Cardiology                   └── Neurology
     Lead: Dr. Sarah Jenkins          Lead: Dr. Michael Chen
     Staff: Dr. Marcus Vance          Staff: Dr. Elena Rostova
            Dr. Priya Sharma                 Dr. Kevin Tanaka
```

---

### Hospital Indoor Campus Connections

```
[Reception] <─── Corridors ───> [Triage / ER] & [Billing / Discharge]
      │
      └───> [Triage / ER] <───> [General Medicine], [Cardiology], [Orthopedics], [Neurology]
                 │
                 └───> [Specialty Clinics] <───> [Radiology / Lab]
                             │
                             └───> [Radiology / Lab] <───> [Pharmacy] <───> [Billing & Discharge]
```

---

### Quick Start Guide

1. **Activate Virtual Environment:**
   ```powershell
   .\.venv\Scripts\activate
   ```

2. **Run the Flask Application:**
   ```powershell
   python app.py
   ```

3. **Access the Web Interface:**
   - Open browser at `http://127.0.0.1:5001`
   - Default Administrator Account: `admin@hospital.com` / `admin123`
   - Default Patient Account: `alice@example.com` / `password123`
