import logging
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
    RoomInputOptions,
)
from livekit.plugins import openai, silero

load_dotenv()

logger = logging.getLogger("voice-assistant")
logger.setLevel(logging.INFO)


class VoiceAssistant(Agent):
    """A simple voice assistant agent."""
    
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a helpful voice assistant powered by LiveKit. "
                "You should be conversational, friendly, and concise in your responses. "
                "Keep responses brief since this is a voice conversation."
            ),
        )


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the voice assistant agent."""
    
    await ctx.connect()
    
    logger.info(f"Connected to room: {ctx.room.name}")
    
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )
    
    await session.start(
        agent=VoiceAssistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(),
    )
    
    logger.info("Voice assistant started")
    
    await session.say("Hello! I'm your voice assistant. How can I help you today?")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
