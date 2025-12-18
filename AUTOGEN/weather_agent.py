#!/usr/bin/env python3
"""
Interactive AutoGen-style Weather Agent
- Prompts the user for a natural language question about the weather
- Uses the LLM (OpenAI) to extract a city name (if `OPENAI_API_KEY` is set)
- Uses Open-Meteo geocoding and weather APIs (no API key required)
- Prints current conditions with local date/time

Requirements: openai, httpx, python-dotenv
"""
from dotenv import load_dotenv
import os
import sys
import json
import time
import httpx
from datetime import datetime

try:
    import openai
except Exception:
    openai = None

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

WEATHER_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def extract_city_with_llm(question: str) -> str | None:
    """Use OpenAI to extract a city name from the user's question.
    Returns the city string or None on failure.
    """
    if not OPENAI_API_KEY or not openai:
        return None

    openai.api_key = OPENAI_API_KEY

    system = (
        "You are a helpful assistant that extracts a single city name from user questions."
        " Respond with only a JSON object with one key: \"city\"."
        " If you cannot identify a city, return {\"city\": null}."
    )
    user = f"Extract the city name from the following question: {question}"

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            max_tokens=60,
        )
        text = resp.choices[0].message.content.strip()
        # Try to parse JSON from the model output
        try:
            j = json.loads(text)
            city = j.get("city")
            if city:
                return city
        except json.JSONDecodeError:
            # fallback: try to extract a quoted string or last word
            if '"' in text or "'" in text:
                # crude
                parts = text.replace("\'", '"').split('"')
                for p in parts:
                    p = p.strip()
                    if p and not p.startswith('{') and len(p) < 60:
                        return p
            # last fallback
            return None
    except Exception:
        return None


def extract_city_fallback(question: str) -> str | None:
    """Very simple regex-like fallback to find common city patterns.
    Looks for 'in <City>' or 'for <City>' phrases.
    """
    q = question.strip().rstrip("?")
    lower = q.lower()
    for pre in [" in ", " for ", " at ", " near "]:
        if pre in lower:
            idx = lower.rfind(pre)
            candidate = q[idx + len(pre) :].strip()
            # remove trailing words like 'today' or 'now'
            for stop in [" today", " now", " right now", " please"]:
                if candidate.lower().endswith(stop):
                    candidate = candidate[: -len(stop)]
            # crude cleanup
            candidate = candidate.strip('"\' .')
            if candidate:
                # if contains comma, take first part
                if "," in candidate:
                    candidate = candidate.split(",")[0].strip()
                return candidate
    return None


def geocode_city(city: str) -> tuple[float, float, str] | None:
    """Use Open-Meteo geocoding to convert city -> (lat, lon, name_with_country)
    Returns None if not found.
    """
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    try:
        r = httpx.get(WEATHER_GEOCODE_URL, params=params, timeout=10.0)
        r.raise_for_status()
        j = r.json()
        results = j.get("results")
        if not results:
            return None
        top = results[0]
        return (top["latitude"], top["longitude"], f"{top.get('name')}, {top.get('country')}")
    except Exception:
        return None


WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def fetch_current_weather(lat: float, lon: float) -> dict | None:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }
    try:
        r = httpx.get(WEATHER_FORECAST_URL, params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def format_weather(city_name: str, weather_json: dict) -> str:
    cw = weather_json.get("current_weather", {})
    temp = cw.get("temperature")
    wind = cw.get("windspeed")
    code = cw.get("weathercode")
    time_str = cw.get("time") or datetime.utcnow().isoformat()
    tz = weather_json.get("timezone") or "UTC"
    desc = WEATHER_CODE_MAP.get(code, f"Weather code {code}")
    dt = time_str
    out = (
        f"Weather for {city_name} at {dt} ({tz}):\n"
        f"  Condition: {desc}\n"
        f"  Temperature: {temp} °C\n"
        f"  Wind speed: {wind} km/h"
    )
    return out


def main():
    print("Interactive Weather Agent — type 'exit' to quit")
    while True:
        try:
            question = input("Ask about the weather: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            break

        city = None
        if OPENAI_API_KEY and openai:
            city = extract_city_with_llm(question)
        if not city:
            city = extract_city_fallback(question)

        if not city:
            print("Could not determine a city from your question. Try: 'What's the weather in Paris?'\n")
            continue

        geo = geocode_city(city)
        if not geo:
            print(f"Could not geocode city: {city}\n")
            continue
        lat, lon, canonical = geo
        weather_json = fetch_current_weather(lat, lon)
        if not weather_json:
            print(f"Failed to fetch weather for {canonical}\n")
            continue
        out = format_weather(canonical, weather_json)
        print(out)
        print()


if __name__ == "__main__":
    main()
