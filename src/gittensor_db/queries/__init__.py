"""
Query exports
"""

from .queries import *

__all__ = [
    # Miner queries
    'GET_MINER',
    'GET_MINER_BY_UID',
    'GET_MINER_BY_HOTKEY',
    'GET_MINER_BY_GITHUB_ID',
    'GET_MINER_BY_HOTKEY_AND_GITHUB_ID',
    'SET_MINER',
    'UPSERT_MINER',
    'GET_ALL_MINERS',

    # Repository queries
    'GET_REPOSITORY',
    'SET_REPOSITORY',
    'GET_ALL_REPOSITORIES',

    # Pull Request queries
    'GET_PULL_REQUEST',
    'SET_PULL_REQUEST',
    'GET_PULL_REQUESTS_BY_REPOSITORY',
    'GET_PULL_REQUESTS_BY_MINER',
    'GET_PULL_REQUEST_WITH_FILE_CHANGES',

    # File Change queries
    'GET_FILE_CHANGE',
    'GET_FILE_CHANGES_BY_PR',
    'SET_FILE_CHANGES_FOR_PR',

    # Miner Evaluation queries
    'GET_MINER_EVALUATION',
    'GET_LATEST_MINER_EVALUATION',
    'SET_MINER_EVALUATION',
    'GET_EVALUATIONS_BY_TIMEFRAME',

    # Issue queries
    'GET_ISSUE',
    'GET_ISSUES_BY_REPOSITORY',
    'SET_ISSUE',

    # Bulk Upsert queries
    'BULK_UPSERT_MINERS',
    'BULK_UPSERT_REPOSITORIES',
    'BULK_UPSERT_PULL_REQUESTS',
    'BULK_UPSERT_ISSUES',
    'BULK_UPSERT_FILE_CHANGES'
]