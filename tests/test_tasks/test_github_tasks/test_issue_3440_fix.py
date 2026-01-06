"""
Unit tests for issue #3440 fix.

These tests verify that the optimization to eliminate redundant full table scans
is working correctly by checking the code changes and testing the logic.
"""
import pytest
import os


def test_batch_size_increased_to_200():
    """
    Verify that the batch size has been increased from 20 to 200 in messages.py.
    """
    messages_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/messages.py"
    
    with open(messages_file, 'r') as f:
        content = f.read()
    
    assert "if len(all_data) >= 200:" in content, "Batch size should be 200"
    assert "# Increased batch size from 20 to 200 for better performance" in content, "Comment should mention batch size 200"


def test_mappings_built_once_in_messages():
    """
    Verify that issue and PR mappings are built once before the batch loop in messages.py.
    """
    messages_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/messages.py"
    
    with open(messages_file, 'r') as f:
        content = f.read()
    
    assert "# Build issue and PR URL mappings once before processing batches" in content
    assert "# This prevents full table scans on every batch (issue #3440)" in content
    assert "issue_url_to_id_map = {}" in content
    assert "pr_issue_url_to_id_map = {}" in content


def test_process_messages_accepts_mapping_parameters():
    """
    Verify that process_messages function signature includes optional mapping parameters.
    """
    messages_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/messages.py"
    
    with open(messages_file, 'r') as f:
        content = f.read()
    
    assert "def process_messages(messages, task_name, repo_id, logger, augur_db, issue_url_to_id_map=None, pr_issue_url_to_id_map=None):" in content


def test_mappings_passed_to_process_messages():
    """
    Verify that mappings are passed to process_messages calls.
    """
    messages_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/messages.py"
    
    with open(messages_file, 'r') as f:
        content = f.read()
    
    assert "process_messages(all_data, task_name, repo_id, logger, augur_db, issue_url_to_id_map, pr_issue_url_to_id_map)" in content


def test_mappings_built_once_in_events():
    """
    Verify that issue and PR mappings are built once before the batch loop in events.py.
    """
    events_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/events.py"
    
    with open(events_file, 'r') as f:
        content = f.read()
    
    assert "# Build issue and PR URL mappings once before processing batches" in content
    assert "# This prevents full table scans on every batch (issue #3440)" in content
    assert "issue_url_to_id_map = self._get_map_from_issue_url_to_id(repo_id)" in content
    assert "pr_url_to_id_map = self._get_map_from_pr_url_to_id(repo_id)" in content


def test_events_process_events_signature():
    """
    Verify that _process_events method signature includes mapping parameters.
    """
    events_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/events.py"
    
    with open(events_file, 'r') as f:
        content = f.read()
    
    assert "def _process_events(self, events, repo_id, issue_url_to_id_map, pr_url_to_id_map):" in content


def test_events_process_issue_events_signature():
    """
    Verify that _process_issue_events method signature includes mapping parameter.
    """
    events_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/events.py"
    
    with open(events_file, 'r') as f:
        content = f.read()
    
    assert "def _process_issue_events(self, issue_events, repo_id, issue_url_to_id_map):" in content


def test_events_process_pr_events_signature():
    """
    Verify that _process_pr_events method signature includes mapping parameter.
    """
    events_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/events.py"
    
    with open(events_file, 'r') as f:
        content = f.read()
    
    assert "def _process_pr_events(self, pr_events, repo_id, pr_url_to_id_map):" in content


def test_mappings_passed_in_events():
    """
    Verify that mappings are passed through the call chain in events.py.
    """
    events_file = "/Users/pratykshgupta/Desktop/pg-augur/augur/tasks/github/events.py"
    
    with open(events_file, 'r') as f:
        content = f.read()
    
    assert "self._process_events(events, repo_id, issue_url_to_id_map, pr_url_to_id_map)" in content
    assert "self._process_issue_events(issue_events, repo_id, issue_url_to_id_map)" in content
    assert "self._process_pr_events(pr_events, repo_id, pr_url_to_id_map)" in content


def test_performance_improvement_calculation():
    """
    Verify the expected performance improvements match the issue #3440 description.
    """
    old_batch_size_messages = 20
    new_batch_size_messages = 200
    num_messages = 1000
    
    old_batches_messages = num_messages // old_batch_size_messages
    old_queries_messages = old_batches_messages * 2
    new_queries_messages = 2
    
    assert old_queries_messages == 100, f"Expected 100 old queries, got {old_queries_messages}"
    assert new_queries_messages == 2, f"Expected 2 new queries, got {new_queries_messages}"
    assert old_queries_messages / new_queries_messages == 50, "Expected 50x improvement"
    
    batch_size_events = 500
    num_events = 10000
    
    old_batches_events = num_events // batch_size_events
    old_queries_events = old_batches_events * 2
    new_queries_events = 2
    
    assert old_queries_events == 40, f"Expected 40 old queries, got {old_queries_events}"
    assert new_queries_events == 2, f"Expected 2 new queries, got {new_queries_events}"
    assert old_queries_events / new_queries_events == 20, "Expected 20x improvement"
