#!/usr/bin/env python3
"""
Multi-Agent AutoGen Restaurant Assistant - Streamlit App
A conversational AI system for a food restaurant using AutoGen agents.
"""

import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Sequence
from dataclasses import dataclass
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

# ============== Restaurant Data ==============

MENU = {
    "appetizers": [
        {"name": "Bruschetta", "price": 8.99, "description": "Toasted bread with tomatoes, basil, and olive oil", "dietary": ["vegetarian"]},
        {"name": "Calamari Fritti", "price": 12.99, "description": "Crispy fried calamari with marinara sauce", "dietary": []},
        {"name": "Caprese Salad", "price": 10.99, "description": "Fresh mozzarella, tomatoes, and basil", "dietary": ["vegetarian", "gluten-free"]},
        {"name": "Garlic Bread", "price": 5.99, "description": "Toasted bread with garlic butter", "dietary": ["vegetarian"]},
        {"name": "Soup of the Day", "price": 6.99, "description": "Ask your server for today's selection", "dietary": []},
    ],
    "main_courses": [
        {"name": "Spaghetti Carbonara", "price": 18.99, "description": "Classic pasta with egg, cheese, pancetta", "dietary": []},
        {"name": "Grilled Salmon", "price": 24.99, "description": "Atlantic salmon with lemon herb butter", "dietary": ["gluten-free"]},
        {"name": "Chicken Parmesan", "price": 19.99, "description": "Breaded chicken with marinara and mozzarella", "dietary": []},
        {"name": "Margherita Pizza", "price": 16.99, "description": "Classic pizza with tomato, mozzarella, basil", "dietary": ["vegetarian"]},
        {"name": "Beef Tenderloin", "price": 32.99, "description": "8oz filet with red wine reduction", "dietary": ["gluten-free"]},
        {"name": "Vegetable Risotto", "price": 17.99, "description": "Creamy arborio rice with seasonal vegetables", "dietary": ["vegetarian", "gluten-free"]},
        {"name": "Seafood Linguine", "price": 26.99, "description": "Pasta with shrimp, mussels, and clams", "dietary": []},
        {"name": "Eggplant Parmesan", "price": 16.99, "description": "Layered eggplant with marinara and cheese", "dietary": ["vegetarian"]},
    ],
    "desserts": [
        {"name": "Tiramisu", "price": 8.99, "description": "Classic Italian coffee-flavored dessert", "dietary": ["vegetarian"]},
        {"name": "Panna Cotta", "price": 7.99, "description": "Italian cream dessert with berry sauce", "dietary": ["vegetarian", "gluten-free"]},
        {"name": "Chocolate Lava Cake", "price": 9.99, "description": "Warm chocolate cake with molten center", "dietary": ["vegetarian"]},
        {"name": "Gelato", "price": 6.99, "description": "Three scoops of Italian ice cream", "dietary": ["vegetarian", "gluten-free"]},
    ],
    "beverages": [
        {"name": "Espresso", "price": 3.99, "description": "Single shot of Italian espresso", "dietary": ["vegan", "gluten-free"]},
        {"name": "Cappuccino", "price": 4.99, "description": "Espresso with steamed milk foam", "dietary": ["vegetarian", "gluten-free"]},
        {"name": "House Wine (Glass)", "price": 8.99, "description": "Red or white, ask server for selection", "dietary": ["vegan", "gluten-free"]},
        {"name": "Soft Drinks", "price": 2.99, "description": "Coke, Sprite, or Fanta", "dietary": ["vegan", "gluten-free"]},
        {"name": "Sparkling Water", "price": 3.99, "description": "San Pellegrino", "dietary": ["vegan", "gluten-free"]},
    ]
}

RESTAURANT_INFO = {
    "name": "La Bella Italia",
    "cuisine": "Italian",
    "hours": {
        "Monday-Thursday": "11:00 AM - 10:00 PM",
        "Friday-Saturday": "11:00 AM - 11:00 PM",
        "Sunday": "12:00 PM - 9:00 PM"
    },
    "address": "123 Main Street, Food City, FC 12345",
    "phone": "(555) 123-4567",
    "reservations": True,
    "delivery": True,
    "takeout": True,
    "parking": "Free parking available in rear lot",
    "special_features": ["Private dining room", "Outdoor patio", "Full bar", "Live music on weekends"]
}

SPECIALS = [
    {"name": "Early Bird Special", "description": "20% off all entrees before 6 PM", "days": "Monday-Thursday"},
    {"name": "Wine Wednesday", "description": "Half-price bottles of wine", "days": "Wednesday"},
    {"name": "Family Sunday", "description": "Kids eat free with adult entree purchase", "days": "Sunday"},
    {"name": "Chef's Tasting Menu", "description": "5-course meal for $65 per person", "days": "Friday-Saturday"},
]

# ============== Agent System Prompts ==============

HOST_AGENT_PROMPT = """You are the friendly Host Agent for La Bella Italia restaurant. Your responsibilities include:
- Welcoming guests warmly
- Providing information about restaurant hours, location, and general policies
- Helping with reservation inquiries
- Directing customers to the appropriate specialist (Menu Expert, Order Specialist, or Recommendations Agent)
- Answering general questions about the restaurant

Restaurant Info:
{restaurant_info}

Always be warm, professional, and helpful. If a customer asks about the menu, food recommendations, or wants to place an order, 
mention that you'll connect them with the appropriate specialist. Keep responses concise but friendly.

When conversation is complete or customer says goodbye/thanks, respond with "TERMINATE" at the end."""

MENU_AGENT_PROMPT = """You are the Menu Expert Agent for La Bella Italia restaurant. Your responsibilities include:
- Presenting menu items with descriptions and prices
- Explaining ingredients and preparation methods
- Answering questions about dietary restrictions (vegetarian, gluten-free, etc.)
- Providing detailed information about any dish

Full Menu:
{menu}

Daily Specials:
{specials}

Be knowledgeable and descriptive about the food. Help customers understand what each dish contains.
Format prices clearly and mention dietary options when relevant.

When the conversation is complete or if customer wants to order, include "TERMINATE" at the end."""

ORDER_AGENT_PROMPT = """You are the Order Specialist Agent for La Bella Italia restaurant. Your responsibilities include:
- Taking and confirming food orders
- Calculating totals (include 8.5% tax)
- Handling special requests and modifications
- Confirming delivery/pickup preferences
- Processing the order summary

Menu with Prices:
{menu}

When taking orders:
1. Confirm each item clearly
2. Ask about any modifications or allergies
3. Provide subtotal, tax, and total
4. Confirm delivery/pickup/dine-in preference

IMPORTANT: When the customer confirms they want to place the order, you MUST format the final order as a JSON block like this:
```ORDER_JSON
{{
    "items": [
        {{"name": "Item Name", "price": 00.00, "quantity": 1, "modifications": "any special requests"}}
    ],
    "subtotal": 00.00,
    "tax": 0.00,
    "total": 00.00,
    "order_type": "dine-in/delivery/takeout",
    "special_instructions": "any overall notes"
}}
```

After providing the ORDER_JSON, say "Please review your order above and click 'Confirm Order' to finalize, or 'Modify Order' to make changes."
Do NOT say the order is placed - it needs human confirmation first.
Include "TERMINATE" at the end after the JSON block."""

RECOMMENDATIONS_AGENT_PROMPT = """You are the Food Recommendations Agent for La Bella Italia restaurant. Your responsibilities include:
- Suggesting dishes based on customer preferences
- Recommending wine pairings
- Suggesting appetizer and dessert combinations
- Helping indecisive customers make choices
- Considering dietary restrictions in recommendations

Full Menu:
{menu}

Daily Specials:
{specials}

Ask about preferences (spicy/mild, meat/seafood/vegetarian, etc.) and dietary needs.
Make personalized recommendations with enthusiasm. Explain why you're recommending each dish.

When recommendations are complete, include "TERMINATE" at the end."""

COORDINATOR_PROMPT = """You are the Restaurant Coordinator Agent. Your job is to:
1. Understand customer requests
2. Route to the appropriate specialist agent:
   - Host Agent: General restaurant info, hours, reservations, directions
   - Menu Agent: Menu questions, ingredients, dietary info
   - Order Agent: Placing orders, modifications, calculating totals
   - Recommendations Agent: Food suggestions, pairings, help choosing

Analyze the customer message and delegate to the right agent. Be brief in your routing decisions.
After the specialist has helped, check if the customer needs anything else.

When the conversation is truly complete (customer says goodbye/thanks/done), respond with "TERMINATE"."""

# ============== Helper Functions ==============

def format_menu_for_prompt() -> str:
    """Format the menu dictionary as a readable string for agent prompts."""
    lines = []
    for category, items in MENU.items():
        lines.append(f"\n{category.upper().replace('_', ' ')}:")
        for item in items:
            dietary = f" [{', '.join(item['dietary'])}]" if item['dietary'] else ""
            lines.append(f"  • {item['name']} - ${item['price']:.2f}{dietary}")
            lines.append(f"    {item['description']}")
    return "\n".join(lines)

def format_specials_for_prompt() -> str:
    """Format specials as a readable string."""
    lines = []
    for special in SPECIALS:
        lines.append(f"• {special['name']} ({special['days']}): {special['description']}")
    return "\n".join(lines)

def format_restaurant_info() -> str:
    """Format restaurant info as a readable string."""
    info = RESTAURANT_INFO
    lines = [
        f"Restaurant: {info['name']}",
        f"Cuisine: {info['cuisine']}",
        f"Address: {info['address']}",
        f"Phone: {info['phone']}",
        "\nHours:",
    ]
    for day, hours in info['hours'].items():
        lines.append(f"  {day}: {hours}")
    lines.append(f"\nServices: {'Reservations, ' if info['reservations'] else ''}{'Delivery, ' if info['delivery'] else ''}{'Takeout' if info['takeout'] else ''}")
    lines.append(f"Parking: {info['parking']}")
    lines.append(f"Features: {', '.join(info['special_features'])}")
    return "\n".join(lines)

def extract_order_json(response: str) -> dict | None:
    """Extract ORDER_JSON from agent response."""
    import re
    pattern = r'```ORDER_JSON\s*([\s\S]*?)```'
    match = re.search(pattern, response)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    return None

def format_order_for_display(order: dict) -> str:
    """Format order dict as readable string."""
    lines = ["📋 **Order Summary:**\n"]
    for item in order.get('items', []):
        qty = item.get('quantity', 1)
        name = item.get('name', 'Unknown')
        price = item.get('price', 0)
        mods = item.get('modifications', '')
        lines.append(f"  • {qty}x {name} - ${price:.2f}")
        if mods:
            lines.append(f"    _Modifications: {mods}_")
    lines.append(f"\n**Subtotal:** ${order.get('subtotal', 0):.2f}")
    lines.append(f"**Tax (8.5%):** ${order.get('tax', 0):.2f}")
    lines.append(f"**Total:** ${order.get('total', 0):.2f}")
    lines.append(f"\n**Order Type:** {order.get('order_type', 'Not specified')}")
    if order.get('special_instructions'):
        lines.append(f"**Special Instructions:** {order.get('special_instructions')}")
    return "\n".join(lines)

# ============== Streamlit App ==============

def init_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "order_items" not in st.session_state:
        st.session_state.order_items = []
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    if "pending_order" not in st.session_state:
        st.session_state.pending_order = None
    if "order_history" not in st.session_state:
        st.session_state.order_history = []
    if "awaiting_confirmation" not in st.session_state:
        st.session_state.awaiting_confirmation = False

async def run_restaurant_chat(user_message: str) -> str:
    """Run the multi-agent chat system and return the response."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."
    
    try:
        # Create the model client
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=api_key
        )
    except Exception as e:
        return f"⚠️ Error creating model client: {str(e)}"
    
    # Format data for prompts
    menu_str = format_menu_for_prompt()
    specials_str = format_specials_for_prompt()
    restaurant_info_str = format_restaurant_info()
    
    # Build conversation history for context
    history = []
    for msg in st.session_state.messages[-6:]:  # Last 3 exchanges
        if msg["role"] == "user":
            history.append(f"Customer: {msg['content']}")
        else:
            history.append(f"Assistant: {msg['content']}")
    
    history_str = "\n".join(history) if history else "No previous conversation."
    
    # Create a comprehensive restaurant assistant agent
    unified_system_prompt = f"""You are the AI Assistant for La Bella Italia, an Italian restaurant. 
You handle ALL customer interactions including:

1. **Greetings & General Info**: Welcome customers, provide restaurant hours, location, reservations
2. **Menu Questions**: Explain dishes, prices, ingredients, dietary options (vegetarian, gluten-free)
3. **Recommendations**: Suggest dishes based on preferences, wine pairings, popular items
4. **Taking Orders**: Confirm items, calculate totals with 8.5% tax, handle modifications

RESTAURANT INFO:
{restaurant_info_str}

FULL MENU:
{menu_str}

TODAY'S SPECIALS:
{specials_str}

PREVIOUS CONVERSATION:
{history_str}

GUIDELINES:
- Be warm, friendly, and professional
- When recommending, explain WHY you're suggesting each dish
- For orders: confirm items, ask about modifications/allergies, calculate totals accurately
- Always include prices when discussing menu items

WHEN PLACING ORDERS:
When customer confirms their order, format as JSON:
```ORDER_JSON
{{
    "items": [{{"name": "Item", "price": 0.00, "quantity": 1, "modifications": ""}}],
    "subtotal": 0.00,
    "tax": 0.00,
    "total": 0.00,
    "order_type": "dine-in/delivery/takeout",
    "special_instructions": ""
}}
```
Then say "Please review your order and confirm."

Respond naturally to the customer's message."""

    try:
        # Create the unified assistant agent
        restaurant_agent = AssistantAgent(
            name="Restaurant_Assistant",
            model_client=model_client,
            system_message=unified_system_prompt,
        )
        
        # Run the agent
        result = await restaurant_agent.run(task=user_message)
        
        response_text = ""
        
        # Extract the response
        if hasattr(result, 'messages') and result.messages:
            for msg in result.messages:
                if hasattr(msg, 'content') and msg.content:
                    content = str(msg.content)
                    # Skip the task message
                    if content == user_message:
                        continue
                    response_text = content.replace("TERMINATE", "").strip()
                    
    except Exception as e:
        import traceback
        print(f"Agent error: {traceback.format_exc()}")
        return f"I apologize, I'm having trouble right now. Error: {str(e)}"
    
    # Check if response contains an order for human review
    order_data = extract_order_json(response_text)
    if order_data:
        st.session_state.pending_order = order_data
        st.session_state.awaiting_confirmation = True
        # Clean up the response to remove JSON block
        import re
        clean_response = re.sub(r'```ORDER_JSON[\s\S]*?```', '', response_text).strip()
        clean_response = clean_response.replace("TERMINATE", "").strip()
        return clean_response if clean_response else "I've prepared your order for review. Please confirm below."
    
    return response_text if response_text else "How can I assist you today?"

def display_pending_order():
    """Display pending order with human-in-the-loop confirmation."""
    if st.session_state.pending_order and st.session_state.awaiting_confirmation:
        order = st.session_state.pending_order
        
        st.markdown("---")
        st.markdown("## 🛒 Order Pending Confirmation")
        st.markdown("*Please review your order and confirm or modify:*")
        
        # Display order in a nice card
        with st.container():
            st.markdown(format_order_for_display(order))
        
        # Editable fields for human modification
        st.markdown("### ✏️ Modify Order (Optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            new_order_type = st.selectbox(
                "Order Type",
                ["dine-in", "delivery", "takeout"],
                index=["dine-in", "delivery", "takeout"].index(order.get('order_type', 'dine-in').lower()) if order.get('order_type', '').lower() in ["dine-in", "delivery", "takeout"] else 0
            )
        
        with col2:
            special_instructions = st.text_input(
                "Special Instructions",
                value=order.get('special_instructions', '')
            )
        
        # Action buttons
        st.markdown("### 👤 Human Approval Required")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Confirm Order", type="primary", use_container_width=True):
                # Update order with any modifications
                order['order_type'] = new_order_type
                order['special_instructions'] = special_instructions
                
                # Save to order history
                import datetime
                order['confirmed_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                order['status'] = 'confirmed'
                st.session_state.order_history.append(order)
                
                # Clear pending order
                st.session_state.pending_order = None
                st.session_state.awaiting_confirmation = False
                
                # Add confirmation message
                confirmation_msg = f"""✅ **Order Confirmed!**
                
{format_order_for_display(order)}

Your order has been placed successfully! 
Order #{len(st.session_state.order_history):04d}

Thank you for dining with La Bella Italia! 🍝"""
                st.session_state.messages.append({"role": "assistant", "content": confirmation_msg})
                st.success("Order confirmed successfully!")
                st.rerun()
        
        with col2:
            if st.button("✏️ Modify Order", use_container_width=True):
                st.session_state.awaiting_confirmation = False
                st.session_state.messages.append({"role": "user", "content": "I'd like to modify my order"})
                st.rerun()
        
        with col3:
            if st.button("❌ Cancel Order", use_container_width=True):
                st.session_state.pending_order = None
                st.session_state.awaiting_confirmation = False
                st.session_state.messages.append({"role": "assistant", "content": "Order cancelled. Is there anything else I can help you with?"})
                st.warning("Order cancelled.")
                st.rerun()
        
        st.markdown("---")
        return True
    return False

def display_order_history():
    """Display order history in sidebar."""
    if st.session_state.order_history:
        with st.sidebar:
            st.divider()
            st.subheader("📜 Order History")
            for i, order in enumerate(reversed(st.session_state.order_history[-5:])):
                with st.expander(f"Order #{len(st.session_state.order_history) - i:04d}"):
                    st.markdown(f"**Total:** ${order.get('total', 0):.2f}")
                    st.markdown(f"**Type:** {order.get('order_type', 'N/A')}")
                    st.markdown(f"**Time:** {order.get('confirmed_at', 'N/A')}")
                    st.caption(f"Items: {len(order.get('items', []))}")

def display_menu_sidebar():
    """Display the menu in the sidebar."""
    with st.sidebar:
        st.header("🍽️ La Bella Italia")
        st.subheader("Menu")
        
        for category, items in MENU.items():
            with st.expander(category.replace("_", " ").title()):
                for item in items:
                    dietary = f" ({', '.join(item['dietary'])})" if item['dietary'] else ""
                    st.markdown(f"**{item['name']}** - ${item['price']:.2f}{dietary}")
                    st.caption(item['description'])
        
        st.divider()
        st.subheader("📢 Today's Specials")
        for special in SPECIALS:
            st.markdown(f"**{special['name']}**")
            st.caption(f"{special['description']} ({special['days']})")
        
        st.divider()
        st.subheader("📍 Restaurant Info")
        st.markdown(f"**Address:** {RESTAURANT_INFO['address']}")
        st.markdown(f"**Phone:** {RESTAURANT_INFO['phone']}")
        
        with st.expander("Hours"):
            for day, hours in RESTAURANT_INFO['hours'].items():
                st.text(f"{day}: {hours}")

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="La Bella Italia - AI Assistant",
        page_icon="🍝",
        layout="wide"
    )
    
    init_session_state()
    display_menu_sidebar()
    display_order_history()
    
    # Main chat interface
    st.title("🍝 La Bella Italia")
    st.subheader("AI Restaurant Assistant")
    st.markdown("Welcome! I'm your AI assistant. Ask me about our menu, make recommendations, place orders, or get restaurant information.")
    st.info("🔔 **Human-in-the-Loop Ordering:** All orders require your explicit confirmation before being placed.")
    
    st.divider()
    
    # Display pending order confirmation (Human-in-the-Loop)
    has_pending_order = display_pending_order()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "👨‍🍳"):
                st.markdown(message["content"])
    
    # Chat input (disabled if awaiting order confirmation)
    if st.session_state.awaiting_confirmation:
        st.warning("⚠️ Please confirm or cancel your pending order above before continuing.")
        st.chat_input("Please confirm your order first...", disabled=True)
    else:
        if prompt := st.chat_input("How can I help you today? (e.g., 'Show me the menu', 'What do you recommend?', 'I'd like to place an order')"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant", avatar="👨‍🍳"):
                with st.spinner("Thinking..."):
                    response = asyncio.run(run_restaurant_chat(prompt))
                    st.markdown(response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to show order confirmation if needed
            if st.session_state.awaiting_confirmation:
                st.rerun()
    
    # Quick action buttons (disabled if awaiting confirmation)
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    disabled = st.session_state.awaiting_confirmation
    
    with col1:
        if st.button("📋 View Menu", use_container_width=True, disabled=disabled):
            st.session_state.messages.append({"role": "user", "content": "Can you show me the full menu?"})
            st.rerun()
    
    with col2:
        if st.button("🌟 Get Recommendations", use_container_width=True, disabled=disabled):
            st.session_state.messages.append({"role": "user", "content": "What dishes do you recommend?"})
            st.rerun()
    
    with col3:
        if st.button("🛒 Place Order", use_container_width=True, disabled=disabled):
            st.session_state.messages.append({"role": "user", "content": "I'd like to place an order"})
            st.rerun()
    
    with col4:
        if st.button("ℹ️ Restaurant Info", use_container_width=True, disabled=disabled):
            st.session_state.messages.append({"role": "user", "content": "Tell me about your restaurant hours and location"})
            st.rerun()
    
    # Clear chat button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.pending_order = None
            st.session_state.awaiting_confirmation = False
            st.rerun()

if __name__ == "__main__":
    main()
