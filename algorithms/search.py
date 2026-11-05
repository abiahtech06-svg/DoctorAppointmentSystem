"""
Searching Algorithms Module for Doctor Appointment Booking and Management System.

Phase 3 - CLO2:
- Linear Search: Sequential search supporting exact and partial matching.
- Binary Search: Divide-and-conquer logarithmic search on sorted arrays.
- Detailed step-by-step tracers and comparison counts for educational evaluation.
"""

import time
from typing import Any, Callable, Dict, List, Optional, Tuple


def linear_search(
    arr: List[Any],
    target: Any,
    key_func: Optional[Callable[[Any], Any]] = None,
    match_mode: str = 'contains'
) -> Dict[str, Any]:
    """
    Perform Linear Search on an array.
    
    Time Complexity:
      - Best Case: O(1) (target is at index 0)
      - Average Case: O(n)
      - Worst Case: O(n) (target is at the last index or not found)
    Space Complexity: O(1) auxiliary space.
    
    Args:
        arr: List of items or dictionaries
        target: Value to search for
        key_func: Optional function to extract comparison key from each element
        match_mode: 'exact' or 'contains' (case-insensitive substring for strings)
        
    Returns:
        Dict containing found status, index, item, comparisons count, execution time, and step trace.
    """
    start_time = time.perf_counter()
    comparisons = 0
    trace = []
    found = False
    found_index = -1
    found_item = None
    
    target_str = str(target).strip().lower()
    target_is_num = False
    target_num = 0.0
    try:
        target_num = float(target)
        target_is_num = True
    except (ValueError, TypeError):
        target_is_num = False
    
    for idx, item in enumerate(arr):
        comparisons += 1
        current_val = key_func(item) if key_func else item
        
        is_match = False
        if current_val is not None:
            val_is_num = False
            val_num = 0.0
            try:
                val_num = float(current_val)
                val_is_num = True
            except (ValueError, TypeError):
                val_is_num = False

            if target_is_num and val_is_num:
                is_match = (val_num == target_num)
            else:
                curr_str = str(current_val).strip().lower()
                if match_mode == 'contains':
                    is_match = (target_str in curr_str) or (curr_str in target_str)
                else:
                    is_match = (curr_str == target_str)
                
        step_info = {
            'step': comparisons,
            'index': idx,
            'current_value': str(current_val) if current_val is not None else '',
            'value': str(current_val) if current_val is not None else '',
            'target': str(target),
            'comparison': f"arr[{idx}] ({current_val}) == {target} -> {'MATCH' if is_match else 'NO MATCH'}",
            'action': 'found' if is_match else 'no match',
            'matched': is_match,
            'found': is_match
        }
        trace.append(step_info)
        
        if is_match:
            found = True
            found_index = idx
            found_item = item
            break
            
    execution_time_ms = (time.perf_counter() - start_time) * 1000
    
    return {
        'algorithm': 'Linear Search',
        'found': found,
        'index': found_index,
        'item': found_item,
        'comparisons': comparisons,
        'total_elements': len(arr),
        'execution_time_ms': round(execution_time_ms, 4),
        'time_ms': round(execution_time_ms, 4),
        'time_complexity': {
            'best': 'O(1)',
            'average': 'O(n)',
            'worst': 'O(n)'
        },
        'space_complexity': 'O(1)',
        'trace': trace,
        'steps': trace
    }


def binary_search(
    arr: List[Any],
    target: Any,
    key_func: Optional[Callable[[Any], Any]] = None,
    is_sorted: bool = False
) -> Dict[str, Any]:
    """
    Perform Binary Search on an array.
    Precondition: Array must be sorted in ascending order by the comparison key.
    If not marked as is_sorted, the function sorts a copy first while tracking that fact.
    
    Time Complexity:
      - Best Case: O(1) (target is at the initial middle index)
      - Average Case: O(log n)
      - Worst Case: O(log n)
    Space Complexity: O(1) auxiliary space (iterative).
    
    Args:
        arr: List of items or dictionaries
        target: Target value to search for
        key_func: Optional key extractor
        is_sorted: Whether arr is already guaranteed sorted
        
    Returns:
        Dict containing found status, index, item, comparisons, execution time, and step trace.
    """
    start_time = time.perf_counter()
    trace = []
    comparisons = 0
    found = False
    found_index = -1
    found_item = None
    
    # Work on a copy if we need to ensure sorted order
    search_arr = list(arr)
    was_sorted_initially = is_sorted
    
    # Helper to extract value safely
    def get_val(item):
        if key_func is not None:
            v = key_func(item)
            return v if v is not None else ''
        return item if item is not None else ''

    # Convert target for numeric comparison if appropriate
    target_is_numeric = False
    try:
        numeric_target = float(target)
        target_is_numeric = True
    except (ValueError, TypeError):
        numeric_target = target

    def sort_key(item):
        v = get_val(item)
        if target_is_numeric:
            try:
                return (0, float(v))
            except (ValueError, TypeError):
                return (1, str(v).lower())
        return (0, str(v).lower())

    # If not guaranteed sorted, sort the array while retaining original items
    if not is_sorted and len(search_arr) > 1:
        search_arr.sort(key=sort_key)
        was_sorted_initially = False

    low = 0
    high = len(search_arr) - 1
    step_num = 0

    while low <= high:
        step_num += 1
        comparisons += 1
        mid = (low + high) // 2
        mid_item = search_arr[mid]
        mid_val = get_val(mid_item)

        # Compare values
        if target_is_numeric:
            try:
                mid_num = float(mid_val)
                diff = mid_num - numeric_target
            except (ValueError, TypeError):
                m_str = str(mid_val).lower()
                t_str = str(target).lower()
                diff = 0 if (m_str == t_str or t_str in m_str) else (-1 if m_str < t_str else 1)
        else:
            m_str = str(mid_val).lower()
            t_str = str(target).lower()
            if m_str == t_str or t_str in m_str or m_str in t_str:
                diff = 0
            else:
                diff = -1 if m_str < t_str else 1

        decision = ""
        if diff == 0:
            found = True
            found_index = mid
            found_item = mid_item
            decision = f"Target {target} matches arr[{mid}] ({mid_val})! Found!"
            trace.append({
                'step': step_num,
                'low': low,
                'mid': mid,
                'high': high,
                'index': mid,
                'mid_value': str(mid_val),
                'value': str(mid_val),
                'target': str(target),
                'action': 'found',
                'decision': decision,
                'found': True,
                'matched': True
            })
            break
        elif diff < 0:
            # mid_val < target => search right half
            decision = f"arr[{mid}] ({mid_val}) < target ({target}) -> Shift search to Right half (low = {mid + 1})"
            trace.append({
                'step': step_num,
                'low': low,
                'mid': mid,
                'high': high,
                'index': mid,
                'mid_value': str(mid_val),
                'value': str(mid_val),
                'target': str(target),
                'action': decision,
                'decision': decision,
                'found': False,
                'matched': False
            })
            low = mid + 1
        else:
            # mid_val > target => search left half
            decision = f"arr[{mid}] ({mid_val}) > target ({target}) -> Shift search to Left half (high = {mid - 1})"
            trace.append({
                'step': step_num,
                'low': low,
                'mid': mid,
                'high': high,
                'index': mid,
                'mid_value': str(mid_val),
                'value': str(mid_val),
                'target': str(target),
                'action': decision,
                'decision': decision,
                'found': False,
                'matched': False
            })
            high = mid - 1

    if not found and low > high:
        trace.append({
            'step': step_num + 1,
            'low': low,
            'mid': None,
            'high': high,
            'index': -1,
            'mid_value': None,
            'value': 'N/A',
            'target': str(target),
            'action': f"low ({low}) > high ({high}) -> Target {target} not present in dataset.",
            'decision': f"low ({low}) > high ({high}) -> Target {target} not present in dataset.",
            'found': False,
            'matched': False
        })

    execution_time_ms = (time.perf_counter() - start_time) * 1000

    return {
        'algorithm': 'Binary Search',
        'found': found,
        'index': found_index,
        'item': found_item,
        'comparisons': comparisons,
        'total_elements': len(search_arr),
        'execution_time_ms': round(execution_time_ms, 4),
        'time_ms': round(execution_time_ms, 4),
        'was_sorted_initially': was_sorted_initially,
        'time_complexity': {
            'best': 'O(1)',
            'average': 'O(log n)',
            'worst': 'O(log n)'
        },
        'space_complexity': 'O(1)',
        'trace': trace,
        'steps': trace
    }


def compare_search_algorithms(
    arr: List[Any],
    target: Any,
    key_func: Optional[Callable[[Any], Any]] = None,
    match_mode: str = 'contains'
) -> Dict[str, Any]:
    """
    Run Linear Search and Binary Search on the same data and produce comparative analysis.
    """
    def get_val(item):
        if key_func is not None:
            v = key_func(item)
            return v if v is not None else ''
        return item if item is not None else ''

    # Check if numeric target
    target_is_num = False
    try:
        float(target)
        target_is_num = True
    except (ValueError, TypeError):
        target_is_num = False

    def sort_key(item):
        v = get_val(item)
        if target_is_num:
            try:
                return (0, float(v))
            except (ValueError, TypeError):
                return (1, str(v).lower())
        return (0, str(v).lower())

    sorted_arr = sorted(arr, key=sort_key)
    
    linear_res = linear_search(arr, target, key_func=key_func, match_mode=match_mode)
    binary_res = binary_search(sorted_arr, target, key_func=key_func, is_sorted=True)
    
    efficiency_ratio = (
        round(linear_res['comparisons'] / binary_res['comparisons'], 2)
        if binary_res['comparisons'] > 0 else 1.0
    )
    
    return {
        'target': target,
        'total_elements': len(arr),
        'linear_search': linear_res,
        'binary_search': binary_res,
        'comparison_summary': {
            'linear_comparisons': linear_res['comparisons'],
            'binary_comparisons': binary_res['comparisons'],
            'efficiency_gain': f"{efficiency_ratio}x fewer comparisons with Binary Search" if efficiency_ratio >= 1 else "Comparable",
            'linear_time_ms': linear_res['execution_time_ms'],
            'binary_time_ms': binary_res['execution_time_ms']
        }
    }
