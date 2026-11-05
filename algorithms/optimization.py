"""Greedy, dynamic-programming, and backtracking algorithms for hospital workflows."""

from typing import Any, Dict, List


def _validate_interval_records(records: List[Dict[str, Any]], label: str) -> None:
    if not isinstance(records, list):
        raise ValueError(f"{label} must be a list.")
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{label}[{index}] must be an object.")
        start = record.get("start")
        end = record.get("end")
        if (isinstance(start, bool) or not isinstance(start, int)
                or isinstance(end, bool) or not isinstance(end, int)):
            raise ValueError(f"{label}[{index}] start and end must be integer minutes.")
        if start < 0 or end <= start:
            raise ValueError(f"{label}[{index}] must have end greater than a non-negative start.")


def greedy_appointment_selection(appointments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Select the maximum number of non-overlapping appointments by earliest finish time."""
    _validate_interval_records(appointments, "appointments")
    ordered = sorted(enumerate(appointments), key=lambda pair: (
        pair[1]["end"], pair[1]["start"], pair[0]
    ))
    selected = []
    trace = []
    last_end = None

    for _, appointment in ordered:
        if last_end is None or appointment["start"] >= last_end:
            selected.append(dict(appointment))
            last_end = appointment["end"]
            action = "selected"
        else:
            action = "skipped"
        if len(trace) < 60:
            trace.append({
                "id": appointment.get("id"),
                "start": appointment["start"],
                "end": appointment["end"],
                "action": action,
                "reason": (
                    "Earliest finishing compatible appointment."
                    if action == "selected"
                    else "Overlaps an already selected appointment."
                )
            })

    return {
        "algorithm": "Greedy Appointment Selection",
        "selected": selected,
        "count": len(selected),
        "trace": trace,
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)"
    }


def optimize_clinic_capacity(cases: List[Dict[str, Any]], capacity: int) -> Dict[str, Any]:
    """Choose the highest-priority set of cases within a consultation-minute budget."""
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
        raise ValueError("capacity must be a non-negative integer.")
    if not isinstance(cases, list):
        raise ValueError("cases must be a list.")

    normalized = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"cases[{index}] must be an object.")
        duration = case.get("duration")
        priority = case.get("priority")
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            raise ValueError(f"cases[{index}] duration must be a positive integer.")
        if isinstance(priority, bool) or not isinstance(priority, int) or priority < 0:
            raise ValueError(f"cases[{index}] priority must be a non-negative integer.")
        normalized.append((duration, priority, case))

    # Each row represents the best priority attainable using the first i cases.
    table = [[0] * (capacity + 1) for _ in range(len(normalized) + 1)]
    trace = []
    for row, (duration, priority, case) in enumerate(normalized, start=1):
        for minutes in range(capacity + 1):
            table[row][minutes] = table[row - 1][minutes]
            if duration <= minutes:
                table[row][minutes] = max(
                    table[row][minutes],
                    table[row - 1][minutes - duration] + priority
                )
        if len(trace) < 60:
            trace.append({
                "id": case.get("id"),
                "duration": duration,
                "priority": priority,
                "best_priority_at_capacity": table[row][capacity]
            })

    chosen = []
    remaining = capacity
    for row in range(len(normalized), 0, -1):
        duration, priority, case = normalized[row - 1]
        if table[row][remaining] != table[row - 1][remaining]:
            chosen.append(dict(case))
            remaining -= duration
    chosen.reverse()

    return {
        "algorithm": "Dynamic Programming Clinic Capacity Optimizer",
        "selected": chosen,
        "count": len(chosen),
        "total_duration": sum(case["duration"] for case in chosen),
        "total_priority": sum(case["priority"] for case in chosen),
        "capacity": capacity,
        "trace": trace,
        "time_complexity": "O(n * capacity)",
        "space_complexity": "O(n * capacity)"
    }


def assign_cases_backtracking(
    doctors: List[Dict[str, Any]],
    cases: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Assign every case to a qualified doctor without overlapping that doctor's visits."""
    if not isinstance(doctors, list) or not isinstance(cases, list):
        raise ValueError("doctors and cases must be lists.")
    for index, doctor in enumerate(doctors):
        if not isinstance(doctor, dict):
            raise ValueError(f"doctors[{index}] must be an object.")
        specialties = doctor.get("specializations", [])
        if not isinstance(specialties, list) or not all(isinstance(item, str) for item in specialties):
            raise ValueError(f"doctors[{index}] specializations must be a list of strings.")
    _validate_interval_records(cases, "cases")

    indexed_cases = list(enumerate(cases))
    indexed_cases.sort(key=lambda pair: (
        sum(
            1 for doctor in doctors
            if str(pair[1].get("specialization", "")).casefold()
            in [specialty.casefold() for specialty in doctor.get("specializations", [])]
        ),
        pair[1]["start"],
        pair[0]
    ))
    assignments = []
    doctor_schedules = [[] for _ in doctors]
    trace = []
    explored = 0

    def search(position: int) -> bool:
        nonlocal explored
        if position == len(indexed_cases):
            return True
        case_index, case = indexed_cases[position]
        specialty = case.get("specialization", "")
        for doctor_index, doctor in enumerate(doctors):
            qualifications = doctor.get("specializations", [])
            if not isinstance(specialty, str) or specialty.casefold() not in [
                item.casefold() for item in qualifications
            ]:
                continue
            if any(
                case["start"] < assigned_case["end"]
                and assigned_case["start"] < case["end"]
                for assigned_case in doctor_schedules[doctor_index]
            ):
                continue

            explored += 1
            assignment = {
                "case_id": case.get("id"),
                "case_specialization": specialty,
                "doctor_id": doctor.get("id"),
                "doctor_name": doctor.get("name", str(doctor.get("id", "Doctor"))),
                "start": case["start"],
                "end": case["end"]
            }
            assignments.append((case_index, assignment))
            doctor_schedules[doctor_index].append(case)
            if len(trace) < 60:
                trace.append({
                    "case_id": case.get("id"),
                    "doctor_name": assignment["doctor_name"],
                    "action": "assign",
                    "reason": "Specialty matches and this doctor's schedule has no overlap."
                })
            if search(position + 1):
                return True

            doctor_schedules[doctor_index].pop()
            assignments.pop()
            if len(trace) < 60:
                trace.append({
                    "case_id": case.get("id"),
                    "doctor_name": assignment["doctor_name"],
                    "action": "backtrack",
                    "reason": "This choice prevented a complete valid schedule."
                })
        return False

    success = search(0)
    result_assignments = [assignment for _, assignment in sorted(assignments)] if success else []
    return {
        "algorithm": "Backtracking Specialty & Schedule Assignment",
        "success": success,
        "assignments": result_assignments,
        "assigned_count": len(result_assignments),
        "case_count": len(cases),
        "explored_assignments": explored,
        "trace": trace,
        "time_complexity": "O(d^n) worst case",
        "space_complexity": "O(n + d)"
    }
