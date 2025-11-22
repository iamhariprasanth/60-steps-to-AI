# 💪 Gym Workout Logger

A modern, interactive web application to log and track your gym workouts with advanced analytics and motivational features.

## Features

### 📋 Workout Logging
- **Log Exercises**: Record exercise name, sets, reps, and weight
- **Quick Entry**: Pre-populated common exercises (Bench Press, Squats, Deadlifts, etc.)
- **Notes Section**: Add custom notes to each workout
- **Data Persistence**: All workouts stored in JSON format

### 📊 Dashboard
- **Real-time Stats**: 
  - Total workouts count
  - This week's workout count
  - Total weight lifted (kg)
  - Favorite exercise
- **Recent Workouts Table**: View and manage your last 10 workouts
- **Weekly Progress Chart**: Visual representation of exercises and reps completed each day

### 📈 Analytics & Trends
- **Trend Chart**: Track weight progression over time for each exercise
- **Donut Chart**: Exercise distribution - see which exercises you do most
- **Reps Chart**: Total reps by exercise - horizontal bar chart for easy comparison

### 🎞️ Motivational Slider
- **5 Rotating Slides**: Beautiful gym images paired with motivational quotes
- **Auto-advance**: Slides automatically rotate every 8 seconds
- **Manual Navigation**: Use arrow buttons or dots to navigate between slides
- **Gym-themed Quotes**: Inspiring messages to keep you motivated

### 🎨 Design Features
- **Dark Gym Theme**: Professional dark background with gym-themed patterns
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Engaging transitions and hover effects
- **Glassmorphism**: Modern frosted glass effect on UI elements
- **Color Scheme**: Vibrant reds and teals inspired by fitness energy

## Project Structure

```
GymWorkoutLogger/
├── app.py                 # Flask application with all routes
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main application template
├── static/
│   ├── css/
│   │   └── style.css     # Complete styling
│   ├── js/
│   │   └── script.js     # Frontend logic and charts
│   └── images/           # (Optional) Local image storage
└── workout_data.json     # Auto-generated workout database
```

## Installation

1. **Clone/Download the project**
   ```bash
   cd GymWorkoutLogger
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## How to Use

### 1. **Log a Workout**
   - Go to "Log Workout" tab
   - Select exercise from the dropdown
   - Enter sets, reps, and weight
   - Add optional notes
   - Click "Log Workout" to save

### 2. **View Dashboard**
   - See your workout statistics
   - View recent workouts in the table
   - Check weekly progress chart
   - Delete old workouts if needed

### 3. **View Analytics**
   - See trend lines for weight progression
   - View exercise distribution (donut chart)
   - Check total reps by exercise
   - Analyze your training patterns

### 4. **Get Motivated**
   - Watch the motivational slider
   - Let inspiring quotes keep you focused
   - Click arrows or dots to navigate between quotes

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main dashboard page |
| POST | `/add-workout` | Add new workout entry |
| GET | `/get-workouts` | Retrieve all workouts |
| GET | `/get-weekly-stats` | Get weekly statistics |
| GET | `/get-exercise-stats` | Get stats by exercise |
| GET | `/get-trends` | Get weight trends by exercise |
| DELETE | `/delete-workout/<id>` | Delete specific workout |

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Data Storage**: JSON
- **External**: Unsplash API for gym images

## Data Format

Workouts are stored in `workout_data.json`:

```json
{
  "workouts": [
    {
      "id": 1,
      "date": "2024-01-15 10:30:00",
      "exercise": "Bench Press",
      "sets": 4,
      "reps": 8,
      "weight": 100.0,
      "notes": "Good form today"
    }
  ]
}
```

## Customization

### Adding More Exercises
Edit the exercise dropdown in `templates/index.html` under the select element with id `exercise`.

### Changing Colors
Update CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #FF6B6B;      /* Main red */
    --secondary-color: #4ECDC4;    /* Main teal */
    --accent-color: #FFA07A;       /* Light salmon */
}
```

### Modifying Motivational Quotes
Edit the slide content in `templates/index.html` to add your own images and quotes.

## Features Included ✅

- ✅ Exercise logging with sets, reps, weight
- ✅ Data stored in table format (JSON)
- ✅ Weekly progress graph
- ✅ Trend chart for weight progression
- ✅ Donut chart for exercise distribution
- ✅ Gym-themed background with motivation messages
- ✅ Image slider with motivational quotes
- ✅ Responsive design
- ✅ Delete functionality for workouts
- ✅ Real-time statistics dashboard

## Future Enhancements

- User authentication and profiles
- Cloud database integration
- Export workouts to PDF
- Mobile app version
- Strength progression goals
- Exercise video tutorials
- Community features
- Meal tracking integration

## Troubleshooting

**Issue**: Port 5000 already in use
- Solution: Change `port=5000` to another port in `app.py`

**Issue**: Workouts not saving
- Solution: Ensure the script has write permissions in the directory

**Issue**: Charts not displaying
- Solution: Check browser console for errors and ensure Chart.js CDN is accessible

## License

Open source - feel free to use and modify!

## Support

For issues or suggestions, feel free to modify and extend this application!

---

**Stay consistent, stay strong! 💪**
