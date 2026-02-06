# MindCare - Mental Health Support App 💜

A comprehensive mental health support application designed to help individuals manage depression through mood tracking, coping strategies, goal setting, and community support.

## 🌟 Features

### Core Features
- **Mood Tracking** - Log daily moods with visual trend analysis using interactive Plotly charts
- **Coping Strategies** - Access 6+ evidence-based techniques for managing depression
- **Goal Setting** - Set and track daily/weekly goals with progress monitoring
- **Peer Support Community** - Share experiences and support others
- **Professional Support** - Access to crisis hotlines and therapy options
- **Medication Reminders** - Track medication schedules
- **Private Journal** - Secure space for thoughts and self-reflection
- **Educational Resources** - Articles and videos on depression management

### Technical Features
- Built with **Python** and **Streamlit** for a responsive web interface
- **Plotly** for interactive data visualizations
- Custom **CSS** styling for a calming, accessible design
- Session state management for data persistence during runtime
- Responsive design that works on desktop and mobile

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project files**
   ```bash
   # Create a project directory
   mkdir mindcare-app
   cd mindcare-app
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:
   - streamlit==1.31.0
   - pandas==2.1.4
   - plotly==5.18.0
   - python-dateutil==2.8.2

3. **Ensure all files are in the same directory**
   ```
   mindcare-app/
   ├── app.py
   ├── style.css
   ├── requirements.txt
   └── README.md
   ```

## 💻 Running the Application

1. **Start the Streamlit server**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

3. **Using the app**
   - Use the sidebar to navigate between different sections
   - Start by logging your mood on the Home page
   - Explore coping strategies, set goals, and engage with the community
   - All data is stored in session state (will reset when you close the browser)

## 📱 Features Guide

### Home Dashboard
- Quick mood logging with emoji-based selection
- Today's goals overview
- Quick action buttons to navigate features

### Mood Tracking
- Log moods on a 1-5 scale (Very Low to Great)
- View interactive trend charts powered by Plotly
- See average mood scores and progress metrics

### Coping Strategies
- 6 evidence-based techniques:
  - Deep Breathing (4-7-8 technique)
  - Mindful Walking
  - Gratitude Journaling
  - Progressive Muscle Relaxation
  - 5-4-3-2-1 Grounding Exercise
  - Positive Affirmations

### Goal Setting
- Add daily/weekly goals
- Track completion with checkboxes
- View progress statistics
- Delete completed goals

### Community Support
- Share experiences anonymously
- Support others with likes and comments
- Build connections with peers

### Professional Support
- **Crisis Hotlines**: 988 (National Suicide Prevention Lifeline)
- Therapy options: Video, Chat, Phone, Group
- Quick access to help resources

### Medication Management
- Add medication names and times
- Mark medications as taken
- Daily reminder tracking

### Private Journal
- Write secure journal entries
- View past entries chronologically
- Safe space for self-reflection

### Educational Resources
- Articles and videos on depression
- Learn about CBT, mindfulness, and healthy habits
- Evidence-based mental health information

## 🎨 Customization

### Modifying Colors
Edit the `style.css` file to change:
- Primary gradient colors (currently purple to pink)
- Button styles
- Background gradients
- Component styling

### Adding Features
The app uses Streamlit's session state for data persistence. To add new features:
1. Initialize state in the session_state section
2. Create functions to manage the data
3. Add UI components in the appropriate page section

## 🔒 Data Privacy

- All data is stored locally in browser session
- No data is sent to external servers
- Journal entries remain completely private
- Data resets when browser is closed

## 🌐 Accessibility Features

- Dark mode toggle (can be extended)
- High contrast text
- Clear, readable fonts
- Responsive design for all screen sizes
- Emoji indicators for visual communication

## 📊 Technologies Used

- **Python 3.8+** - Core programming language
- **Streamlit 1.31.0** - Web framework for the interface
- **Plotly 5.18.0** - Interactive data visualizations
- **Pandas 2.1.4** - Data manipulation and analysis
- **CSS3** - Custom styling and design

## 🤝 Contributing

This is a hackathon project. Suggestions for improvements:
- Add data export functionality (CSV, PDF reports)
- Implement user authentication
- Add database integration for persistent storage
- Expand educational content library
- Add more visualization options
- Implement notification system
- Add multilingual support

## 📋 Hackathon Requirements Checklist

✅ Name and Branding: "MindCare"
✅ User Interface: Calming colors, intuitive navigation
✅ Mood Tracking: Visual mood logging with trend charts
✅ Coping Strategies: Library of techniques
✅ Goal Setting: Task management with progress tracking
✅ Peer Support: Community posting feature
✅ Professional Support: Crisis hotlines and therapy access
✅ Medication Reminders: Scheduling and tracking
✅ Journaling: Private, secure space
✅ Educational Resources: Articles and videos
✅ Accessibility: Responsive design, clear UI

## 🆘 Crisis Resources

If you or someone you know is in crisis:

- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

## 📄 License

This project is created for educational and hackathon purposes.

## 👨‍💻 Author

Built for GUVI Hackathon - Mental Health Support App Challenge

---

**Remember**: This app is a supportive tool and does not replace professional mental health care. If you're struggling, please reach out to a mental health professional or crisis hotline.

**Recovery is possible. You are not alone. Help is available.** 💜
