# Algorithms Package
# Contains algorithm implementations using data structures and sorting/searching routines

from .expression_stack import ExpressionValidator
from .search import linear_search, binary_search, compare_search_algorithms
from .sort import merge_sort, quick_sort, insertion_sort, compare_sorting_algorithms
from .optimization import (
    greedy_appointment_selection,
    optimize_clinic_capacity,
    assign_cases_backtracking
)

__all__ = [
    'ExpressionValidator',
    'linear_search',
    'binary_search',
    'compare_search_algorithms',
    'merge_sort',
    'quick_sort',
    'insertion_sort',
    'compare_sorting_algorithms',
    'greedy_appointment_selection',
    'optimize_clinic_capacity',
    'assign_cases_backtracking'
]
