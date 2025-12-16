#!/usr/bin/env python3
"""Generate a LiveKit access token for testing."""

from livekit import api
import os

# Configuration
API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret12345678901234567890123456")
ROOM_NAME = "test-room"
PARTICIPANT_NAME = "test-user"

def generate_token():
    token = api.AccessToken(API_KEY, API_SECRET)
    token.with_identity(PARTICIPANT_NAME)
    token.with_name(PARTICIPANT_NAME)
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=ROOM_NAME,
    ))
    
    jwt_token = token.to_jwt()
    print(f"\n🔑 LiveKit Access Token Generated\n")
    print(f"Room: {ROOM_NAME}")
    print(f"Identity: {PARTICIPANT_NAME}")
    print(f"\nToken:\n{jwt_token}")
    print(f"\n📱 Connect using:")
    print(f"   URL: ws://localhost:7880")
    print(f"   Token: (see above)")
    print(f"\n🌐 Or open in browser:")
    print(f"   https://meet.livekit.io/?tab=custom")
    print(f"   - Set LiveKit URL to: ws://localhost:7880")
    print(f"   - Paste the token above")
    
    return jwt_token

if __name__ == "__main__":
    generate_token()
