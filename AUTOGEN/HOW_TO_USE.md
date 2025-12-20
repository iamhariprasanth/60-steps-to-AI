# 🍝 La Bella Italia - AI Restaurant Assistant

## How to Use Guide

A multi-agent AI-powered restaurant assistant built with AutoGen and Streamlit, featuring human-in-the-loop order confirmation.

---

## 📋 Table of Contents

1. [Setup & Installation](#setup--installation)
2. [Running the App](#running-the-app)
3. [Features Overview](#features-overview)
4. [How to Use](#how-to-use)
5. [Agent System](#agent-system)
6. [Human-in-the-Loop Ordering](#human-in-the-loop-ordering)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Setup & Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Step 1: Create a Virtual Environment

```bash
cd /Users/hariprasanthmadhavan/AUTOGEN
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Or copy from the example:

```bash
cp .env.example .env
# Then edit .env with your actual API key
```

---

## 🚀 Running the App

Start the Streamlit application:

```bash
streamlit run restaurant_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## ✨ Features Overview

| Feature | Description |
|---------|-------------|
| 🤖 Multi-Agent System | 4 specialized AI agents handle different tasks |
| 💬 Chat Interface | Natural conversation with the AI assistant |
| 📋 Full Menu | Browse appetizers, mains, desserts & beverages |
| 🌟 Smart Recommendations | Get personalized food suggestions |
| 🛒 Order Placement | Place orders with modifications |
| 👤 Human-in-the-Loop | Review and confirm orders before finalizing |
| 📜 Order History | Track your confirmed orders |

---

## 📖 How to Use

### The Interface

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR                │  MAIN AREA                        │
│  ────────               │  ─────────                        │
│  📋 Menu                │  🍝 La Bella Italia               │
│  • Appetizers           │  AI Restaurant Assistant          │
│  • Main Courses         │                                   │
│  • Desserts             │  [Chat Messages]                  │
│  • Beverages            │                                   │
│                         │  [Order Confirmation Panel]       │
│  📢 Today's Specials    │  (when ordering)                  │
│                         │                                   │
│  📍 Restaurant Info     │  [Chat Input Box]                 │
│                         │                                   │
│  📜 Order History       │  [Quick Action Buttons]           │
│                         │  📋 View Menu                     │
│                         │  🌟 Get Recommendations           │
│                         │  🛒 Place Order                   │
│                         │  ℹ️ Restaurant Info               │
└─────────────────────────────────────────────────────────────┘
```

### Quick Actions

Click any of the quick action buttons to:

- **📋 View Menu** - See the complete menu with prices
- **🌟 Get Recommendations** - Get AI-powered food suggestions
- **🛒 Place Order** - Start the ordering process
- **ℹ️ Restaurant Info** - Get hours, location, and contact info

### Example Conversations

#### Viewing the Menu
```
You: "Show me the menu"
AI: [Displays categorized menu with prices and dietary info]
```

#### Getting Recommendations
```
You: "I'm vegetarian, what do you recommend?"
AI: "For a vegetarian dining experience, I recommend:
     - Caprese Salad ($10.99) - Fresh mozzarella with tomatoes
     - Margherita Pizza ($16.99) - Classic with basil
     - Vegetable Risotto ($17.99) - Creamy and satisfying
     ..."
```

#### Placing an Order
```
You: "I'd like to order a Margherita Pizza and Tiramisu"
AI: [Confirms items, calculates total, asks for order type]
You: "That's for dine-in please"
AI: [Presents order summary for confirmation]
```

---

## 🤖 Agent System

The app uses 4 specialized AI agents:

### 1. Host Agent 👋
**Handles:** Greetings, restaurant info, hours, reservations

**Example triggers:**
- "Hello"
- "What are your hours?"
- "Where are you located?"
- "Do you take reservations?"

### 2. Menu Agent 📋
**Handles:** Menu items, ingredients, dietary restrictions, prices

**Example triggers:**
- "Show me the menu"
- "What's in the Carbonara?"
- "Do you have gluten-free options?"
- "How much is the salmon?"

### 3. Order Agent 🛒
**Handles:** Taking orders, modifications, calculating totals

**Example triggers:**
- "I'd like to order..."
- "Can I add extra cheese?"
- "What's my total?"
- "I want delivery"

### 4. Recommendations Agent 🌟
**Handles:** Food suggestions, wine pairings, helping you choose

**Example triggers:**
- "What do you recommend?"
- "I'm not sure what to get"
- "What wine goes with salmon?"
- "What's popular here?"

---

## 👤 Human-in-the-Loop Ordering

### Why Human-in-the-Loop?

All orders require your explicit approval before being placed. This ensures:
- ✅ Order accuracy
- ✅ Ability to make last-minute changes
- ✅ Full control over your order
- ✅ Review of total cost before confirming

### Order Confirmation Flow

```
Step 1: Chat with AI to build your order
        ↓
Step 2: AI presents ORDER SUMMARY
        ↓
Step 3: Review order details
        • Items and prices
        • Subtotal, tax, total
        • Order type (dine-in/delivery/takeout)
        ↓
Step 4: Modify if needed
        • Change order type
        • Add special instructions
        ↓
Step 5: Choose action:
        ┌────────────────────────────────────────┐
        │ ✅ Confirm Order │ ✏️ Modify │ ❌ Cancel │
        └────────────────────────────────────────┘
```

### Confirmation Panel

When an order is ready, you'll see:

```
┌─────────────────────────────────────────┐
│  🛒 Order Pending Confirmation          │
│                                         │
│  📋 Order Summary:                      │
│  • 1x Margherita Pizza - $16.99         │
│  • 1x Tiramisu - $8.99                  │
│                                         │
│  Subtotal: $25.98                       │
│  Tax (8.5%): $2.21                      │
│  Total: $28.19                          │
│                                         │
│  Order Type: [dine-in ▼]                │
│  Special Instructions: [____________]    │
│                                         │
│  👤 Human Approval Required             │
│  [✅ Confirm] [✏️ Modify] [❌ Cancel]    │
└─────────────────────────────────────────┘
```

### Button Actions

| Button | Action |
|--------|--------|
| ✅ **Confirm Order** | Finalizes the order, saves to history |
| ✏️ **Modify Order** | Returns to chat to make changes |
| ❌ **Cancel Order** | Cancels the order completely |

> ⚠️ **Note:** Chat is disabled while an order is pending confirmation.

---

## 🔍 Troubleshooting

### Common Issues

#### "OpenAI API key not found"
**Solution:** Create a `.env` file with your API key:
```
OPENAI_API_KEY=sk-your-key-here
```

#### App won't start
**Solution:** Make sure you're in the virtual environment:
```bash
source .venv/bin/activate
streamlit run restaurant_app.py
```

#### Slow responses
**Solution:** This is normal for AI responses. The app uses GPT-4o-mini for faster responses.

#### Order not showing confirmation panel
**Solution:** Make sure you've completed the full order flow:
1. Tell the AI what you want to order
2. Confirm the items
3. Specify dine-in/delivery/takeout
4. The AI will then present the order for confirmation

### Reset the App

To clear all chat history and pending orders:
1. Click the **🗑️ Clear Chat** button
2. Or refresh the browser page

---

## 📞 Restaurant Information

**La Bella Italia**
- 📍 Address: 123 Main Street, Food City, FC 12345
- ☎️ Phone: (555) 123-4567
- 🚗 Parking: Free parking in rear lot

**Hours:**
- Monday-Thursday: 11:00 AM - 10:00 PM
- Friday-Saturday: 11:00 AM - 11:00 PM
- Sunday: 12:00 PM - 9:00 PM

**Services:**
- ✅ Dine-in
- ✅ Delivery
- ✅ Takeout
- ✅ Reservations

---

## 📁 Project Files

```
AUTOGEN/
├── restaurant_app.py     # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .env.example          # Example environment file
├── HOW_TO_USE.md         # This guide
└── README.md             # Project overview
```

---

## 🎉 Enjoy Your Dining Experience!

Feel free to explore the menu, get recommendations, and place orders. The AI assistant is here to help make your dining experience seamless and enjoyable!

**Buon Appetito! 🍝**
