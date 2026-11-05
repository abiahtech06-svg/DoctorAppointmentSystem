
"""
Doctor Appointment Booking and Management System - Flask Application.

This is the main Flask application that provides:
- Web interface for the appointment system
- User authentication and authorization
- Doctor, Patient, and Appointment management
- Phase 1 data structures demonstration

Phase 1 Features:
- Linked List for data storage and demonstration
- Stack for appointment action tracking
- Queue for patient waiting management
- Expression validation using Stack
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
from database import db
from data_structures import (
    LinkedList, Stack, Queue,
    TreeNode, BinaryTree, BinarySearchTree, Graph
)
from algorithms import (
    ExpressionValidator,
    linear_search, binary_search, compare_search_algorithms,
    merge_sort, quick_sort, insertion_sort, compare_sorting_algorithms,
    greedy_appointment_selection, optimize_clinic_capacity,
    assign_cases_backtracking
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'doctor_appointment_system_phase1_key'

@app.context_processor
def inject_global_context():
    """Inject current year dynamically into all templates."""
    from datetime import datetime
    return {'current_year': datetime.now().year}

# Initialize data structures for Phase 1 demonstration
doctors_linked_list = LinkedList()
patients_linked_list = LinkedList()
appointments_linked_list = LinkedList()
appointment_actions_stack = Stack()
patient_waiting_queue = Queue()
expression_validator = ExpressionValidator()

# Initialize data structures for Phase 2 demonstration (CLO2)
hospital_hierarchy_tree = BinaryTree("Chief Medical Officer")
doctor_bst = BinarySearchTree()
hospital_graph = Graph(directed=False)



# ========== AUTHENTICATION DECORATORS ==========

def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('login'))
        
        role = session.get('role')
        if role != 'Admin':
            user = db.get_user_by_email(session.get('email'))
            if not user or user.get('role') != 'Admin':
                flash('Admin access required', 'error')
                return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function


# ========== HELPER FUNCTIONS ==========

def load_linked_lists_from_db():
    """Load all data from database into Linked Lists."""
    global doctors_linked_list, patients_linked_list, appointments_linked_list
    
    # Clear existing linked lists
    doctors_linked_list = LinkedList()
    patients_linked_list = LinkedList()
    appointments_linked_list = LinkedList()
    
    # Load doctors
    for doctor in db.get_all_doctors():
        doctors_linked_list.insert(doctor)
    
    # Load patients
    for patient in db.get_all_patients():
        patients_linked_list.insert(patient)
    
    # Load appointments
    for appointment in db.get_all_appointments():
        appointments_linked_list.insert(appointment)


def populate_phase2_structures():
    """Load records into Phase 2 data structures (Tree, BST, Graph)."""
    global hospital_hierarchy_tree, doctor_bst, hospital_graph
    
    # 1. Binary Search Tree (BST) for Doctors
    doctor_bst = BinarySearchTree()
    for doctor in db.get_all_doctors():
        doctor_record = dict(doctor) if not isinstance(doctor, dict) else doctor
        doctor_bst.insert(doctor_record['doctor_id'], doctor_record)
    
    # 2. Binary Tree for Hospital Organizational Hierarchy
    hospital_hierarchy_tree = BinaryTree("Chief Medical Officer")
    hospital_hierarchy_tree.insert("Clinical Services")
    hospital_hierarchy_tree.insert("Surgical Services")
    hospital_hierarchy_tree.insert("General Medicine")
    hospital_hierarchy_tree.insert("Cardiology")
    hospital_hierarchy_tree.insert("Orthopedics")
    hospital_hierarchy_tree.insert("Neurology")
    
    # 3. Graph for Hospital Department Navigation & Referrals
    hospital_graph = Graph(directed=False)
    departments = [
        "Reception",
        "Triage / ER",
        "General Medicine",
        "Cardiology",
        "Orthopedics",
        "Neurology",
        "Radiology / Lab",
        "Pharmacy",
        "Billing & Discharge"
    ]
    for dept in departments:
        hospital_graph.add_vertex(dept)
    
    hospital_graph.add_edge("Reception", "Triage / ER")
    hospital_graph.add_edge("Reception", "Billing & Discharge")
    hospital_graph.add_edge("Triage / ER", "General Medicine")
    hospital_graph.add_edge("Triage / ER", "Cardiology")
    hospital_graph.add_edge("Triage / ER", "Orthopedics")
    hospital_graph.add_edge("Triage / ER", "Neurology")
    hospital_graph.add_edge("General Medicine", "Radiology / Lab")
    hospital_graph.add_edge("Cardiology", "Radiology / Lab")
    hospital_graph.add_edge("Orthopedics", "Radiology / Lab")
    hospital_graph.add_edge("Neurology", "Radiology / Lab")
    hospital_graph.add_edge("Radiology / Lab", "Pharmacy")
    hospital_graph.add_edge("Pharmacy", "Billing & Discharge")


def ensure_phase2_structures():
    """Ensure hierarchical and graph data structures are populated."""
    global hospital_hierarchy_tree, doctor_bst, hospital_graph
    if (hospital_graph is None or len(hospital_graph.vertices) == 0 or
        hospital_hierarchy_tree is None or
        doctor_bst is None or doctor_bst.get_size() == 0):
        populate_phase2_structures()


def get_dataset_items(dataset_type):
    """Retrieve records as list of dictionaries for Phase 3 sorting and searching."""
    if dataset_type == 'doctors':
        return [dict(d) for d in db.get_all_doctors()]
    elif dataset_type == 'patients':
        return [dict(p) for p in db.get_all_patients()]
    elif dataset_type == 'appointments':
        appts = [dict(a) for a in db.get_all_appointments()]
        for a in appts:
            doc = db.get_doctor_by_id(a['doctor_id'])
            pat = db.get_patient_by_id(a['patient_id'])
            a['doctor_name'] = doc['doctor_name'] if doc else 'Unknown'
            a['patient_name'] = pat['patient_name'] if pat else 'Unknown'
            a['specialization'] = doc['specialization'] if doc else 'General Medicine'
        return appts
    return []


def initialize_app_state():
    """Populate the database-backed structures used by the app at startup."""
    try:
        db.create_tables()
        load_linked_lists_from_db()
        populate_phase2_structures()
        return True
    except Exception as exc:
        print(f"[WARN] Deferred initial data load: {exc}")
        return False


# Initialize structures when the module is imported or the app boots.
initialize_app_state()


def format_record_for_display(record):
    """Format database record for display in Linked List."""
    if isinstance(record, dict):
        # Get first non-null value as display text
        for key, value in record.items():
            if key not in ['created_at'] and value:
                return f"{key}:{value}"
        return str(record)
    return str(record)


# ========== HOME AND AUTHENTICATION ==========

@app.route('/favicon.ico')
def favicon():
    """Return an empty favicon response to prevent noisy missing-favicon 404s."""
    return '', 204


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'Patient')
        
        # Validation
        if not all([full_name, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 4:
            flash('Password must be at least 4 characters', 'error')
            return redirect(url_for('register'))
        
        # Register user
        result = db.register_user(full_name, email, password, role)
        
        if result['success']:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return redirect(url_for('login'))
        
        # Authenticate user
        result = db.login_user(email, password)
        
        if result['success']:
            user = result['user']
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            
            flash(f'Welcome {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


# ========== MAIN DASHBOARD ==========

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard after login."""
    # Load data for statistics
    doctors = db.get_all_doctors()
    patients = db.get_all_patients()
    appointments = db.get_all_appointments()
    waiting_patients = patient_waiting_queue.display()
    
    booked_count = sum(1 for a in appointments if a.get('status') == 'Booked')
    completed_count = sum(1 for a in appointments if a.get('status') == 'Completed')
    cancelled_count = sum(1 for a in appointments if a.get('status') == 'Cancelled')
    recent_actions = appointment_actions_stack.display()[:6]
    
    # Enrich recent appointments
    recent_appts = []
    for appt in appointments[-6:]:
        appt_dict = dict(appt)
        doc = db.get_doctor_by_id(appt_dict['doctor_id'])
        pat = db.get_patient_by_id(appt_dict['patient_id'])
        appt_dict['doctor_name'] = doc['doctor_name'] if doc else 'Doctor'
        appt_dict['patient_name'] = pat['patient_name'] if pat else 'Patient'
        recent_appts.append(appt_dict)
    recent_appts.reverse()

    stats = {
        'total_doctors': len(doctors),
        'total_patients': len(patients),
        'total_appointments': len(appointments),
        'booked_appointments': booked_count,
        'completed_appointments': completed_count,
        'cancelled_appointments': cancelled_count,
        'waiting_count': len(waiting_patients)
    }
    
    return render_template(
        'dashboard.html',
        stats=stats,
        user=session,
        waiting_patients=waiting_patients,
        recent_actions=recent_actions,
        recent_appointments=recent_appts,
        doctors=doctors[:6]
    )


# ========== DOCTOR MANAGEMENT ==========

@app.route('/doctors')
@login_required
def doctors_list():
    """Display all doctors with real-world searching (Linear/Binary) and sorting (Merge/Quick/Insertion)."""
    raw_doctors = [dict(d) for d in db.get_all_doctors()]
    sort_mode = request.args.get('sort', 'default')
    sort_alg = request.args.get('algorithm', 'merge')
    sort_by = request.args.get('sort_by', 'id')
    reverse = request.args.get('order', 'asc') == 'desc'
    
    search_query = request.args.get('search_query', '').strip()
    search_alg = request.args.get('search_alg', 'linear')
    search_by = request.args.get('search_by', 'id')
    
    sort_metrics = None
    search_metrics = None
    
    # 1. Search filter if requested
    if search_query:
        if search_alg == 'binary' and search_by == 'id':
            # Pre-sort by ID for binary search
            sorted_for_search = sorted(raw_doctors, key=lambda d: d['doctor_id'])
            search_res = binary_search(sorted_for_search, search_query, key_func=lambda d: d['doctor_id'], is_sorted=True)
            search_metrics = search_res
            doctors = [search_res['item']] if search_res['found'] else []
        elif search_alg == 'binary' and search_by == 'name':
            sorted_for_search = sorted(raw_doctors, key=lambda d: d['doctor_name'].lower())
            search_res = binary_search(sorted_for_search, search_query, key_func=lambda d: d['doctor_name'].lower(), is_sorted=True)
            search_metrics = search_res
            doctors = [search_res['item']] if search_res['found'] else []
        else:
            # Linear search (supports partial match)
            key_fn = (lambda d: d['doctor_id']) if search_by == 'id' else ((lambda d: d['specialization']) if search_by == 'specialization' else (lambda d: d['doctor_name']))
            search_res = linear_search(raw_doctors, search_query, key_func=key_fn, match_mode='contains')
            search_metrics = search_res
            doctors = [search_res['item']] if search_res['found'] else []
    else:
        doctors = raw_doctors

    # 2. Sorting
    if sort_mode == 'bst':
        sorted_records = doctor_bst.inorder_records()
        doctors = [r['data'] for r in sorted_records if r.get('data')]
        sort_metrics = {
            'algorithm': 'BST Inorder Traversal',
            'comparisons': doctor_bst.get_size(),
            'operations': doctor_bst.get_size(),
            'operation_label': 'Node Visits',
            'execution_time_ms': 0.1,
            'time_complexity': {'average': 'O(n)'},
            'space_complexity': 'O(n)'
        }
    elif sort_mode in ['id', 'name', 'specialization'] or request.args.get('sort_by'):
        field = sort_mode if sort_mode in ['id', 'name', 'specialization'] else sort_by
        key_map = {
            'id': lambda d: d['doctor_id'],
            'name': lambda d: d['doctor_name'],
            'specialization': lambda d: d['specialization']
        }
        key_fn = key_map.get(field, lambda d: d['doctor_id'])
        
        if sort_alg == 'quick':
            sort_res = quick_sort(doctors, key_func=key_fn, reverse=reverse)
        elif sort_alg == 'insertion':
            sort_res = insertion_sort(doctors, key_func=key_fn, reverse=reverse)
        else: # Default is merge sort
            sort_res = merge_sort(doctors, key_func=key_fn, reverse=reverse)
            
        doctors = sort_res['sorted_list']
        sort_metrics = sort_res

    return render_template(
        'doctors.html',
        doctors=doctors,
        sort_mode=sort_mode,
        sort_alg=sort_alg,
        sort_by=sort_by,
        reverse=reverse,
        search_query=search_query,
        search_alg=search_alg,
        search_by=search_by,
        sort_metrics=sort_metrics,
        search_metrics=search_metrics,
        total_doctors=len(raw_doctors)
    )



@app.route('/add-doctor', methods=['GET', 'POST'])
@admin_required
def add_doctor():
    """Add a new doctor."""
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id', '').strip()
        doctor_name = request.form.get('doctor_name', '').strip()
        specialization = request.form.get('specialization', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        available_day = request.form.get('available_day', '').strip()
        available_time = request.form.get('available_time', '').strip()
        
        # Validation
        if not all([doctor_name, specialization, phone, email]):
            flash('Doctor name, specialization, phone, and email are required', 'error')
            return redirect(url_for('add_doctor'))
        
        try:
            doc_id_val = int(doctor_id) if doctor_id else db.get_next_doctor_id()
        except ValueError:
            flash('Doctor ID must be a number', 'error')
            return redirect(url_for('add_doctor'))
        
        # Add to database
        result = db.add_doctor(doc_id_val, doctor_name, specialization, phone, email, available_day, available_time)
        
        if result['success']:
            # Add to Linked List & BST
            doctor_record = {
                'doctor_id': doc_id_val,
                'doctor_name': doctor_name,
                'specialization': specialization,
                'phone': phone,
                'email': email,
                'available_day': available_day,
                'available_time': available_time
            }
            doctors_linked_list.insert(doctor_record)
            doctor_bst.insert(doc_id_val, doctor_record)
            appointment_actions_stack.push(f"Doctor {doctor_name} (ID: {doc_id_val}) registered")
            
            flash(result['message'], 'success')
            return redirect(url_for('doctors_list'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('add_doctor'))
    
    suggested_id = db.get_next_doctor_id()
    return render_template('add_doctor.html', suggested_id=suggested_id)
 
 
@app.route('/doctors/<int:doctor_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_doctor(doctor_id):
    """Delete a doctor record from database and synchronized data structures."""
    if session.get('role') != 'Admin':
        flash('Admin privileges required to delete a doctor', 'error')
        return redirect(url_for('doctors_list'))
        
    result = db.delete_doctor(doctor_id)
    if result['success']:
        load_linked_lists_from_db()
        doctor_bst.delete(doctor_id)
        appointment_actions_stack.push(f"Doctor {doctor_id} removed")
        flash(f"Doctor #{doctor_id} deleted successfully", 'success')
    else:
        flash(result.get('message', 'Failed to delete doctor'), 'error')
        
    return redirect(url_for('doctors_list'))
 
 
# ========== PATIENT MANAGEMENT ==========

@app.route('/patients')
@login_required
def patients_list():
    """Display all patients with Phase 3 sorting (Merge/Quick/Insertion) and searching (Linear/Binary)."""
    raw_patients = [dict(p) for p in db.get_all_patients()]
    sort_by = request.args.get('sort_by')
    sort_alg = request.args.get('algorithm', 'merge')
    reverse = request.args.get('order', 'asc') == 'desc'
    
    search_query = request.args.get('search_query', '').strip()
    search_alg = request.args.get('search_alg', 'linear')
    search_by = request.args.get('search_by', 'name')
    
    sort_metrics = None
    search_metrics = None
    
    # 1. Search
    if search_query:
        if search_alg == 'binary' and search_by == 'id':
            sorted_p = sorted(raw_patients, key=lambda x: x['patient_id'])
            search_res = binary_search(sorted_p, search_query, key_func=lambda x: x['patient_id'], is_sorted=True)
            search_metrics = search_res
            patients = [search_res['item']] if search_res['found'] else []
        elif search_alg == 'binary' and search_by == 'name':
            sorted_p = sorted(raw_patients, key=lambda x: x['patient_name'].lower())
            search_res = binary_search(sorted_p, search_query, key_func=lambda x: x['patient_name'].lower(), is_sorted=True)
            search_metrics = search_res
            patients = [search_res['item']] if search_res['found'] else []
        else:
            key_fn = (lambda x: x['patient_id']) if search_by == 'id' else (lambda x: x['patient_name'])
            search_res = linear_search(raw_patients, search_query, key_func=key_fn, match_mode='contains')
            search_metrics = search_res
            patients = [search_res['item']] if search_res['found'] else []
    else:
        patients = raw_patients
        
    # 2. Sort
    if sort_by:
        key_map = {
            'id': lambda x: x['patient_id'],
            'name': lambda x: x['patient_name'],
            'age': lambda x: x['age'] or 0
        }
        key_fn = key_map.get(sort_by, lambda x: x['patient_id'])
        if sort_alg == 'quick':
            sort_res = quick_sort(patients, key_func=key_fn, reverse=reverse)
        elif sort_alg == 'insertion':
            sort_res = insertion_sort(patients, key_func=key_fn, reverse=reverse)
        else:
            sort_res = merge_sort(patients, key_func=key_fn, reverse=reverse)
            
        patients = sort_res['sorted_list']
        sort_metrics = sort_res
        
    return render_template(
        'patients.html',
        patients=patients,
        sort_by=sort_by,
        sort_alg=sort_alg,
        reverse=reverse,
        search_query=search_query,
        search_alg=search_alg,
        search_by=search_by,
        sort_metrics=sort_metrics,
        search_metrics=search_metrics,
        total_patients=len(raw_patients)
    )


@app.route('/add-patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    """Register a new patient."""
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', '').strip()
        patient_name = request.form.get('patient_name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validation
        if not all([patient_name, age, gender, phone, email]):
            flash('Patient name, age, gender, phone, and email are required', 'error')
            return redirect(url_for('add_patient'))
        
        try:
            pat_id_val = int(patient_id) if patient_id else db.get_next_patient_id()
            age_val = int(age)
        except ValueError:
            flash('Patient ID and Age must be numbers', 'error')
            return redirect(url_for('add_patient'))
        
        # Add to database
        result = db.add_patient(pat_id_val, patient_name, age_val, gender, phone, email)
        
        if result['success']:
            # Add to Linked List
            patient_record = {
                'patient_id': pat_id_val,
                'patient_name': patient_name,
                'age': age_val,
                'gender': gender,
                'phone': phone,
                'email': email
            }
            patients_linked_list.insert(patient_record)
            
            # Automatically check in patient to live waiting queue
            patient_waiting_queue.enqueue(patient_record)
            appointment_actions_stack.push(f"Patient {patient_name} (ID: {pat_id_val}) registered and checked in to queue")
            
            flash(f"Patient {patient_name} registered and checked in to waiting line! (ID: {pat_id_val})", 'success')
            return redirect(url_for('patients_list'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('add_patient'))
    
    suggested_id = db.get_next_patient_id()
    return render_template('add_patient.html', suggested_id=suggested_id)


@app.route('/checkin-patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def checkin_patient(patient_id):
    """Check in a registered patient into the live waiting room queue."""
    patient = db.get_patient_by_id(patient_id)
    if not patient:
        flash(f'Patient #{patient_id} not found', 'error')
        return redirect(url_for('patients_list'))
        
    patient_record = {
        'patient_id': patient['patient_id'],
        'patient_name': patient['patient_name'],
        'age': patient['age'],
        'gender': patient['gender'],
        'phone': patient['phone'],
        'email': patient['email']
    }
    patient_waiting_queue.enqueue(patient_record)
    appointment_actions_stack.push(f"Patient {patient['patient_name']} (#{patient_id}) checked in to waiting line")
    flash(f"✓ {patient['patient_name']} (#{patient_id}) successfully checked in to the Live Waiting Room!", 'success')
    return redirect(url_for('queue_demo'))


@app.route('/patients/<int:patient_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_patient(patient_id):
    """Delete a patient record from database and synchronized data structures."""
    result = db.delete_patient(patient_id)
    if result['success']:
        load_linked_lists_from_db()
        appointment_actions_stack.push(f"Patient {patient_id} removed")
        flash(f"Patient #{patient_id} deleted successfully", 'success')
    else:
        flash(result.get('message', 'Failed to delete patient'), 'error')
        
    return redirect(url_for('patients_list'))


# ========== APPOINTMENT MANAGEMENT ==========

@app.route('/appointments')
@login_required
def appointments_list():
    """Display all appointments with hospital department routes and Phase 3 sorting/searching."""
    raw_appointments = db.get_all_appointments()
    appointments = []
    
    # Enrich appointments with doctor, patient, department, and hospital navigation data
    for appt in raw_appointments:
        appt_dict = dict(appt)
        doctor = db.get_doctor_by_id(appt_dict['doctor_id'])
        patient = db.get_patient_by_id(appt_dict['patient_id'])
        
        appt_dict['doctor_name'] = doctor['doctor_name'] if doctor else 'Unknown'
        appt_dict['patient_name'] = patient['patient_name'] if patient else 'Unknown'
        
        spec = doctor['specialization'] if doctor else 'General Medicine'
        appt_dict['specialization'] = spec
        
        # Match department in hospital graph
        dept = 'General Medicine'
        for v in hospital_graph.vertices:
            if v.lower() in spec.lower() or spec.lower() in v.lower():
                dept = v
                break
        appt_dict['department'] = dept
        
        # Determine hospital division from binary tree
        div_info = hospital_hierarchy_tree.get_department_division(dept)
        appt_dict['division'] = div_info.get('division', 'Clinical Services')
        appt_dict['wing'] = div_info.get('wing', 'Main Wing')
        appointments.append(appt_dict)
        
    sort_by = request.args.get('sort_by')
    sort_alg = request.args.get('algorithm', 'merge')
    reverse = request.args.get('order', 'asc') == 'desc'
    
    search_query = request.args.get('search_query', '').strip()
    search_alg = request.args.get('search_alg', 'linear')
    search_by = request.args.get('search_by', 'id')
    
    sort_metrics = None
    search_metrics = None
    
    # 1. Search
    if search_query:
        if search_alg == 'binary' and search_by == 'id':
            sorted_appts = sorted(appointments, key=lambda x: x['appointment_id'])
            search_res = binary_search(sorted_appts, search_query, key_func=lambda x: x['appointment_id'], is_sorted=True)
            search_metrics = search_res
            appointments = [search_res['item']] if search_res['found'] else []
        else:
            key_fn = (lambda x: x['appointment_id']) if search_by == 'id' else ((lambda x: x['patient_name']) if search_by == 'patient' else ((lambda x: x['doctor_name']) if search_by == 'doctor' else (lambda x: x['appointment_date'])))
            search_res = linear_search(appointments, search_query, key_func=key_fn, match_mode='contains')
            search_metrics = search_res
            appointments = [search_res['item']] if search_res['found'] else []

    # 2. Sort (Stable Merge Sort is ideal for chronological appointment schedules)
    if sort_by:
        key_map = {
            'id': lambda x: x['appointment_id'],
            'date': lambda x: f"{x['appointment_date']} {x['appointment_time']}",
            'patient': lambda x: x['patient_name'],
            'doctor': lambda x: x['doctor_name'],
            'status': lambda x: x['status']
        }
        key_fn = key_map.get(sort_by, lambda x: x['appointment_id'])
        if sort_alg == 'quick':
            sort_res = quick_sort(appointments, key_func=key_fn, reverse=reverse)
        elif sort_alg == 'insertion':
            sort_res = insertion_sort(appointments, key_func=key_fn, reverse=reverse)
        else:
            sort_res = merge_sort(appointments, key_func=key_fn, reverse=reverse)
        appointments = sort_res['sorted_list']
        sort_metrics = sort_res

    return render_template(
        'appointments.html',
        appointments=appointments,
        sort_by=sort_by,
        sort_alg=sort_alg,
        reverse=reverse,
        search_query=search_query,
        search_alg=search_alg,
        search_by=search_by,
        sort_metrics=sort_metrics,
        search_metrics=search_metrics,
        total_appointments=len(raw_appointments)
    )


@app.route('/api/hospital/navigation-guide/<int:appointment_id>')
@login_required
def api_hospital_navigation_guide(appointment_id):
    """Calculate the patient's hospital corridor journey from Reception to clinic and onward to Pharmacy/Billing."""
    appt = db.get_appointment_by_id(appointment_id)
    if not appt:
        return jsonify({'error': 'Appointment not found'}), 404
        
    doctor = db.get_doctor_by_id(appt['doctor_id'])
    patient = db.get_patient_by_id(appt['patient_id'])
    
    spec = doctor['specialization'] if doctor else 'General Medicine'
    
    # Match department in graph
    dept = 'General Medicine'
    for v in hospital_graph.vertices:
        if v.lower() in spec.lower() or spec.lower() in v.lower():
            dept = v
            break
            
    # Calculate shortest route from Reception to Doctor's Department using Graph BFS
    route_to_clinic = hospital_graph.find_shortest_path("Reception", dept)
    
    # Calculate onward route from Doctor's Department to Pharmacy
    route_to_pharmacy = hospital_graph.find_shortest_path(dept, "Pharmacy")
    
    # Fetch administrative division from Binary Tree hierarchy
    div_info = hospital_hierarchy_tree.get_department_division(dept)
    
    return jsonify({
        'appointment_id': appointment_id,
        'patient_name': patient['patient_name'] if patient else 'Patient',
        'doctor_name': doctor['doctor_name'] if doctor else 'Doctor',
        'specialization': spec,
        'department': dept,
        'division_info': div_info,
        'route_to_clinic': route_to_clinic,
        'route_to_pharmacy': route_to_pharmacy
    })



@app.route('/add-appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    """Book a new appointment."""
    from datetime import datetime
    if request.method == 'POST':
        appointment_id = request.form.get('appointment_id', '').strip()
        patient_id = request.form.get('patient_id', '').strip()
        doctor_id = request.form.get('doctor_id', '').strip()
        appointment_date = request.form.get('appointment_date', '').strip()
        appointment_time = request.form.get('appointment_time', '').strip()
        
        # Validation
        if not all([patient_id, doctor_id, appointment_date, appointment_time]):
            flash('Patient, doctor, date, and time are required', 'error')
            return redirect(url_for('add_appointment'))
        
        try:
            appt_id_val = int(appointment_id) if appointment_id else db.get_next_appointment_id()
            pat_id_val = int(patient_id)
            doc_id_val = int(doctor_id)
        except ValueError:
            flash('IDs must be numbers', 'error')
            return redirect(url_for('add_appointment'))
        
        # Verify patient and doctor exist
        patient_record = db.get_patient_by_id(pat_id_val)
        if not patient_record:
            flash('Patient not found', 'error')
            return redirect(url_for('add_appointment'))
        
        doctor_record = db.get_doctor_by_id(doc_id_val)
        if not doctor_record:
            flash('Doctor not found', 'error')
            return redirect(url_for('add_appointment'))
        
        # Add to database
        result = db.add_appointment(appt_id_val, pat_id_val, doc_id_val, appointment_date, appointment_time)
        
        if result['success']:
            # Add to Linked List
            appointment_record = {
                'appointment_id': appt_id_val,
                'patient_id': pat_id_val,
                'doctor_id': doc_id_val,
                'date': appointment_date,
                'time': appointment_time
            }
            appointments_linked_list.insert(appointment_record)
            
            # Add action to stack (LIFO - most recent at top)
            action = f"Appointment #{appt_id_val} booked ({patient_record['patient_name']} with {doctor_record['doctor_name']})"
            appointment_actions_stack.push(action)
            
            flash(f"Appointment #{appt_id_val} booked successfully for {patient_record['patient_name']} with {doctor_record['doctor_name']}", 'success')
            return redirect(url_for('appointments_list'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('add_appointment'))
    
    # Get lists for dropdowns and smart defaults
    patients = db.get_all_patients()
    doctors = db.get_all_doctors()
    suggested_id = db.get_next_appointment_id()
    today_date = datetime.now().strftime('%Y-%m-%d')
    selected_doctor_id = request.args.get('doctor_id', type=int)
    selected_patient_id = request.args.get('patient_id', type=int)
    
    return render_template(
        'add_appointment.html',
        patients=patients,
        doctors=doctors,
        suggested_id=suggested_id,
        today_date=today_date,
        selected_doctor_id=selected_doctor_id,
        selected_patient_id=selected_patient_id
    )


@app.route('/complete-appointment/<int:appointment_id>', methods=['POST', 'GET'])
@login_required
def complete_appointment(appointment_id):
    """Mark an appointment as completed."""
    result = db.complete_appointment(appointment_id)
    if result['success']:
        load_linked_lists_from_db()
        appointment_actions_stack.push(f"Appointment #{appointment_id} marked as Completed")
        flash(f"✓ Appointment #{appointment_id} marked as Completed", 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('appointments_list'))


@app.route('/cancel-appointment/<int:appointment_id>', methods=['POST', 'GET'])
@login_required
def cancel_appointment(appointment_id):
    """Cancel an appointment."""
    result = db.cancel_appointment(appointment_id)
    
    if result['success']:
        # Add action to stack
        action = f"Appointment #{appointment_id} cancelled"
        appointment_actions_stack.push(action)
        flash(f"Appointment #{appointment_id} has been cancelled", 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('appointments_list'))


@app.route('/appointments/<int:appointment_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_appointment(appointment_id):
    """Delete an appointment record."""
    result = db.delete_appointment(appointment_id)
    if result['success']:
        load_linked_lists_from_db()
        appointment_actions_stack.push(f"Appointment {appointment_id} removed")
        flash(f"Appointment #{appointment_id} deleted successfully", 'success')
    else:
        flash(result.get('message', 'Failed to delete appointment'), 'error')
        
    return redirect(url_for('appointments_list'))


# ========== PHASE 1 DATA STRUCTURES (LINEAR) ==========

@app.route('/phase1')
@login_required
def phase1():
    """Phase 1 Linear Data Structures Overview."""
    return render_template('phase1.html')


@app.route('/linked-list')
@login_required
def linked_list_demo():
    """Linked list demonstration page."""
    load_linked_lists_from_db()
    doctors = db.get_all_doctors()
    patients = db.get_all_patients()
    appointments = db.get_all_appointments()
    return render_template(
        'linked_list.html',
        doctors=doctors,
        doctors_display=doctors_linked_list.display_as_list(),
        patients=patients,
        patients_display=patients_linked_list.display_as_list(),
        appointments=appointments,
        appointments_display=appointments_linked_list.display_as_list()
    )


@app.route('/stack-demo')
@login_required
def stack_demo():
    """Stack demonstration page."""
    actions = appointment_actions_stack.display()
    return render_template('stack.html', actions=actions)


@app.route('/queue-demo')
@login_required
def queue_demo():
    """Live patient triage waiting queue page."""
    waiting_patients = patient_waiting_queue.display()
    all_patients = db.get_all_patients()
    return render_template('queue.html', waiting_patients=waiting_patients, all_patients=all_patients)


@app.route('/expression-handler')
@login_required
def expression_handler():
    """Expression validator demonstration page."""
    return render_template('expression.html')


# ========== PHASE 2 DATA STRUCTURES (HIERARCHICAL & GRAPH - CLO2) ==========

@app.route('/phase2')
@login_required
def phase2():
    """Phase 2 Hierarchical and Graph Structures Overview."""
    return render_template('phase2.html')


def get_doctor_hierarchy_data():
    """
    Build structured Doctor Hierarchy categorized by Clinical & Surgical Divisions and Departments.
    Includes leadership roles: Chief Medical Officer, Division Heads, Department Heads, and Attending Specialists.
    """
    hierarchy = {
        'cmo': {
            'title': 'Chief Medical Officer',
            'name': 'Dr. Arthur Pendelton, MD',
            'role': 'Executive Medical Director',
            'experience': '25+ Years Experience',
            'email': 'cmo@hospital.com',
            'phone': '555-0100'
        },
        'divisions': [
            {
                'id': 'div-clinical',
                'name': 'Clinical Services Division',
                'head_name': 'Dr. Robert Patel, MD',
                'head_title': 'Chief of Clinical Medicine',
                'wing': 'Clinical Wing - West Block (Floors 1-2)',
                'departments': [
                    {
                        'name': 'General Medicine',
                        'icon': '🩺',
                        'floor': 'Floor 1, Rooms 101-110',
                        'head_doctor': {
                            'id': 104,
                            'name': 'Dr. Robert Patel',
                            'title': 'Department Head & Lead Consultant',
                            'specialization': 'Internal & General Medicine',
                            'phone': '555-0104',
                            'email': 'patel@hospital.com',
                            'schedule': 'Daily (09:00 - 17:00)'
                        },
                        'staff_doctors': [
                            {
                                'name': 'Dr. David Warner',
                                'title': 'Attending Physician',
                                'rank': 'Consultant',
                                'specialization': 'Internal Medicine & Chronic Care',
                                'schedule': 'Mon - Fri (08:00 - 15:00)'
                            },
                            {
                                'name': 'Dr. Chloe Bennett',
                                'title': 'Resident Medical Officer',
                                'rank': 'Resident Physician',
                                'specialization': 'Outpatient & Triage Care',
                                'schedule': 'Mon - Sat (12:00 - 20:00)'
                            }
                        ]
                    },
                    {
                        'name': 'Cardiology',
                        'icon': '❤️',
                        'floor': 'Floor 2, Rooms 201-215',
                        'head_doctor': {
                            'id': 101,
                            'name': 'Dr. Sarah Jenkins',
                            'title': 'Chief of Cardiology & Senior Consultant',
                            'specialization': 'Cardiology',
                            'phone': '555-0101',
                            'email': 'jenkins@hospital.com',
                            'schedule': 'Monday - Friday (09:00 - 14:00)'
                        },
                        'staff_doctors': [
                            {
                                'name': 'Dr. Marcus Vance',
                                'title': 'Senior Cardiovascular Specialist',
                                'rank': 'Associate Consultant',
                                'specialization': 'Interventional Cardiology',
                                'schedule': 'Tue - Sat (10:00 - 16:00)'
                            },
                            {
                                'name': 'Dr. Priya Sharma',
                                'title': 'Cardiology Clinical Fellow',
                                'rank': 'Clinical Fellow',
                                'specialization': 'Echocardiography & Cardiac ICU',
                                'schedule': 'Wed - Sun (08:30 - 14:30)'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'div-surgical',
                'name': 'Surgical Services Division',
                'head_name': 'Dr. Amanda Ross, MD',
                'head_title': 'Chief of Surgery',
                'wing': 'Surgical Wing - East Block (Floors 2-4)',
                'departments': [
                    {
                        'name': 'Orthopedics',
                        'icon': '🦴',
                        'floor': 'Floor 2, Rooms 220-230',
                        'head_doctor': {
                            'id': 103,
                            'name': 'Dr. Emily Taylor',
                            'title': 'Head of Orthopedic Surgery',
                            'specialization': 'Orthopedics',
                            'phone': '555-0103',
                            'email': 'taylor@hospital.com',
                            'schedule': 'Monday - Thursday (08:30 - 13:30)'
                        },
                        'staff_doctors': [
                            {
                                'name': 'Dr. James Morrison',
                                'title': 'Consultant Joint Replacement Surgeon',
                                'rank': 'Senior Consultant',
                                'specialization': 'Arthroplasty & Trauma Surgery',
                                'schedule': 'Mon - Wed (09:00 - 15:00)'
                            },
                            {
                                'name': 'Dr. Liam O\'Connor',
                                'title': 'Orthopedic Surgical Resident',
                                'rank': 'Resident Surgeon',
                                'specialization': 'Musculoskeletal Trauma',
                                'schedule': 'Thu - Sun (11:00 - 19:00)'
                            }
                        ]
                    },
                    {
                        'name': 'Neurology',
                        'icon': '🧠',
                        'floor': 'Floor 3, Rooms 301-312',
                        'head_doctor': {
                            'id': 102,
                            'name': 'Dr. Michael Chen',
                            'title': 'Chief of Neurology & Neuro-Specialist',
                            'specialization': 'Neurology',
                            'phone': '555-0102',
                            'email': 'chen@hospital.com',
                            'schedule': 'Tuesday - Saturday (10:00 - 16:00)'
                        },
                        'staff_doctors': [
                            {
                                'name': 'Dr. Elena Rostova',
                                'title': 'Consultant Neurophysiologist',
                                'rank': 'Senior Consultant',
                                'specialization': 'Stroke & Neurovascular Care',
                                'schedule': 'Mon - Thu (09:00 - 14:00)'
                            },
                            {
                                'name': 'Dr. Kevin Tanaka',
                                'title': 'Neurology Clinical Fellow',
                                'rank': 'Clinical Fellow',
                                'specialization': 'Neuro-Diagnostics & Monitoring',
                                'schedule': 'Tue - Sat (12:00 - 18:00)'
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Merge additional registered database doctors dynamically
    all_db_doctors = db.get_all_doctors()
    for doc in all_db_doctors:
        spec = (doc.get('specialization') or '').lower()
        matched = False
        for div in hierarchy['divisions']:
            for dept in div['departments']:
                dept_name = dept['name'].lower()
                if (dept_name in spec or spec in dept_name) and doc.get('doctor_id') != dept['head_doctor'].get('id'):
                    if not any(s.get('name') == doc.get('doctor_name') for s in dept['staff_doctors']):
                        dept['staff_doctors'].append({
                            'id': doc.get('doctor_id'),
                            'name': doc.get('doctor_name'),
                            'title': 'Staff Specialist',
                            'rank': 'Specialist',
                            'specialization': doc.get('specialization'),
                            'schedule': f"{doc.get('available_day', 'Mon-Fri')} ({doc.get('available_time', '9 AM - 5 PM')})"
                        })
                    matched = True
                    break
            if matched:
                break
                
    return hierarchy


@app.route('/tree-demo')
@login_required
def tree_demo():
    """Hospital Department & Doctor Hierarchy demonstration page."""
    inorder = hospital_hierarchy_tree.inorder_traversal()
    preorder = hospital_hierarchy_tree.preorder_traversal()
    postorder = hospital_hierarchy_tree.postorder_traversal()
    doctor_hierarchy = get_doctor_hierarchy_data()
    return render_template(
        'tree_demo.html',
        tree_data=hospital_hierarchy_tree.to_dict(),
        inorder=inorder,
        preorder=preorder,
        postorder=postorder,
        height=hospital_hierarchy_tree.get_height(),
        doctor_hierarchy=doctor_hierarchy
    )


@app.route('/bst-demo')
@login_required
def bst_demo():
    """Binary Search Tree demonstration page."""
    sorted_doctors = doctor_bst.inorder_records()
    return render_template(
        'bst_demo.html',
        bst_data=doctor_bst.to_dict(),
        sorted_doctors=sorted_doctors,
        total_nodes=doctor_bst.get_size()
    )


@app.route('/graph-demo')
@login_required
def graph_demo():
    """Graph Representation & Traversals demonstration page."""
    ensure_phase2_structures()
    adj_list = hospital_graph.get_adjacency_list()
    adj_matrix = hospital_graph.get_adjacency_matrix()
    summary = hospital_graph.get_graph_summary()
    return render_template(
        'graph_demo.html',
        adj_list=adj_list,
        adj_matrix=adj_matrix,
        summary=summary,
        vertices=hospital_graph.vertices
    )



# ========== API ENDPOINTS FOR AJAX ==========

@app.route('/api/validate-expression', methods=['POST'])
@login_required
def validate_expression():
    """API endpoint to validate an expression."""
    data = request.get_json()
    expression = data.get('expression', '')
    
    if not expression:
        return jsonify({'error': 'Expression cannot be empty'}), 400
    
    # Get detailed analysis
    analysis = expression_validator.get_detailed_analysis(expression)
    
    return jsonify(analysis)


@app.route('/api/linked-list/delete', methods=['POST'])
@login_required
def api_linked_list_delete():
    """API endpoint to delete from Linked List."""
    data = request.get_json()
    list_type = data.get('list_type')  # 'doctors', 'patients', 'appointments'
    record_id = data.get('id')
    
    if list_type == 'doctors':
        result = db.delete_doctor(record_id)
        if result['success']:
            load_linked_lists_from_db()
            doctor_bst.delete(record_id)
    elif list_type == 'patients':
        result = db.delete_patient(record_id)
        if result['success']:
            load_linked_lists_from_db()
    elif list_type == 'appointments':
        result = db.delete_appointment(record_id)
        if result['success']:
            load_linked_lists_from_db()
    else:
        return jsonify({'success': False, 'message': 'Invalid list type'}), 400
    
    return jsonify(result)


@app.route('/api/stack/pop', methods=['POST'])
@login_required
def api_stack_pop():
    """API endpoint to pop from appointment actions stack."""
    top_action = appointment_actions_stack.pop()
    
    if top_action:
        return jsonify({'success': True, 'action': top_action})
    else:
        return jsonify({'success': False, 'message': 'Stack is empty'})


@app.route('/api/queue/dequeue', methods=['POST'])
@login_required
def api_queue_dequeue():
    """API endpoint to dequeue from patient waiting queue."""
    next_patient = patient_waiting_queue.dequeue()
    
    if next_patient:
        return jsonify({'success': True, 'patient': next_patient})
    else:
        return jsonify({'success': False, 'message': 'Queue is empty'})


# ========== PHASE 2 API ENDPOINTS ==========

@app.route('/api/tree/traverse', methods=['POST'])
@login_required
def api_tree_traverse():
    """API endpoint to get step-by-step tree traversal trace."""
    data = request.get_json() or {}
    traversal_type = data.get('traversal_type', 'inorder')
    trace = hospital_hierarchy_tree.get_detailed_traversal_trace(traversal_type)
    return jsonify(trace)


@app.route('/api/bst/search', methods=['POST'])
@login_required
def api_bst_search():
    """API endpoint to search for a Doctor in the BST."""
    data = request.get_json() or {}
    raw_key = data.get('key')
    if raw_key is None or str(raw_key).strip() == '':
        return jsonify({'error': 'Doctor ID is required'}), 400
    try:
        key = int(raw_key)
    except ValueError:
        return jsonify({'error': 'Doctor ID must be an integer'}), 400
    
    found, node, trace = doctor_bst.search(key)
    return jsonify({
        'found': found,
        'key': key,
        'doctor': node.data if node else None,
        'trace': trace
    })


@app.route('/api/bst/insert', methods=['POST'])
@login_required
def api_bst_insert():
    """API endpoint to insert a doctor into the BST."""
    data = request.get_json() or {}
    raw_key = data.get('key')
    name = data.get('name', 'Doctor')
    spec = data.get('specialization', 'General Medicine')
    phone = data.get('phone', 'N/A')
    email = data.get('email', 'N/A')
    
    if not raw_key:
        return jsonify({'error': 'Doctor ID is required'}), 400
    try:
        key = int(raw_key)
    except ValueError:
        return jsonify({'error': 'Doctor ID must be an integer'}), 400
        
    doctor_record = {
        'doctor_id': key,
        'doctor_name': name,
        'specialization': spec,
        'phone': phone,
        'email': email
    }
    inserted = doctor_bst.insert(key, doctor_record)
    return jsonify({
        'success': True,
        'inserted': inserted,
        'message': f"Doctor '{name}' (ID: {key}) successfully indexed in BST.",
        'sorted_doctors': doctor_bst.inorder_records(),
        'bst_data': doctor_bst.to_dict(),
        'total_nodes': doctor_bst.get_size()
    })


@app.route('/api/graph/traverse', methods=['POST'])
@login_required
def api_graph_traverse():
    """API endpoint to run BFS or DFS on the Hospital Graph."""
    data = request.get_json() or {}
    start_vertex = data.get('start_vertex', 'Reception')
    algorithm = data.get('algorithm', 'bfs').lower()
    
    if algorithm == 'bfs':
        result = hospital_graph.bfs(start_vertex)
    elif algorithm == 'dfs':
        result = hospital_graph.dfs(start_vertex)
    else:
        return jsonify({'error': "Algorithm must be 'bfs' or 'dfs'"}), 400
        
    return jsonify(result)


@app.route('/api/graph/route', methods=['POST'])
@login_required
def api_graph_route():
    """API endpoint to find shortest route between two locations in the hospital."""
    data = request.get_json() or {}
    start = data.get('start', 'Reception')
    destination = data.get('destination', 'Pharmacy')
    
    route_data = hospital_graph.find_shortest_path(start, destination)
    if not route_data or not route_data.get('path'):
        return jsonify({
            'error': f"No connected corridor route found between '{start}' and '{destination}'",
            'start': start,
            'destination': destination,
            'path': [],
            'steps_count': 0,
            'directions': []
        }), 404
        
    return jsonify(route_data)


# ========== PHASE 3 SEARCHING & SORTING (CLO2) ==========

@app.route('/phase3')
@login_required
def phase3():
    """Phase 3 Searching and Sorting Operations Overview."""
    doctors = [dict(d) for d in db.get_all_doctors()]
    patients = [dict(p) for p in db.get_all_patients()]
    appointments = get_dataset_items('appointments')
    return render_template(
        'phase3.html',
        total_doctors=len(doctors),
        total_patients=len(patients),
        total_appointments=len(appointments),
        doctors=doctors,
        patients=patients,
        appointments=appointments
    )


@app.route('/search-demo')
@login_required
def search_demo():
    """Interactive Searching Demonstration workbench (Linear vs Binary Search)."""
    doctors = [dict(d) for d in db.get_all_doctors()]
    patients = [dict(p) for p in db.get_all_patients()]
    appointments = get_dataset_items('appointments')
    return render_template(
        'search_demo.html',
        doctors=doctors,
        patients=patients,
        appointments=appointments
    )


@app.route('/sort-demo')
@login_required
def sort_demo():
    """Interactive Sorting Demonstration workbench (Merge vs Quick vs Insertion Sort)."""
    doctors = [dict(d) for d in db.get_all_doctors()]
    patients = [dict(p) for p in db.get_all_patients()]
    appointments = get_dataset_items('appointments')
    return render_template(
        'sort_demo.html',
        doctors=doctors,
        patients=patients,
        appointments=appointments
    )


# ========== PHASE 4 ALGORITHMIC PROBLEM SOLVING (CLO3) ==========

@app.route('/phase4')
@login_required
def phase4():
    """Interactive demonstrations of greedy, dynamic-programming, and backtracking."""
    doctors = [dict(doctor) for doctor in db.get_all_doctors()]
    return render_template('phase4.html', doctors=doctors)


@app.route('/api/phase4/greedy', methods=['POST'])
@login_required
def api_phase4_greedy():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'A JSON object is required.'}), 400
    appointments = data.get('appointments', [])
    if not isinstance(appointments, list):
        return jsonify({'error': 'appointments must be a list.'}), 400
    if len(appointments) > 5000:
        return jsonify({'error': 'appointments must contain no more than 5000 items.'}), 400
    try:
        return jsonify(greedy_appointment_selection(appointments))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@app.route('/api/phase4/dp', methods=['POST'])
@login_required
def api_phase4_dp():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'A JSON object is required.'}), 400
    try:
        capacity = data.get('capacity', 0)
        cases = data.get('cases', [])
        if not isinstance(cases, list):
            raise ValueError("cases must be a list.")
        if len(cases) > 40:
            raise ValueError("cases must contain no more than 40 items.")
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity > 1440:
            raise ValueError("capacity must be an integer between 0 and 1440.")
        return jsonify(optimize_clinic_capacity(cases, capacity))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


@app.route('/api/phase4/backtracking', methods=['POST'])
@login_required
def api_phase4_backtracking():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'A JSON object is required.'}), 400
    doctors = data.get('doctors', [])
    cases = data.get('cases', [])
    if not isinstance(cases, list):
        return jsonify({'error': 'cases must be a list.'}), 400
    if len(cases) > 12:
        return jsonify({'error': "cases must contain no more than 12 items."}), 400
    if not isinstance(doctors, list):
        return jsonify({'error': 'doctors must be a list.'}), 400
    if len(doctors) > 20:
        return jsonify({'error': "doctors must contain no more than 20 items."}), 400
    try:
        return jsonify(assign_cases_backtracking(doctors, cases))
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


# ========== PHASE 3 API ENDPOINTS ==========

@app.route('/api/search/run', methods=['POST'])
@login_required
def api_search_run():
    """API endpoint to execute Linear Search, Binary Search, or Compare both."""
    data = request.get_json() or {}
    dataset_type = data.get('dataset_type', 'doctors')
    target = data.get('target')
    search_by = data.get('search_by', 'id')
    algorithm = data.get('algorithm', 'compare').lower()
    match_mode = data.get('match_mode', 'contains')
    
    if target is None or str(target).strip() == '':
        return jsonify({'error': 'Search target is required'}), 400
        
    # Get items
    if dataset_type == 'custom':
        raw_items = data.get('custom_data', [])
        key_fn = None
    else:
        raw_items = get_dataset_items(dataset_type)
        if dataset_type == 'doctors':
            key_map = {
                'id': lambda x: x.get('doctor_id'),
                'name': lambda x: x.get('doctor_name'),
                'specialization': lambda x: x.get('specialization')
            }
        elif dataset_type == 'patients':
            key_map = {
                'id': lambda x: x.get('patient_id'),
                'name': lambda x: x.get('patient_name')
            }
        else: # appointments
            key_map = {
                'id': lambda x: x.get('appointment_id'),
                'patient': lambda x: x.get('patient_name'),
                'doctor': lambda x: x.get('doctor_name'),
                'date': lambda x: x.get('appointment_date')
            }
        key_fn = key_map.get(search_by, lambda x: x.get(search_by) if isinstance(x, dict) and search_by in x else (x.get('id') if isinstance(x, dict) else x))

    if algorithm == 'linear':
        result = linear_search(raw_items, target, key_func=key_fn, match_mode=match_mode)
    elif algorithm == 'binary':
        result = binary_search(raw_items, target, key_func=key_fn, is_sorted=False)
    else: # compare both
        result = compare_search_algorithms(raw_items, target, key_func=key_fn, match_mode=match_mode)
        
    return jsonify(result)


@app.route('/api/sort/run', methods=['POST'])
@login_required
def api_sort_run():
    """API endpoint to execute Merge Sort, Quick Sort, Insertion Sort, or Compare all."""
    data = request.get_json() or {}
    dataset_type = data.get('dataset_type', 'doctors')
    sort_by = data.get('sort_by', 'id')
    algorithm = data.get('algorithm', 'compare').lower()
    reverse = bool(data.get('reverse', False))
    
    if dataset_type == 'custom':
        raw_items = data.get('custom_data', [])
        key_fn = None
    else:
        raw_items = get_dataset_items(dataset_type)
        if dataset_type == 'doctors':
            key_map = {
                'id': lambda x: x.get('doctor_id', 0),
                'name': lambda x: x.get('doctor_name', ''),
                'specialization': lambda x: x.get('specialization', '')
            }
        elif dataset_type == 'patients':
            key_map = {
                'id': lambda x: x.get('patient_id', 0),
                'name': lambda x: x.get('patient_name', ''),
                'age': lambda x: x.get('age', 0)
            }
        else: # appointments
            key_map = {
                'id': lambda x: x.get('appointment_id', 0),
                'date': lambda x: f"{x.get('appointment_date', '')} {x.get('appointment_time', '')}",
                'patient': lambda x: x.get('patient_name', ''),
                'doctor': lambda x: x.get('doctor_name', ''),
                'status': lambda x: x.get('status', '')
            }
        key_fn = key_map.get(sort_by, lambda x: x.get('id') if isinstance(x, dict) else x)

    if algorithm == 'merge':
        result = merge_sort(raw_items, key_func=key_fn, reverse=reverse)
    elif algorithm == 'quick':
        result = quick_sort(raw_items, key_func=key_fn, reverse=reverse)
    elif algorithm == 'insertion':
        result = insertion_sort(raw_items, key_func=key_fn, reverse=reverse)
    else: # compare
        result = compare_sorting_algorithms(raw_items, key_func=key_fn, reverse=reverse)
        
    return jsonify(result)


@app.route('/api/benchmark/search', methods=['POST'])
@login_required
def api_benchmark_search():
    """Benchmark Linear Search vs Binary Search on custom sized arrays."""
    data = request.get_json() or {}
    try:
        size = int(data.get('size', 1000))
    except (ValueError, TypeError):
        size = 1000
    size = max(10, min(10000, size))  # Bound between 10 and 10,000
    
    pos = data.get('target_position', 'middle')
    arr = list(range(1, size + 1))
    
    if pos == 'best':
        target = 1  # Best case for linear
    elif pos == 'middle':
        target = arr[len(arr) // 2]  # Best/good case for binary
    elif pos == 'worst':
        target = size  # Worst case for linear
    else: # missing
        target = size + 999
        
    comparison = compare_search_algorithms(arr, target)
    return jsonify({
        'dataset_size': size,
        'target': target,
        'position': pos,
        'results': comparison
    })


@app.route('/api/benchmark/sort', methods=['POST'])
@login_required
def api_benchmark_sort():
    """Benchmark Merge Sort, Quick Sort, and Insertion Sort across dataset distributions."""
    import random
    data = request.get_json() or {}
    try:
        size = int(data.get('size', 200))
    except (ValueError, TypeError):
        size = 200
    size = max(10, min(2000, size))  # Bound between 10 and 2,000 for responsive browser execution
    
    distribution = data.get('distribution', 'random')
    if distribution == 'sorted':
        arr = list(range(1, size + 1))
    elif distribution == 'reversed':
        arr = list(range(size, 0, -1))
    elif distribution == 'nearly_sorted':
        arr = list(range(1, size + 1))
        # Swap 5% of elements
        for _ in range(max(1, size // 20)):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
    else: # random
        arr = [random.randint(1, size * 10) for _ in range(size)]
        
    comparison = compare_sorting_algorithms(arr)
    return jsonify({
        'dataset_size': size,
        'distribution': distribution,
        'comparison': comparison
    })


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


# ========== INITIALIZATION ==========

if __name__ == '__main__':
    initialize_app_state()
    app.run(debug=True, host='127.0.0.1', port=5001)
