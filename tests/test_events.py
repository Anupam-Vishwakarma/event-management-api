"""
Comprehensive tests for Event Management API events endpoints.
Tests cover: creation, retrieval, updates, deletion, and various error scenarios.
"""

import pytest
from datetime import datetime, timedelta, timezone
from fastapi import status


class TestCreateEvent:
    """Test cases for POST /events endpoint."""
    
    def test_create_event_success(self, client, sample_event_data):
        """Test successful event creation."""
        response = client.post("/events/", json=sample_event_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_event_data["title"]
        assert data["description"] == sample_event_data["description"]
        assert data["location"] == sample_event_data["location"]
        assert data["max_capacity"] == sample_event_data["max_capacity"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_event_minimal_data(self, client):
        """Test event creation with minimal required fields."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        event_data = {
            "title": "Simple Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 50
        }
        
        response = client.post("/events/", json=event_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Simple Event"
        assert data["description"] is None
        assert data["location"] is None
    
    def test_create_event_missing_title(self, client):
        """Test event creation fails without title."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        event_data = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 50
        }
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_missing_start_time(self, client, sample_event_data):
        """Test event creation fails without start_time."""
        event_data = sample_event_data.copy()
        del event_data["start_time"]
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_missing_end_time(self, client, sample_event_data):
        """Test event creation fails without end_time."""
        event_data = sample_event_data.copy()
        del event_data["end_time"]
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_missing_capacity(self, client, sample_event_data):
        """Test event creation fails without max_capacity."""
        event_data = sample_event_data.copy()
        del event_data["max_capacity"]
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_negative_capacity(self, client, sample_event_data):
        """Test event creation fails with negative capacity."""
        event_data = sample_event_data.copy()
        event_data["max_capacity"] = -10
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_zero_capacity(self, client, sample_event_data):
        """Test event creation fails with zero capacity."""
        event_data = sample_event_data.copy()
        event_data["max_capacity"] = 0
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_end_time_before_start_time(self, client, sample_event_data):
        """Test event creation fails when end_time is before start_time."""
        event_data = sample_event_data.copy()
        # Swap start and end times
        event_data["start_time"], event_data["end_time"] = \
            event_data["end_time"], event_data["start_time"]
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_same_start_end_time(self, client):
        """Test event creation fails when start and end times are equal."""
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        
        event_data = {
            "title": "Invalid Event",
            "start_time": start_time.isoformat(),
            "end_time": start_time.isoformat(),
            "max_capacity": 50
        }
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_event_large_capacity(self, client, sample_event_data):
        """Test event creation with large capacity."""
        event_data = sample_event_data.copy()
        event_data["max_capacity"] = 999999
        
        response = client.post("/events/", json=event_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["max_capacity"] == 999999


class TestGetAllEvents:
    """Test cases for GET /events endpoint."""
    
    def test_get_all_events_empty(self, client):
        """Test getting all events when database is empty."""
        response = client.get("/events/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_all_events_single(self, client, created_event):
        """Test getting all events with one event in database."""
        response = client.get("/events/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == created_event["id"]
        assert data[0]["title"] == created_event["title"]
    
    def test_get_all_events_multiple(self, client, sample_event_data):
        """Test getting all events with multiple events in database."""
        # Create 3 events
        for i in range(3):
            event_data = sample_event_data.copy()
            event_data["title"] = f"Event {i+1}"
            client.post("/events/", json=event_data)
        
        response = client.get("/events/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_all_events_returns_list(self, client):
        """Test that GET /events returns a list."""
        response = client.get("/events/")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_get_all_events_correct_schema(self, client, created_event):
        """Test that returned events have correct schema."""
        response = client.get("/events/")
        
        assert response.status_code == status.HTTP_200_OK
        events = response.json()
        event = events[0]
        
        required_fields = ["id", "title", "start_time", "end_time", "max_capacity", 
                          "created_at", "updated_at"]
        for field in required_fields:
            assert field in event


class TestGetEventById:
    """Test cases for GET /events/{event_id} endpoint."""
    
    def test_get_event_by_id_success(self, client, created_event):
        """Test successfully getting an event by ID."""
        event_id = created_event["id"]
        response = client.get(f"/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == event_id
        assert data["title"] == created_event["title"]
    
    def test_get_event_by_id_not_found(self, client):
        """Test getting a non-existent event returns 404."""
        response = client.get("/events/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_event_by_id_invalid_id_type(self, client):
        """Test getting event with invalid ID type."""
        response = client.get("/events/invalid")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_event_by_id_negative_id(self, client):
        """Test getting event with negative ID."""
        response = client.get("/events/-1")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_event_by_id_returns_complete_data(self, client, created_event):
        """Test that GET returns all event fields."""
        event_id = created_event["id"]
        response = client.get(f"/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "location" in data
        assert "start_time" in data
        assert "end_time" in data
        assert "max_capacity" in data
        assert "created_at" in data
        assert "updated_at" in data


class TestUpdateEvent:
    """Test cases for PUT /events/{event_id} endpoint."""
    
    def test_update_event_success(self, client, created_event):
        """Test successfully updating an event."""
        event_id = created_event["id"]
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description"
        }
        
        response = client.put(f"/events/{event_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated Description"
        assert data["id"] == event_id
    
    def test_update_event_partial(self, client, created_event):
        """Test partial update of an event."""
        event_id = created_event["id"]
        original_title = created_event["title"]
        
        update_data = {"description": "New Description"}
        
        response = client.put(f"/events/{event_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == original_title  # Unchanged
        assert data["description"] == "New Description"
    
    def test_update_event_not_found(self, client):
        """Test updating non-existent event returns 404."""
        update_data = {"title": "New Title"}
        response = client.put("/events/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_event_invalid_capacity(self, client, created_event):
        """Test updating event with invalid capacity."""
        event_id = created_event["id"]
        update_data = {"max_capacity": 0}
        
        response = client.put(f"/events/{event_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_event_invalid_end_time(self, client, created_event):
        """Test updating event with end_time before start_time."""
        event_id = created_event["id"]
        
        # Set end_time to before start_time
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        update_data = {
            "start_time": start_time.isoformat(),
            "end_time": (start_time - timedelta(hours=1)).isoformat()
        }
        
        response = client.put(f"/events/{event_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_event_empty_body(self, client, created_event):
        """Test updating event with empty body (no changes)."""
        event_id = created_event["id"]
        
        response = client.put(f"/events/{event_id}", json={})
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_update_event_all_fields(self, client, created_event):
        """Test updating all fields of an event."""
        event_id = created_event["id"]
        
        start_time = datetime.now(timezone.utc) + timedelta(days=2)
        end_time = start_time + timedelta(hours=3)
        
        update_data = {
            "title": "Completely Updated",
            "description": "New desc",
            "location": "New Location",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 200
        }
        
        response = client.put(f"/events/{event_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Completely Updated"
        assert data["max_capacity"] == 200


class TestDeleteEvent:
    """Test cases for DELETE /events/{event_id} endpoint."""
    
    def test_delete_event_success(self, client, created_event):
        """Test successfully deleting an event."""
        event_id = created_event["id"]
        
        response = client.delete(f"/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify it's deleted
        verify_response = client.get(f"/events/{event_id}")
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_event_not_found(self, client):
        """Test deleting non-existent event returns 404."""
        response = client.delete("/events/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_event_invalid_id_type(self, client):
        """Test deleting event with invalid ID type."""
        response = client.delete("/events/invalid")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_delete_event_twice(self, client, created_event):
        """Test deleting same event twice returns error on second attempt."""
        event_id = created_event["id"]
        
        # First delete
        response1 = client.delete(f"/events/{event_id}")
        assert response1.status_code == status.HTTP_200_OK
        
        # Second delete
        response2 = client.delete(f"/events/{event_id}")
        assert response2.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_event_removes_from_list(self, client, created_event):
        """Test that deleted event no longer appears in event list."""
        event_id = created_event["id"]
        
        # Get list before delete
        response_before = client.get("/events/")
        assert len(response_before.json()) == 1
        
        # Delete event
        client.delete(f"/events/{event_id}")
        
        # Get list after delete
        response_after = client.get("/events/")
        assert len(response_after.json()) == 0
