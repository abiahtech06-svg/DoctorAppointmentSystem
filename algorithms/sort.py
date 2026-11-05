"""
Sorting Algorithms Module for Doctor Appointment Booking and Management System.

Phase 3 - CLO2:
- Merge Sort: Divide-and-conquer, stable sorting algorithm with O(n log n) guaranteed time.
- Quick Sort: Partitioning-based divide-and-conquer algorithm with efficient in-place sorting.
- Insertion Sort: Adaptive incremental sorting, ideal for small or nearly-sorted datasets.
- Performance and conceptual comparison utilities.
"""

import time
import copy
from typing import Any, Callable, Dict, List, Optional


def _extract_val(item: Any, key_func: Optional[Callable[[Any], Any]] = None) -> Any:
    """Helper to safely extract key value from item."""
    if key_func is not None:
        return key_func(item)
    return item


def _compare_values(a: Any, b: Any, reverse: bool = False) -> bool:
    """
    Returns True if a should come before b based on reverse flag.
    For ascending (reverse=False): returns True if a <= b.
    """
    try:
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a >= b if reverse else a <= b
        return str(a).lower() >= str(b).lower() if reverse else str(a).lower() <= str(b).lower()
    except (TypeError, ValueError):
        return a >= b if reverse else a <= b


# ==========================================
# 1. MERGE SORT IMPLEMENTATION
# ==========================================

def merge_sort(
    arr: List[Any],
    key_func: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
    record_trace: bool = True
) -> Dict[str, Any]:
    """
    Perform Merge Sort on a list.
    
    Divide and Conquer Strategy:
    1. Divide: Split the unsorted list into two approximately equal halves.
    2. Conquer: Recursively sort each sublist.
    3. Combine: Merge the two sorted sublists into a single sorted list.
    
    Properties:
    - Stable: Preserves relative order of duplicate elements.
    - Time Complexity:
        * Best Case: O(n log n)
        * Average Case: O(n log n)
        * Worst Case: O(n log n)
    - Space Complexity: O(n) auxiliary space for merging.
    """
    start_time = time.perf_counter()
    data = list(arr)
    comparisons = 0
    merges = 0
    trace_steps = []
    
    def _merge(left: List[Any], right: List[Any], depth: int) -> List[Any]:
        nonlocal comparisons, merges
        merged = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            comparisons += 1
            left_val = _extract_val(left[i], key_func)
            right_val = _extract_val(right[j], key_func)
            
            if _compare_values(left_val, right_val, reverse):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                
        merged.extend(left[i:])
        merged.extend(right[j:])
        merges += 1
        
        if record_trace and len(trace_steps) < 25:
            left_preview = [_extract_val(x, key_func) for x in left[:3]]
            right_preview = [_extract_val(x, key_func) for x in right[:3]]
            merged_preview = [_extract_val(x, key_func) for x in merged[:5]]
            trace_steps.append({
                'type': 'merge',
                'depth': depth,
                'left_size': len(left),
                'right_size': len(right),
                'merged_size': len(merged),
                'left_sample': left_preview,
                'right_sample': right_preview,
                'merged_sample': merged_preview,
                'description': f"Merged left ({len(left)} items) and right ({len(right)} items) -> {len(merged)} sorted items"
            })
            
        return merged

    def _sort(sub_arr: List[Any], depth: int = 0) -> List[Any]:
        if len(sub_arr) <= 1:
            return sub_arr
        
        mid = len(sub_arr) // 2
        left_half = _sort(sub_arr[:mid], depth + 1)
        right_half = _sort(sub_arr[mid:], depth + 1)
        
        return _merge(left_half, right_half, depth)

    sorted_list = _sort(data, 0)
    exec_time_ms = (time.perf_counter() - start_time) * 1000

    return {
        'algorithm': 'Merge Sort',
        'sorted_list': sorted_list,
        'sorted_items': sorted_list,
        'comparisons': comparisons,
        'operations': merges,
        'moves': merges,
        'operation_label': 'Merges',
        'execution_time_ms': round(exec_time_ms, 4),
        'time_ms': round(exec_time_ms, 4),
        'total_elements': len(arr),
        'stable': True,
        'is_stable': True,
        'time_complexity': {
            'best': 'O(n log n)',
            'average': 'O(n log n)',
            'worst': 'O(n log n)'
        },
        'space_complexity': 'O(n)',
        'trace': trace_steps,
        'steps': trace_steps
    }


# ==========================================
# 2. QUICK SORT IMPLEMENTATION
# ==========================================

def quick_sort(
    arr: List[Any],
    key_func: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
    record_trace: bool = True
) -> Dict[str, Any]:
    """
    Perform Quick Sort on a list.
    
    Divide and Conquer Strategy:
    1. Pivot Selection: Choose an element as pivot (middle element chosen here to mitigate sorted-input worst case).
    2. Partition: Reorder array so elements less than pivot come before, and greater come after.
    3. Recursion: Recursively sort left and right partitions.
    
    Properties:
    - In-place (or auxiliary stack space): O(log n) stack memory.
    - Unstable: May change relative order of identical keys.
    - Time Complexity:
        * Best Case: O(n log n)
        * Average Case: O(n log n)
        * Worst Case: O(n^2) (pathological pivot choice on sorted/reverse lists)
    - Space Complexity: O(log n) auxiliary stack space.
    """
    start_time = time.perf_counter()
    data = list(arr)
    comparisons = 0
    swaps = 0
    trace_steps = []

    def _partition(low: int, high: int, depth: int) -> int:
        nonlocal comparisons, swaps
        # Choose middle element as pivot and swap to end for stability against pre-sorted data
        mid = low + (high - low) // 2
        data[mid], data[high] = data[high], data[mid]
        swaps += 1
        
        pivot_item = data[high]
        pivot_val = _extract_val(pivot_item, key_func)
        i = low - 1
        
        for j in range(low, high):
            comparisons += 1
            curr_val = _extract_val(data[j], key_func)
            
            # For ascending, place elements <= pivot to left partition
            if _compare_values(curr_val, pivot_val, reverse):
                i += 1
                if i != j:
                    data[i], data[j] = data[j], data[i]
                    swaps += 1
                    
        # Place pivot at correct partition index
        data[i + 1], data[high] = data[high], data[i + 1]
        swaps += 1
        pivot_index = i + 1
        
        if record_trace and len(trace_steps) < 25:
            trace_steps.append({
                'type': 'partition',
                'depth': depth,
                'low': low,
                'high': high,
                'pivot_index': pivot_index,
                'pivot_value': str(pivot_val),
                'description': f"Partitioned subarray [{low}:{high}] around pivot '{pivot_val}' at index {pivot_index}"
            })
            
        return pivot_index

    def _quick_sort(low: int, high: int, depth: int = 0):
        if low < high:
            pi = _partition(low, high, depth)
            _quick_sort(low, pi - 1, depth + 1)
            _quick_sort(pi + 1, high, depth + 1)

    if len(data) > 1:
        _quick_sort(0, len(data) - 1, 0)
        
    exec_time_ms = (time.perf_counter() - start_time) * 1000

    return {
        'algorithm': 'Quick Sort',
        'sorted_list': data,
        'sorted_items': data,
        'comparisons': comparisons,
        'operations': swaps,
        'moves': swaps,
        'operation_label': 'Swaps',
        'execution_time_ms': round(exec_time_ms, 4),
        'time_ms': round(exec_time_ms, 4),
        'total_elements': len(arr),
        'stable': False,
        'is_stable': False,
        'time_complexity': {
            'best': 'O(n log n)',
            'average': 'O(n log n)',
            'worst': 'O(n^2)'
        },
        'space_complexity': 'O(log n)',
        'trace': trace_steps,
        'steps': trace_steps
    }


# ==========================================
# 3. INSERTION SORT IMPLEMENTATION
# ==========================================

def insertion_sort(
    arr: List[Any],
    key_func: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
    record_trace: bool = True
) -> Dict[str, Any]:
    """
    Perform Insertion Sort on a list.
    
    Incremental Strategy:
    Builds the sorted array one item at a time by repeatedly taking the next item
    and inserting it into its correct position among the already-sorted items.
    
    Properties:
    - Adaptive: O(n) when array is already sorted or nearly sorted!
    - Stable: Preserves relative order of equal elements.
    - In-place: O(1) auxiliary space.
    - Time Complexity:
        * Best Case: O(n) (already sorted)
        * Average Case: O(n^2)
        * Worst Case: O(n^2) (reverse sorted)
    - Space Complexity: O(1) auxiliary space.
    """
    start_time = time.perf_counter()
    data = list(arr)
    comparisons = 0
    shifts = 0
    trace_steps = []
    n = len(data)

    for i in range(1, n):
        key_item = data[i]
        key_val = _extract_val(key_item, key_func)
        j = i - 1
        
        while j >= 0:
            comparisons += 1
            curr_val = _extract_val(data[j], key_func)
            
            # Condition to shift:
            # In ascending (reverse=False): shift if curr_val > key_val (i.e. not _compare_values(curr_val, key_val, False))
            # In descending (reverse=True): shift if curr_val < key_val
            needs_shift = not _compare_values(curr_val, key_val, reverse)
            
            if needs_shift:
                data[j + 1] = data[j]
                shifts += 1
                j -= 1
            else:
                break
                
        data[j + 1] = key_item
        
        if record_trace and len(trace_steps) < 25:
            trace_steps.append({
                'pass': i,
                'inserted_value': str(key_val),
                'inserted_position': j + 1,
                'shifts_in_pass': i - (j + 1),
                'description': f"Pass {i}: Inserted '{key_val}' at index {j + 1}"
            })

    exec_time_ms = (time.perf_counter() - start_time) * 1000

    return {
        'algorithm': 'Insertion Sort',
        'sorted_list': data,
        'sorted_items': data,
        'comparisons': comparisons,
        'operations': shifts,
        'moves': shifts,
        'operation_label': 'Shifts',
        'execution_time_ms': round(exec_time_ms, 4),
        'time_ms': round(exec_time_ms, 4),
        'total_elements': len(arr),
        'stable': True,
        'is_stable': True,
        'time_complexity': {
            'best': 'O(n)',
            'average': 'O(n^2)',
            'worst': 'O(n^2)'
        },
        'space_complexity': 'O(1)',
        'trace': trace_steps,
        'steps': trace_steps
    }


# ==========================================
# 4. COMPARISON UTILITY
# ==========================================

def compare_sorting_algorithms(
    arr: List[Any],
    key_func: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False
) -> Dict[str, Any]:
    """
    Run Merge Sort, Quick Sort, and Insertion Sort on copies of the exact same dataset
    to provide empirical and conceptual performance comparison.
    """
    # Execute each algorithm independently on identical data
    merge_res = merge_sort(copy.deepcopy(arr), key_func=key_func, reverse=reverse, record_trace=False)
    quick_res = quick_sort(copy.deepcopy(arr), key_func=key_func, reverse=reverse, record_trace=False)
    insertion_res = insertion_sort(copy.deepcopy(arr), key_func=key_func, reverse=reverse, record_trace=False)

    return {
        'total_elements': len(arr),
        'reverse': reverse,
        'sorted_list': merge_res['sorted_list'],
        'sorted_items': merge_res['sorted_items'],
        'merge_sort': merge_res,
        'quick_sort': quick_res,
        'insertion_sort': insertion_res,
        'algorithms': {
            'merge_sort': {
                'name': 'Merge Sort',
                'comparisons': merge_res['comparisons'],
                'operations': merge_res['operations'],
                'moves': merge_res['moves'],
                'operation_label': merge_res['operation_label'],
                'execution_time_ms': merge_res['execution_time_ms'],
                'time_ms': merge_res['time_ms'],
                'stable': merge_res['stable'],
                'is_stable': merge_res['is_stable'],
                'best_time': 'O(n log n)',
                'avg_time': 'O(n log n)',
                'worst_time': 'O(n log n)',
                'space_complexity': 'O(n)',
                'strategy': 'Divide and Conquer (Merge)'
            },
            'quick_sort': {
                'name': 'Quick Sort',
                'comparisons': quick_res['comparisons'],
                'operations': quick_res['operations'],
                'moves': quick_res['moves'],
                'operation_label': quick_res['operation_label'],
                'execution_time_ms': quick_res['execution_time_ms'],
                'time_ms': quick_res['time_ms'],
                'stable': quick_res['stable'],
                'is_stable': quick_res['is_stable'],
                'best_time': 'O(n log n)',
                'avg_time': 'O(n log n)',
                'worst_time': 'O(n^2)',
                'space_complexity': 'O(log n)',
                'strategy': 'Divide and Conquer (Partitioning)'
            },
            'insertion_sort': {
                'name': 'Insertion Sort',
                'comparisons': insertion_res['comparisons'],
                'operations': insertion_res['operations'],
                'moves': insertion_res['moves'],
                'operation_label': insertion_res['operation_label'],
                'execution_time_ms': insertion_res['execution_time_ms'],
                'time_ms': insertion_res['time_ms'],
                'stable': insertion_res['stable'],
                'is_stable': insertion_res['is_stable'],
                'best_time': 'O(n)',
                'avg_time': 'O(n^2)',
                'worst_time': 'O(n^2)',
                'space_complexity': 'O(1)',
                'strategy': 'Incremental Insertion'
            }
        }
    }
