"""
Comprehensive tests for Event Management API participants endpoints.
Tests cover: registration, capacity limits, duplicate prevention, and error scenarios.
"""

import pytest
from fastapi import status


class TestRegisterParticipant:
    """Test cases for POST /events/{event_id}/register endpoint."""
    
    def test_register_participant_success(self, client, created_event, sample_participant_data):
        """Test successful participant registration."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_participant_data["name"]
        assert data["email"] == sample_participant_data["email"]
        assert data["event_id"] == event_id
        assert "id" in data
        assert "registered_at" in data
    
    def test_register_participant_multiple_to_same_event(self, client, created_event, 
                                                         sample_participant_data, 
                                                         sample_participant_data_2):
        """Test registering multiple participants to the same event."""
        event_id = created_event["id"]
        
        # Register first participant
        response1 = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Register second participant
        response2 = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data_2
        )
        assert response2.status_code == status.HTTP_201_CREATED
        
        # Verify both are registered
        assert response1.json()["email"] != response2.json()["email"]
    
    def test_register_participant_duplicate_email(self, client, created_event, 
                                                  sample_participant_data):
        """Test that duplicate email registration is prevented."""
        event_id = created_event["id"]
        
        # Register first time
        response1 = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to register with same email
        response2 = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response2.json()["detail"].lower()
    
    def test_register_participant_capacity_full(self, client, created_event_small_capacity,
                                               sample_participant_data, 
                                               sample_participant_data_2):
        """Test that registration fails when event capacity is full."""
        event_id = created_event_small_capacity["id"]
        
        # Register first participant (fills capacity)
        response1 = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to register second participant (should fail)
        response2 = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data_2
        )
        
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "maximum capacity" in response2.json()["detail"].lower()
    
    def test_register_participant_nonexistent_event(self, client, sample_participant_data):
        """Test registration to non-existent event returns 404."""
        response = client.post(
            "/events/999/register",
            json=sample_participant_data
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_register_participant_missing_name(self, client, created_event):
        """Test registration fails without name."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_participant_missing_email(self, client, created_event):
        """Test registration fails without email."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"name": "John Doe"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_participant_empty_name(self, client, created_event):
        """Test registration fails with empty name."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"name": "", "email": "test@example.com"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_participant_empty_email(self, client, created_event):
        """Test registration fails with empty email."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"name": "John Doe", "email": ""}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_participant_invalid_email_format(self, client, created_event):
        """Test registration fails with invalid email format."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"name": "John Doe", "email": "invalid-email"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_participant_long_name(self, client, created_event):
        """Test registration with very long name."""
        event_id = created_event["id"]
        long_name = "A" * 200  # Very long name
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"name": long_name, "email": "test@example.com"}
        )
        
        # Should succeed - no name length validation
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_register_participant_special_characters_email(self, client, created_event):
        """Test registration with special characters in email (valid format)."""
        event_id = created_event["id"]
        
        response = client.post(
            f"/events/{event_id}/register",
            json={"name": "John Doe", "email": "john+special@example.co.uk"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED


class TestGetEventParticipants:
    """Test cases for GET /events/{event_id}/participants endpoint."""
    
    def test_get_participants_empty(self, client, created_event):
        """Test getting participants when none registered."""
        event_id = created_event["id"]
        
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_participants_single(self, client, created_event, sample_participant_data):
        """Test getting participants with one registered."""
        event_id = created_event["id"]
        
        # Register one participant
        client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["email"] == sample_participant_data["email"]
    
    def test_get_participants_multiple(self, client, created_event, 
                                      sample_participant_data, sample_participant_data_2):
        """Test getting participants with multiple registered."""
        event_id = created_event["id"]
        
        # Register two participants
        client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data_2
        )
        
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
    
    def test_get_participants_nonexistent_event(self, client):
        """Test getting participants for non-existent event returns 404."""
        response = client.get("/events/999/participants")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_participants_returns_list(self, client, created_event):
        """Test that GET participants returns a list."""
        event_id = created_event["id"]
        
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
    
    def test_get_participants_correct_schema(self, client, created_event, 
                                            sample_participant_data):
        """Test that returned participants have correct schema."""
        event_id = created_event["id"]
        
        # Register a participant
        client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_200_OK
        participants = response.json()
        participant = participants[0]
        
        required_fields = ["id", "name", "email", "event_id", "registered_at"]
        for field in required_fields:
            assert field in participant
    
    def test_get_participants_isolation(self, client, sample_event_data, 
                                       sample_participant_data, sample_participant_data_2):
        """Test that participants are isolated per event."""
        # Create two events
        response1 = client.post("/events/", json=sample_event_data)
        event1_id = response1.json()["id"]
        
        sample_event_data_2 = sample_event_data.copy()
        sample_event_data_2["title"] = "Second Event"
        response2 = client.post("/events/", json=sample_event_data_2)
        event2_id = response2.json()["id"]
        
        # Register participant to event 1
        client.post(
            f"/events/{event1_id}/register",
            json=sample_participant_data
        )
        
        # Register different participant to event 2
        client.post(
            f"/events/{event2_id}/register",
            json=sample_participant_data_2
        )
        
        # Get participants for event 1
        response_event1 = client.get(f"/events/{event1_id}/participants")
        assert len(response_event1.json()) == 1
        assert response_event1.json()[0]["email"] == sample_participant_data["email"]
        
        # Get participants for event 2
        response_event2 = client.get(f"/events/{event2_id}/participants")
        assert len(response_event2.json()) == 1
        assert response_event2.json()[0]["email"] == sample_participant_data_2["email"]
    
    def test_get_participants_returns_correct_count(self, client, created_event, 
                                                    sample_event_data):
        """Test that participant count matches registrations."""
        event_id = created_event["id"]
        
        # Register 5 participants
        for i in range(5):
            client.post(
                f"/events/{event_id}/register",
                json={
                    "name": f"Participant {i+1}",
                    "email": f"participant{i+1}@example.com"
                }
            )
        
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5
    
    def test_get_participants_after_deletion(self, client, created_event, 
                                            sample_participant_data):
        """Test getting participants after event deletion."""
        event_id = created_event["id"]
        
        # Register a participant
        client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        
        # Delete the event
        client.delete(f"/events/{event_id}")
        
        # Try to get participants
        response = client.get(f"/events/{event_id}/participants")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCapacityManagement:
    """Test cases focused on capacity management logic."""
    
    def test_capacity_check_exact_fill(self, client):
        """Test capacity enforcement when filled exactly."""
        from datetime import datetime, timedelta, timezone
        
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=2)
        
        # Create event with capacity of 3
        event_data = {
            "title": "Capacity Test Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 3
        }
        
        response = client.post("/events/", json=event_data)
        event_id = response.json()["id"]
        
        # Register exactly 3 participants
        for i in range(3):
            response = client.post(
                f"/events/{event_id}/register",
                json={
                    "name": f"Person {i+1}",
                    "email": f"person{i+1}@example.com"
                }
            )
            assert response.status_code == status.HTTP_201_CREATED
        
        # Try to register 4th participant (should fail)
        response = client.post(
            f"/events/{event_id}/register",
            json={
                "name": "Person 4",
                "email": "person4@example.com"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_capacity_with_one_slot(self, client):
        """Test capacity management with capacity of 1."""
        from datetime import datetime, timedelta, timezone
        
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=2)
        
        # Create event with capacity of 1
        event_data = {
            "title": "Single Slot Event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_capacity": 1
        }
        
        response = client.post("/events/", json=event_data)
        event_id = response.json()["id"]
        
        # Register the only slot
        response1 = client.post(
            f"/events/{event_id}/register",
            json={"name": "Only Person", "email": "only@example.com"}
        )
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to register another participant
        response2 = client.post(
            f"/events/{event_id}/register",
            json={"name": "Second Person", "email": "second@example.com"}
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST


class TestEventIntegration:
    """Integration tests combining event and participant operations."""
    
    def test_create_event_register_get_workflow(self, client, sample_event_data, 
                                               sample_participant_data):
        """Test complete workflow: create event, register participant, get both."""
        # Create event
        response = client.post("/events/", json=sample_event_data)
        event = response.json()
        event_id = event["id"]
        
        # Verify event created
        response = client.get(f"/events/{event_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Register participant
        response = client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        participant = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        
        # Get participants
        response = client.get(f"/events/{event_id}/participants")
        participants = response.json()
        assert len(participants) == 1
        assert participants[0]["email"] == sample_participant_data["email"]
    
    def test_update_capacity_affects_registration(self, client, sample_event_data, 
                                                  sample_participant_data):
        """Test that capacity changes affect registration availability."""
        # Create event with capacity 2
        response = client.post("/events/", json=sample_event_data)
        event_id = response.json()["id"]
        
        # Register participant
        client.post(
            f"/events/{event_id}/register",
            json=sample_participant_data
        )
        
        # Reduce capacity to 1
        client.put(f"/events/{event_id}", json={"max_capacity": 1})
        
        # Should still be able to query remaining slots
        response = client.get(f"/events/{event_id}/participants")
        assert len(response.json()) == 1
