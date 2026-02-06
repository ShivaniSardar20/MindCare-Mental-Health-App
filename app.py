import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import uuid

# Page configuration
st.set_page_config(
    page_title="MindCare - Mental Health Support",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state with more realistic data
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Alex Johnson',
        'age': 28,
        'diagnosis': 'Generalized Anxiety',
        'therapist': 'Dr. Sarah Martinez',
        'emergency_contact': 'Mom - (555) 123-4567',
        'joined_date': datetime(2024, 1, 10)
    }

if 'moods' not in st.session_state:
    # More realistic mood data over time
    base_date = datetime.now() - timedelta(days=30)
    st.session_state.moods = []
    for i in range(30):
        date = base_date + timedelta(days=i)
        # Simulate realistic mood patterns with some variation
        base_mood = 3  # baseline okay
        variation = (i % 7)  # weekly pattern
        if variation in [0, 6]:  # weekends might be better
            base_mood += 0.5
        elif variation in [1, 2]:  # Monday/Tuesday might be harder
            base_mood -= 0.5

        mood_value = max(1, min(5, base_mood + (0.5 - pd.Series([0]).sample(1).iloc[0])))
        mood_labels = {1: 'Very Low', 2: 'Low', 3: 'Okay', 4: 'Good', 5: 'Great'}
        mood_emojis = {1: '😢', 2: '😔', 3: '😐', 4: '🙂', 5: '😊'}

        st.session_state.moods.append({
            'id': str(uuid.uuid4()),
            'date': date.strftime('%Y-%m-%d'),
            'datetime': date,
            'value': round(mood_value),
            'label': mood_labels[round(mood_value)],
            'emoji': mood_emojis[round(mood_value)],
            'notes': f"Daily mood tracking - {mood_labels[round(mood_value)].lower()} day"
        })

if 'goals' not in st.session_state:
    st.session_state.goals = [
        {'id': str(uuid.uuid4()), 'text': 'Practice deep breathing for 5 minutes daily', 'completed': True, 'created': datetime(2024, 1, 15), 'category': 'Mindfulness'},
        {'id': str(uuid.uuid4()), 'text': 'Take a 20-minute walk outside', 'completed': True, 'created': datetime(2024, 1, 16), 'category': 'Exercise'},
        {'id': str(uuid.uuid4()), 'text': 'Write in journal about positive experiences', 'completed': False, 'created': datetime(2024, 1, 17), 'category': 'Journaling'},
        {'id': str(uuid.uuid4()), 'text': 'Call a friend or family member', 'completed': False, 'created': datetime(2024, 1, 18), 'category': 'Social'},
        {'id': str(uuid.uuid4()), 'text': 'Try a new healthy recipe', 'completed': False, 'created': datetime(2024, 1, 19), 'category': 'Nutrition'},
        {'id': str(uuid.uuid4()), 'text': 'Attend weekly therapy session', 'completed': False, 'created': datetime(2024, 1, 20), 'category': 'Therapy'},
    ]

if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = [
        {
            'id': str(uuid.uuid4()),
            'content': 'Today was challenging. Work was stressful and I felt overwhelmed. Took some deep breaths and went for a short walk. Feeling a bit better now.',
            'timestamp': datetime.now() - timedelta(days=2),
            'mood': 2,
            'tags': ['stress', 'work', 'anxiety']
        },
        {
            'id': str(uuid.uuid4()),
            'content': 'Had a good therapy session today. We talked about coping strategies and I feel more equipped to handle difficult situations.',
            'timestamp': datetime.now() - timedelta(days=1),
            'mood': 4,
            'tags': ['therapy', 'progress', 'coping']
        }
    ]

if 'medications' not in st.session_state:
    st.session_state.medications = [
        {'id': str(uuid.uuid4()), 'name': 'Sertraline (Zoloft)', 'dosage': '50mg', 'time': '08:00 AM', 'taken_today': True, 'frequency': 'Daily', 'purpose': 'Anxiety/Depression'},
        {'id': str(uuid.uuid4()), 'name': 'Lorazepam (Ativan)', 'dosage': '0.5mg', 'time': 'As needed', 'taken_today': False, 'frequency': 'PRN', 'purpose': 'Acute Anxiety'},
        {'id': str(uuid.uuid4()), 'name': 'Vitamin D3', 'dosage': '2000 IU', 'time': '09:00 AM', 'taken_today': False, 'frequency': 'Daily', 'purpose': 'Supplement'},
    ]

if 'appointments' not in st.session_state:
    st.session_state.appointments = [
        {'id': str(uuid.uuid4()), 'title': 'Weekly Therapy Session', 'datetime': datetime.now() + timedelta(days=2), 'duration': 50, 'type': 'Therapy', 'location': 'Virtual', 'notes': 'Discuss coping strategies'},
        {'id': str(uuid.uuid4()), 'title': 'Psychiatrist Follow-up', 'datetime': datetime.now() + timedelta(days=7), 'duration': 30, 'type': 'Medication Review', 'location': 'Clinic', 'notes': 'Medication adjustment review'},
    ]

if 'symptoms' not in st.session_state:
    st.session_state.symptoms = [
        {'id': str(uuid.uuid4()), 'name': 'Anxiety', 'severity': 6, 'date': datetime.now().strftime('%Y-%m-%d'), 'notes': 'Worse in mornings'},
        {'id': str(uuid.uuid4()), 'name': 'Sleep Quality', 'severity': 4, 'date': datetime.now().strftime('%Y-%m-%d'), 'notes': 'Better than last week'},
        {'id': str(uuid.uuid4()), 'name': 'Concentration', 'severity': 5, 'date': datetime.now().strftime('%Y-%m-%d'), 'notes': 'Improving with medication'},
    ]

if 'community_posts' not in st.session_state:
    st.session_state.community_posts = [
        {
            'id': str(uuid.uuid4()),
            'author': 'Anonymous User',
            'content': 'Today was hard, but I made it through. Small victories matter. Remember to be kind to yourself.',
            'likes': 24,
            'timestamp': datetime.now() - timedelta(hours=2),
            'tags': ['motivation', 'self-care']
        },
        {
            'id': str(uuid.uuid4()),
            'author': 'Hope Seeker',
            'content': 'Started using the breathing exercises from the coping strategies. They really help when anxiety spikes!',
            'likes': 15,
            'timestamp': datetime.now() - timedelta(hours=5),
            'tags': ['coping', 'anxiety', 'breathing']
        },
        {
            'id': str(uuid.uuid4()),
            'author': 'Mindful One',
            'content': 'Grateful for this community. Therapy starts next week and I\'m nervous but hopeful.',
            'likes': 8,
            'timestamp': datetime.now() - timedelta(hours=8),
            'tags': ['therapy', 'gratitude', 'hope']
        }
    ]

if 'progress_metrics' not in st.session_state:
    st.session_state.progress_metrics = {
        'therapy_sessions': 8,
        'days_sober': 45,
        'medication_adherence': 92,
        'journal_entries': 23,
        'goals_completed': 12
    }

# Load custom CSS
def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
try:
    load_css()
except:
    pass

# Mood tracking functions
def add_mood(mood_value, mood_label, mood_emoji):
    st.session_state.moods.append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'datetime': datetime.now(),
        'value': mood_value,
        'label': mood_label,
        'emoji': mood_emoji
    })
    st.success(f"Mood logged: {mood_emoji} {mood_label}")
    st.rerun()

def get_mood_data():
    if not st.session_state.moods:
        return None
    df = pd.DataFrame(st.session_state.moods)
    return df

def plot_mood_trend():
    df = get_mood_data()
    if df is None or len(df) == 0:
        st.info("📊 No mood data yet. Start tracking to see your trends!")
        return
    
    # Group by date and get average
    daily_avg = df.groupby('date')['value'].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_avg['date'],
        y=daily_avg['value'],
        mode='lines+markers',
        name='Mood Trend',
        line=dict(color='#9333ea', width=3),
        marker=dict(size=10, color='#ec4899'),
        fill='tozeroy',
        fillcolor='rgba(147, 51, 234, 0.1)'
    ))
    
    fig.update_layout(
        title='Your Mood Trend Over Time',
        xaxis_title='Date',
        yaxis_title='Mood Score',
        yaxis=dict(range=[0, 6], tickvals=[1, 2, 3, 4, 5]),
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    avg_mood = df['value'].mean()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Mood", f"{avg_mood:.1f}/5")
    with col2:
        st.metric("Total Entries", len(df))
    with col3:
        if len(df) > 1:
            recent_avg = df.tail(3)['value'].mean()
            previous_avg = df.head(len(df)-3)['value'].mean() if len(df) > 3 else avg_mood
            delta = recent_avg - previous_avg
            st.metric("Recent Trend", f"{recent_avg:.1f}/5", f"{delta:+.1f}")

# Goal management functions
def add_goal(goal_text):
    st.session_state.goals.append({
        'id': len(st.session_state.goals),
        'text': goal_text,
        'completed': False,
        'created': datetime.now()
    })
    st.success("✅ Goal added!")
    st.rerun()

def toggle_goal(goal_id):
    for goal in st.session_state.goals:
        if goal['id'] == goal_id:
            goal['completed'] = not goal['completed']
    st.rerun()

def delete_goal(goal_id):
    st.session_state.goals = [g for g in st.session_state.goals if g['id'] != goal_id]
    st.rerun()

# Journal functions
def add_journal_entry(content):
    st.session_state.journal_entries.insert(0, {
        'content': content,
        'timestamp': datetime.now()
    })
    st.success("📝 Journal entry saved!")
    st.rerun()

# Medication functions
def add_medication(name, time):
    st.session_state.medications.append({
        'id': len(st.session_state.medications),
        'name': name,
        'time': time,
        'taken_today': False
    })
    st.success("💊 Medication reminder added!")
    st.rerun()

def toggle_medication(med_id):
    for med in st.session_state.medications:
        if med['id'] == med_id:
            med['taken_today'] = not med['taken_today']
    st.rerun()

# Community functions
def add_post(content):
    st.session_state.community_posts.insert(0, {
        'author': 'You',
        'content': content,
        'likes': 0,
        'timestamp': datetime.now()
    })
    st.success("📮 Post shared with the community!")
    st.rerun()

def generate_chat_response(user_message):
    """Generate a supportive AI response based on user input"""
    user_lower = user_message.lower()

    # Crisis detection
    crisis_keywords = ['suicide', 'kill myself', 'end it all', 'not worth living', 'better off dead', 'harm myself']
    if any(keyword in user_lower for keyword in crisis_keywords):
        return "I'm really concerned about what you're saying. If you're having thoughts of harming yourself, please reach out immediately to the 988 Suicide & Crisis Lifeline (call or text 988) or go to your nearest emergency room. You are valuable and worthy of help. You're not alone in this."

    # Anxiety responses
    if any(word in user_lower for word in ['anxious', 'anxiety', 'worried', 'panic', 'nervous']):
        return "I hear that you're feeling anxious right now. Anxiety can be really overwhelming. Try this grounding technique: Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste. This can help bring you back to the present moment. Would you like to talk more about what's causing your anxiety?"

    # Depression responses
    if any(word in user_lower for word in ['depressed', 'sad', 'hopeless', 'empty', 'worthless']):
        return "I'm sorry you're feeling this way. Depression can make everything feel heavy and hopeless. Remember that these feelings are temporary, even when they don't feel like it. Small steps like going for a walk, eating something nourishing, or calling a friend can help. Have you been able to do any self-care activities today?"

    # Stress responses
    if any(word in user_lower for word in ['stressed', 'overwhelmed', 'pressure', 'burnout']):
        return "Stress can feel overwhelming when it builds up. It's important to recognize when you need a break. Try the 4-7-8 breathing technique: Inhale for 4 counts, hold for 7 counts, exhale for 8 counts. This can help activate your body's relaxation response. What seems to be causing the most stress right now?"

    # Sleep issues
    if any(word in user_lower for word in ['sleep', 'insomnia', 'tired', 'exhausted']):
        return "Sleep issues can really affect our mental health. Establishing a consistent bedtime routine can help. Try dimming lights an hour before bed, avoiding screens, and doing something relaxing like reading. If sleep problems persist, talking to a healthcare provider about sleep hygiene or other treatments might be helpful."

    # Positive responses
    if any(word in user_lower for word in ['good', 'better', 'happy', 'grateful', 'thankful']):
        return "I'm glad to hear you're feeling positive! It's important to notice and celebrate these moments. What helped you feel this way? Recognizing what works for you can help you incorporate more of it into your life."

    # General supportive responses
    supportive_responses = [
        "Thank you for sharing that with me. It takes courage to open up about how you're feeling. How long have you been feeling this way?",
        "I appreciate you trusting me with your thoughts. Everyone's mental health journey is unique. What coping strategies have worked for you in the past?",
        "It's completely valid to feel the way you do. Mental health challenges affect millions of people. You're not alone in this. What would be most helpful for you right now?",
        "Your feelings matter, and it's important to acknowledge them. Would you like to explore some coping strategies together, or would you prefer to talk more about what's on your mind?",
        "I'm here to listen without judgment. Sometimes just having someone to talk to can make a difference. What's one thing that's been particularly challenging lately?"
    ]

    return supportive_responses[len(user_message) % len(supportive_responses)]

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='background: linear-gradient(135deg, #9333ea 0%, #ec4899 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-size: 2.5em; margin: 0;'>💜 MindCare</h1>
            <p style='color: white; font-size: 0.9em; margin-top: 5px;'>Your Mental Wellness Companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🏠 Home", "😊 Mood Tracking", "🌟 Coping Strategies", "🎯 Goals",
         "👥 Community", "📞 Professional Support", "💬 Chat Support", "💊 Medications",
         "📔 Journal", "📚 Education", "👤 Profile"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
        <div style='background: linear-gradient(135deg, #fee2e2 0%, #fce7f3 100%); 
                    padding: 15px; border-radius: 10px; text-align: center;'>
            <p style='margin: 0; font-size: 0.8em; color: #991b1b;'><strong>🆘 Crisis Support</strong></p>
            <p style='margin: 5px 0; font-size: 1.5em; color: #dc2626;'><strong>988</strong></p>
            <p style='margin: 0; font-size: 0.7em; color: #991b1b;'>Available 24/7</p>
        </div>
    """, unsafe_allow_html=True)

# Main content area
if page == "📊 Dashboard":
    st.title("📊 Mental Health Dashboard")

    # Overview metrics
    st.markdown("### 📈 Your Progress Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_mood = sum(m['value'] for m in st.session_state.moods[-7:]) / len(st.session_state.moods[-7:])
        st.metric("7-Day Avg Mood", f"{avg_mood:.1f}/5", "+0.3")
    with col2:
        completed_goals = len([g for g in st.session_state.goals if g['completed']])
        st.metric("Goals Completed", f"{completed_goals}/{len(st.session_state.goals)}", f"{completed_goals} total")
    with col3:
        adherence = st.session_state.progress_metrics['medication_adherence']
        st.metric("Med Adherence", f"{adherence}%", "Excellent")
    with col4:
        st.metric("Journal Streak", "5 days", "↗️ 2 days")

    # Mood trend chart
    st.markdown("### 📊 Mood Trends (Last 30 Days)")
    plot_mood_trend()

    # Upcoming appointments
    st.markdown("### 📅 Upcoming Appointments")
    upcoming = [a for a in st.session_state.appointments if a['datetime'] > datetime.now()]
    upcoming.sort(key=lambda x: x['datetime'])

    if upcoming:
        for appt in upcoming[:3]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{appt['title']}**")
                st.caption(f"{appt['datetime'].strftime('%B %d, %Y at %I:%M %p')} • {appt['location']} • {appt['duration']} min")
            with col2:
                days_until = (appt['datetime'] - datetime.now()).days
                if days_until == 0:
                    st.success("Today")
                elif days_until == 1:
                    st.info("Tomorrow")
                else:
                    st.info(f"In {days_until} days")
    else:
        st.info("No upcoming appointments scheduled.")

    # Symptom tracking
    st.markdown("### 📋 Current Symptoms")
    for symptom in st.session_state.symptoms:
        col1, col2, col3 = st.columns([2, 1, 3])
        with col1:
            st.write(f"**{symptom['name']}**")
        with col2:
            severity = symptom['severity']
            color = "🟢" if severity <= 3 else "🟡" if severity <= 6 else "🔴"
            st.write(f"{color} {severity}/10")
        with col3:
            st.caption(symptom['notes'])

elif page == "👤 Profile":
    st.title("👤 My Profile")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 👤 Personal Information")
        profile = st.session_state.user_profile

        st.markdown(f"**Name:** {profile['name']}")
        st.markdown(f"**Age:** {profile['age']}")
        st.markdown(f"**Diagnosis:** {profile['diagnosis']}")
        st.markdown(f"**Therapist:** {profile['therapist']}")
        st.markdown(f"**Emergency Contact:** {profile['emergency_contact']}")
        st.markdown(f"**Member Since:** {profile['joined_date'].strftime('%B %Y')}")

    with col2:
        st.markdown("### 🏆 Achievements & Milestones")

        achievements = [
            ("🎯 Goal Setter", f"Completed {st.session_state.progress_metrics['goals_completed']} wellness goals"),
            ("📝 Journal Keeper", f"{st.session_state.progress_metrics['journal_entries']} journal entries written"),
            ("💊 Medication Hero", f"{st.session_state.progress_metrics['medication_adherence']}% adherence rate"),
            ("🧘 Therapy Attendee", f"{st.session_state.progress_metrics['therapy_sessions']} sessions completed"),
            ("🌅 Recovery Journey", f"{st.session_state.progress_metrics['days_sober']} days of progress"),
        ]

        for icon, desc in achievements:
            st.markdown(f"{icon} {desc}")

    st.markdown("---")
    st.markdown("### 📊 Progress Metrics")

    metrics = st.session_state.progress_metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Therapy Sessions", metrics['therapy_sessions'])
        st.metric("Journal Entries", metrics['journal_entries'])

    with col2:
        st.metric("Goals Completed", metrics['goals_completed'])
        st.metric("Days of Progress", metrics['days_sober'])

    with col3:
        st.metric("Med Adherence", f"{metrics['medication_adherence']}%")
        st.metric("Current Streak", "7 days")

elif page == "🏠 Home":
    # Personalized welcome with dynamic content
    user_name = st.session_state.user_profile['name'].split()[0]
    current_hour = datetime.now().hour

    # Dynamic greeting based on time of day
    if current_hour < 12:
        greeting = "Good morning"
        emoji = "🌅"
    elif current_hour < 17:
        greeting = "Good afternoon"
        emoji = "☀️"
    else:
        greeting = "Good evening"
        emoji = "🌙"

    # Get recent activity
    recent_moods = [m for m in st.session_state.moods if (datetime.now() - m['datetime']).days <= 7]
    avg_recent_mood = sum(m['value'] for m in recent_moods) / len(recent_moods) if recent_moods else 3

    # Personalized message based on recent mood
    if avg_recent_mood >= 4:
        encouragement = "You're doing great! Keep up the positive momentum."
    elif avg_recent_mood >= 2.5:
        encouragement = "Remember that every day is a new opportunity for growth."
    else:
        encouragement = "Be gentle with yourself. Small steps lead to big changes."

    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #9333ea 0%, #ec4899 100%);
                    padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0; font-size: 2.5em;'>{emoji} {greeting}, {user_name}!</h1>
            <p style='color: rgba(255,255,255,0.9); margin-top: 10px; font-size: 1.1em;'>
                {encouragement}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        today_meds = [m for m in st.session_state.medications if m['frequency'] != 'PRN' and m['taken_today']]
        st.metric("Meds Today", f"{len(today_meds)}/{len([m for m in st.session_state.medications if m['frequency'] != 'PRN'])}")
    with col2:
        completed_goals = len([g for g in st.session_state.goals if g['completed']])
        st.metric("Goals Done", f"{completed_goals}/{len(st.session_state.goals)}")
    with col3:
        st.metric("Journal Streak", "5 days")
    with col4:
        upcoming_appts = len([a for a in st.session_state.appointments if a['datetime'] > datetime.now() and (a['datetime'] - datetime.now()).days <= 7])
        st.metric("Upcoming Appts", upcoming_appts)

    st.markdown("---")

    # Main content columns
    col1, col2 = st.columns([1, 1])

    with col1:
        # Mood Check-in
        st.markdown("### 💜 Daily Mood Check-in")

        # Show last 3 days mood trend
        recent_moods = sorted(st.session_state.moods, key=lambda x: x['datetime'], reverse=True)[:3]
        if recent_moods:
            st.markdown("**Recent Mood Trend:**")
            for mood in recent_moods:
                days_ago = (datetime.now() - mood['datetime']).days
                day_label = "Today" if days_ago == 0 else f"{days_ago} day{'s' if days_ago > 1 else ''} ago"
                st.caption(f"{day_label}: {mood['emoji']} {mood['label']}")

        st.markdown("**How are you feeling right now?**")
        mood_options = [
            (5, "Great", "😊"),
            (4, "Good", "🙂"),
            (3, "Okay", "😐"),
            (2, "Low", "😔"),
            (1, "Very Low", "😢")
        ]

        cols = st.columns(5)
        for idx, (value, label, emoji) in enumerate(mood_options):
            with cols[idx]:
                if st.button(f"{emoji}\n{label}", key=f"mood_home_{value}", use_container_width=True):
                    add_mood(value, label, emoji)

        # Symptom Quick Check
        st.markdown("### 📊 Symptom Check")
        symptoms_to_check = ["Anxiety", "Sleep Quality", "Energy Level"]
        for symptom in symptoms_to_check:
            severity = st.slider(f"{symptom}", 1, 10, 5, key=f"symptom_{symptom.lower().replace(' ', '_')}")
            if severity <= 3:
                st.success(f"✅ {symptom}: Good")
            elif severity <= 7:
                st.warning(f"⚠️ {symptom}: Moderate")
            else:
                st.error(f"🚨 {symptom}: High - Consider reaching out")

    with col2:
        # Today's Focus
        st.markdown("### 🎯 Today's Focus")

        # Upcoming appointments
        upcoming = [a for a in st.session_state.appointments if a['datetime'] > datetime.now()]
        upcoming.sort(key=lambda x: x['datetime'])

        if upcoming:
            next_appt = upcoming[0]
            days_until = (next_appt['datetime'] - datetime.now()).days
            if days_until == 0:
                st.success(f"📅 **Today**: {next_appt['title']} at {next_appt['datetime'].strftime('%I:%M %p')}")
            elif days_until == 1:
                st.info(f"📅 **Tomorrow**: {next_appt['title']} at {next_appt['datetime'].strftime('%I:%M %p')}")
            else:
                st.info(f"📅 **In {days_until} days**: {next_appt['title']}")

        # Active goals
        st.markdown("### 📋 Active Goals")
        incomplete_goals = [g for g in st.session_state.goals if not g['completed']]
        if incomplete_goals:
            for goal in incomplete_goals[:4]:  # Show up to 4 goals
                col_check, col_text = st.columns([0.15, 0.85])
                with col_check:
                    if st.checkbox("", key=f"home_goal_{goal['id']}", value=goal['completed'], label_visibility="hidden"):
                        toggle_goal(goal['id'])
                with col_text:
                    category_emoji = {
                        'Mindfulness': '🧘',
                        'Exercise': '🏃',
                        'Journaling': '📝',
                        'Social': '👥',
                        'Nutrition': '🥗',
                        'Therapy': '💬'
                    }.get(goal.get('category', ''), '🎯')
                    st.write(f"{category_emoji} {goal['text']}")
        else:
            st.success("🎉 All goals completed! Add new ones to keep growing.")

        if st.button("➕ Manage All Goals", use_container_width=True):
            st.session_state.page = "🎯 Goals"
            st.rerun()

    st.markdown("---")

    # Quick Actions with enhanced functionality
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🌟 Coping Tools", use_container_width=True, key="quick_coping"):
            st.session_state.page = "🌟 Coping Strategies"
            st.rerun()
        st.caption("Access breathing exercises and mindfulness techniques")

    with col2:
        if st.button("📞 Get Support", use_container_width=True, key="quick_support"):
            st.session_state.page = "📞 Professional Support"
            st.rerun()
        st.caption("Find therapists and crisis resources")

    with col3:
        if st.button("📔 Write Journal", use_container_width=True, key="quick_journal"):
            st.session_state.page = "📔 Journal"
            st.rerun()
        st.caption("Document your thoughts and feelings")

    with col4:
        if st.button("👥 Community", use_container_width=True, key="quick_community"):
            st.session_state.page = "👥 Community"
            st.rerun()
        st.caption("Connect with others on similar journeys")

    # Personalized tip based on user activity
    st.markdown("---")

    # Determine tip based on user patterns
    last_journal_days = (datetime.now() - st.session_state.journal_entries[0]['timestamp']).days if st.session_state.journal_entries else 999
    meds_taken_today = len([m for m in st.session_state.medications if m['taken_today']])

    if last_journal_days > 3:
        tip = "💡 **Tip**: Journaling can help process emotions. Try writing for just 5 minutes today."
    elif meds_taken_today == 0 and st.session_state.medications:
        tip = "💊 **Reminder**: Don't forget to take your medications if you haven't already."
    elif not incomplete_goals:
        tip = "🎯 **Great job!** Consider setting a new goal to maintain your progress."
    else:
        tip = "🌟 **Remember**: Progress isn't linear. Every small step counts toward your wellness journey."

    st.info(tip)

elif page == "😊 Mood Tracking":
    st.title("😊 Mood Tracking")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Log Your Mood")
        mood_options = [
            (5, "Great", "😊"),
            (4, "Good", "🙂"),
            (3, "Okay", "😐"),
            (2, "Low", "😔"),
            (1, "Very Low", "😢")
        ]
        
        for value, label, emoji in mood_options:
            if st.button(f"{emoji} {label}", key=f"mood_log_{value}", use_container_width=True):
                add_mood(value, label, emoji)
    
    with col2:
        st.markdown("### Mood Trends")
        plot_mood_trend()
    
    st.markdown("---")
    st.markdown("### Recent Mood History")
    
    if st.session_state.moods:
        recent_moods = sorted(st.session_state.moods, key=lambda x: x['datetime'], reverse=True)[:10]
        
        for mood in recent_moods:
            col1, col2, col3 = st.columns([0.5, 2, 1])
            with col1:
                st.markdown(f"<h1 style='margin: 0;'>{mood['emoji']}</h1>", unsafe_allow_html=True)
            with col2:
                st.write(f"**{mood['label']}**")
                st.caption(mood['datetime'].strftime('%B %d, %Y at %I:%M %p'))
            with col3:
                # Progress bar
                progress = mood['value'] / 5
                st.progress(progress)
    else:
        st.info("No mood entries yet. Start tracking above!")

elif page == "🌟 Coping Strategies":
    st.title("🌟 Coping Strategies")
    st.markdown("Evidence-based techniques to help manage depression and improve well-being.")
    
    strategies = [
        {
            'title': 'Deep Breathing Exercise',
            'category': 'Relaxation',
            'description': '4-7-8 Technique: Breathe in for 4 counts, hold for 7, breathe out for 8.',
            'emoji': '🫁',
            'color': '#10b981'
        },
        {
            'title': 'Mindful Walking',
            'category': 'Mindfulness',
            'description': 'Take a 10-minute walk focusing on your senses and surroundings.',
            'emoji': '🚶',
            'color': '#3b82f6'
        },
        {
            'title': 'Gratitude Journaling',
            'category': 'Journaling',
            'description': 'Write down 3 things you\'re grateful for today, no matter how small.',
            'emoji': '🙏',
            'color': '#f59e0b'
        },
        {
            'title': 'Progressive Muscle Relaxation',
            'category': 'Relaxation',
            'description': 'Systematically tense and release each muscle group in your body.',
            'emoji': '💪',
            'color': '#8b5cf6'
        },
        {
            'title': '5-4-3-2-1 Grounding',
            'category': 'Mindfulness',
            'description': 'Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.',
            'emoji': '👁️',
            'color': '#ec4899'
        },
        {
            'title': 'Positive Affirmations',
            'category': 'Self-Talk',
            'description': 'Repeat: "I am worthy. I am strong. I will get through this."',
            'emoji': '💭',
            'color': '#06b6d4'
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, strategy in enumerate(strategies):
        with col1 if idx % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                    <div style='background: white; padding: 25px; border-radius: 15px; 
                                border-left: 5px solid {strategy['color']}; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                            <span style='font-size: 2em; margin-right: 15px;'>{strategy['emoji']}</span>
                            <div>
                                <h3 style='margin: 0; color: #1f2937;'>{strategy['title']}</h3>
                                <span style='background: {strategy['color']}20; color: {strategy['color']}; 
                                             padding: 3px 10px; border-radius: 12px; font-size: 0.75em; font-weight: 600;'>
                                    {strategy['category']}
                                </span>
                            </div>
                        </div>
                        <p style='color: #4b5563; margin: 15px 0;'>{strategy['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start {strategy['title']}", key=f"start_{idx}", use_container_width=True):
                    st.success(f"✨ Great! Take a moment to practice {strategy['title']}")
                
                st.markdown("<br>", unsafe_allow_html=True)

elif page == "🎯 Goals":
    st.title("🎯 Wellness Goals")
    st.markdown("Set and track your personal wellness goals.")

    # Simple goal creation
    st.markdown("### ➕ Add New Goal")
    with st.form("simple_goal_form", clear_on_submit=True):
        goal_text = st.text_input(
            "What would you like to achieve?",
            placeholder="e.g., Practice deep breathing for 5 minutes daily",
            help="Be specific about what you want to accomplish"
        )
        submitted = st.form_submit_button("🚀 Add Goal", use_container_width=True, type="primary")

        if submitted and goal_text.strip():
            new_goal = {
                'id': str(uuid.uuid4()),
                'text': goal_text.strip(),
                'completed': False,
                'created': datetime.now()
            }
            st.session_state.goals.append(new_goal)
            st.success(f"✅ Goal added: {goal_text}")
            st.rerun()

    st.markdown("---")

    # Display goals in simple list
    st.markdown("### 📋 Your Goals")

    if st.session_state.goals:
        # Separate active and completed goals
        active_goals = [g for g in st.session_state.goals if not g['completed']]
        completed_goals = [g for g in st.session_state.goals if g['completed']]

        # Show active goals first
        if active_goals:
            st.markdown("#### 🎯 Active Goals")
            for goal in active_goals:
                with st.container():
                    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

                    with col1:
                        if st.checkbox("", key=f"complete_{goal['id']}", value=False, label_visibility="hidden"):
                            toggle_goal(goal['id'])

                    with col2:
                        st.write(f"**{goal['text']}**")
                        st.caption(f"Added {goal['created'].strftime('%B %d, %Y')}")

                    with col3:
                        if st.button("🗑️", key=f"delete_{goal['id']}", help="Delete this goal"):
                            delete_goal(goal['id'])

                st.markdown("---")

        # Show completed goals
        if completed_goals:
            st.markdown("#### ✅ Completed Goals")
            for goal in completed_goals:
                with st.container():
                    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

                    with col1:
                        if st.checkbox("", key=f"uncomplete_{goal['id']}", value=True, label_visibility="hidden"):
                            toggle_goal(goal['id'])

                    with col2:
                        st.write(f"~~{goal['text']}~~")
                        st.caption(f"Completed • Added {goal['created'].strftime('%B %d, %Y')}")

                    with col3:
                        if st.button("🗑️", key=f"delete_completed_{goal['id']}", help="Delete this goal"):
                            delete_goal(goal['id'])

                st.markdown("---")

        # Simple progress summary
        total_goals = len(st.session_state.goals)
        completed_count = len(completed_goals)
        active_count = len(active_goals)

        st.markdown("### 📊 Progress Summary")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Goals", total_goals)

        with col2:
            st.metric("Completed", completed_count)

        with col3:
            st.metric("Active", active_count)

    else:
        st.info("🎯 No goals yet! Add your first goal above to start your wellness journey.")

    # Simple motivational message
    st.markdown("---")
    st.markdown("### 💡 Remember")
    st.info("Small steps lead to big changes. Celebrate your progress and be kind to yourself along the way.")


elif page == "👥 Community":
    st.title("👥 Peer Support Community")
    st.markdown("Share your experiences, offer support, and connect with others on similar journeys.")
    
    with st.expander("📝 Share with the community", expanded=True):
        with st.form("post_form", clear_on_submit=True):
            post_content = st.text_area(
                "What's on your mind?",
                placeholder="Share your experience, offer support, or ask for advice...",
                height=100
            )
            submitted = st.form_submit_button("📮 Post", use_container_width=True)
            
            if submitted and post_content:
                add_post(post_content)
    
    st.markdown("---")
    st.markdown("### Community Posts")
    
    for idx, post in enumerate(st.session_state.community_posts):
        with st.container():
            col1, col2 = st.columns([0.5, 9.5])
            
            with col1:
                # Avatar
                st.markdown(f"""
                    <div style='width: 50px; height: 50px; border-radius: 50%; 
                                background: linear-gradient(135deg, #9333ea 0%, #ec4899 100%);
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-weight: bold; font-size: 1.5em;'>
                        {post['author'][0]}
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{post['author']}**")
                st.caption(post['timestamp'].strftime('%B %d, %Y at %I:%M %p'))
                st.write(post['content'])
                
                col_like, col_reply = st.columns([1, 9])
                with col_like:
                    st.button(f"❤️ {post['likes']}", key=f"like_{idx}")
                with col_reply:
                    st.button(f"💬 Reply", key=f"reply_{idx}")
        
        st.markdown("---")

elif page == "📞 Professional Support":
    st.title("📞 Professional Support & Resources")

    # Initialize provider search state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'selected_provider' not in st.session_state:
        st.session_state.selected_provider = None

    # Crisis Support Section
    st.markdown("### 🆘 Immediate Crisis Support")
    st.markdown("*If you're in crisis or having thoughts of self-harm, please reach out immediately. Help is available 24/7 and confidential.*")

    crisis_resources = [
        {
            'name': '988 Suicide & Crisis Lifeline',
            'contact': 'Call or Text: 988',
            'description': '24/7 free & confidential support for anyone in crisis',
            'icon': '📞',
            'color': '#dc2626',
            'availability': '24/7'
        },
        {
            'name': 'Crisis Text Line',
            'contact': 'Text HOME to 741741',
            'description': 'Free 24/7 crisis counseling via text message',
            'icon': '💬',
            'color': '#db2777',
            'availability': '24/7'
        },
        {
            'name': 'Emergency Services',
            'contact': 'Call 911',
            'description': 'For immediate danger or medical emergencies',
            'icon': '🚑',
            'color': '#ef4444',
            'availability': '24/7'
        },
        {
            'name': 'International Hotlines',
            'contact': 'befrienders.org',
            'description': 'Find crisis support in your country worldwide',
            'icon': '🌐',
            'color': '#2563eb',
            'availability': 'Varies by location'
        }
    ]

    for resource in crisis_resources:
        with st.container():
            col1, col2, col3 = st.columns([0.5, 2, 1])
            with col1:
                st.markdown(f"<h2 style='margin: 0; color: {resource['color']};'>{resource['icon']}</h2>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{resource['name']}**")
                st.markdown(f"*{resource['contact']}*")
                st.caption(resource['description'])
            with col3:
                st.markdown(f"**{resource['availability']}**")
                if st.button("Contact", key=f"contact_{resource['name'].replace(' ', '_')}", use_container_width=True):
                    st.success(f"Opening contact for {resource['name']}")

    st.markdown("---")

    # Therapist Finder
    st.markdown("### 🔍 Find a Therapist")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Search Criteria")

        # Search filters
        specialty = st.multiselect(
            "Specialties:",
            ["Anxiety", "Depression", "Trauma/PTSD", "Bipolar Disorder", "OCD", "Eating Disorders",
             "Substance Use", "Relationship Issues", "LGBTQ+ Issues", "Grief & Loss", "Stress Management"],
            key="specialty_filter"
        )

        therapy_types = st.multiselect(
            "Therapy Types:",
            ["Cognitive Behavioral (CBT)", "Dialectical Behavior (DBT)", "Psychodynamic", "Humanistic",
             "Family Systems", "EMDR", "Mindfulness-Based", "Solution-Focused", "Art Therapy", "Group Therapy"],
            key="therapy_filter"
        )

        insurance = st.multiselect(
            "Insurance Accepted:",
            ["Aetna", "Blue Cross Blue Shield", "Cigna", "UnitedHealthcare", "Medicare", "Medicaid",
             "Self-Pay", "Sliding Scale"],
            key="insurance_filter"
        )

        session_format = st.multiselect(
            "Session Format:",
            ["In-Person", "Video", "Phone", "Text/Chat"],
            default=["Video"],
            key="format_filter"
        )

        max_cost = st.slider("Maximum Cost per Session ($):", 50, 300, 150, key="cost_filter")

        location = st.text_input("Location (City, State):", placeholder="e.g., New York, NY", key="location_filter")

        if st.button("🔍 Search Therapists", use_container_width=True):
            # Simulate search results
            st.session_state.search_results = [
                {
                    'id': '1',
                    'name': 'Dr. Sarah Martinez, LCSW',
                    'specialties': ['Anxiety', 'Depression', 'Trauma/PTSD'],
                    'approaches': ['CBT', 'EMDR', 'Mindfulness-Based'],
                    'insurance': ['Aetna', 'Blue Cross Blue Shield', 'Self-Pay'],
                    'formats': ['Video', 'In-Person'],
                    'cost': '$120-150/session',
                    'rating': 4.8,
                    'reviews': 127,
                    'availability': 'Next available: Tomorrow',
                    'credentials': 'Licensed Clinical Social Worker, EMDR Certified',
                    'experience': '12 years',
                    'location': 'Virtual + Downtown Office'
                },
                {
                    'id': '2',
                    'name': 'Dr. Michael Chen, PhD',
                    'specialties': ['Anxiety', 'OCD', 'Bipolar Disorder'],
                    'approaches': ['CBT', 'DBT'],
                    'insurance': ['Cigna', 'UnitedHealthcare', 'Medicare'],
                    'formats': ['Video', 'Phone'],
                    'cost': '$140-180/session',
                    'rating': 4.9,
                    'reviews': 89,
                    'availability': 'Next available: Friday',
                    'credentials': 'Clinical Psychologist, Board Certified',
                    'experience': '15 years',
                    'location': 'Virtual Only'
                },
                {
                    'id': '3',
                    'name': 'Jennifer Lopez, LMFT',
                    'specialties': ['Relationship Issues', 'Depression', 'LGBTQ+ Issues'],
                    'approaches': ['Humanistic', 'Family Systems'],
                    'insurance': ['Blue Cross Blue Shield', 'Self-Pay', 'Sliding Scale'],
                    'formats': ['Video', 'In-Person'],
                    'cost': '$90-130/session',
                    'rating': 4.7,
                    'reviews': 203,
                    'availability': 'Next available: Next Monday',
                    'credentials': 'Licensed Marriage & Family Therapist',
                    'experience': '8 years',
                    'location': 'Virtual + Midtown Office'
                }
            ]
            st.rerun()

    with col2:
        st.markdown("#### Search Results")

        if st.session_state.search_results:
            for provider in st.session_state.search_results:
                with st.container():
                    # Provider header
                    col_name, col_rating = st.columns([3, 1])
                    with col_name:
                        st.markdown(f"**{provider['name']}**")
                        st.caption(f"⭐ {provider['rating']} ({provider['reviews']} reviews)")
                    with col_rating:
                        st.markdown(f"**{provider['availability']}**")

                    # Specialties and approaches
                    specialties_str = ", ".join(provider['specialties'][:3])
                    if len(provider['specialties']) > 3:
                        specialties_str += f" +{len(provider['specialties'])-3} more"
                    st.caption(f"🎯 {specialties_str}")

                    approaches_str = ", ".join(provider['approaches'][:2])
                    if len(provider['approaches']) > 2:
                        approaches_str += f" +{len(provider['approaches'])-2} more"
                    st.caption(f"🛠️ {approaches_str}")

                    # Cost and insurance
                    col_cost, col_format = st.columns([1, 1])
                    with col_cost:
                        st.caption(f"💰 {provider['cost']}")
                    with col_format:
                        formats_str = ", ".join(provider['formats'])
                        st.caption(f"📱 {formats_str}")

                    # Action buttons
                    col_view, col_book = st.columns([1, 1])
                    with col_view:
                        if st.button("View Profile", key=f"view_{provider['id']}", use_container_width=True):
                            st.session_state.selected_provider = provider
                            st.rerun()
                    with col_book:
                        if st.button("Book Consultation", key=f"book_{provider['id']}", use_container_width=True):
                            st.success(f"📅 Consultation request sent to {provider['name'].split(',')[0]}!")

                st.markdown("---")
        else:
            st.info("Use the filters on the left to search for therapists in your area.")

    # Selected Provider Details
    if st.session_state.selected_provider:
        provider = st.session_state.selected_provider
        st.markdown("---")
        st.markdown(f"### 👤 {provider['name']}")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**⭐ {provider['rating']}** ({provider['reviews']} reviews)")
            st.markdown(f"**📍 {provider['location']}**")
            st.markdown(f"**💼 {provider['credentials']}**")
            st.markdown(f"**⏰ {provider['experience']} experience**")

            st.markdown("**Specialties:**")
            for specialty in provider['specialties']:
                st.markdown(f"• {specialty}")

            st.markdown("**Therapy Approaches:**")
            for approach in provider['approaches']:
                st.markdown(f"• {approach}")

        with col2:
            st.markdown("**Accepted Insurance:**")
            for ins in provider['insurance']:
                st.markdown(f"• {ins}")

            st.markdown(f"**Session Formats:** {', '.join(provider['formats'])}")
            st.markdown(f"**Cost:** {provider['cost']}")

            if st.button("📞 Schedule Consultation", use_container_width=True):
                st.success("Consultation request sent! You'll receive a confirmation email shortly.")

            if st.button("❌ Close Profile", use_container_width=True):
                st.session_state.selected_provider = None
                st.rerun()

    st.markdown("---")

    # Additional Resources
    st.markdown("### 📚 Additional Resources")

    resources = [
        {
            'title': 'Psychology Today Therapist Directory',
            'description': 'Comprehensive database of licensed therapists with detailed profiles',
            'link': 'psychologytoday.com',
            'icon': '🔍',
            'color': '#3b82f6'
        },
        {
            'title': 'Open Path Collective',
            'description': 'Affordable therapy with licensed clinicians ($30-60/session)',
            'link': 'openpathcollective.org',
            'icon': '💰',
            'color': '#10b981'
        },
        {
            'title': 'Mental Health America',
            'description': 'Screening tools, treatment locator, and educational resources',
            'link': 'mhanational.org',
            'icon': '📖',
            'color': '#f59e0b'
        },
        {
            'title': 'NAMI HelpLine',
            'description': 'Free support for individuals and families affected by mental illness',
            'link': 'nami.org/help',
            'icon': '📞',
            'color': '#ec4899'
        }
    ]

    for resource in resources:
        with st.container():
            col_icon, col_content, col_link = st.columns([0.5, 3, 1])
            with col_icon:
                st.markdown(f"<h3 style='margin: 0; color: {resource['color']};'>{resource['icon']}</h3>", unsafe_allow_html=True)
            with col_content:
                st.markdown(f"**{resource['title']}**")
                st.caption(resource['description'])
            with col_link:
                if st.button("Visit", key=f"visit_{resource['title'].replace(' ', '_')}", use_container_width=True):
                    st.success(f"Opening {resource['link']}")

    # Insurance & Cost Information
    st.markdown("---")
    st.markdown("### 💳 Insurance & Cost Information")

    with st.expander("Understanding Therapy Costs & Insurance", expanded=False):
        st.markdown("""
        **Average Therapy Costs (2024):**
        - Individual therapy: $100-200 per session
        - Couples therapy: $150-250 per session
        - Group therapy: $50-80 per session

        **Insurance Coverage:**
        - Most major insurers cover mental health treatment
        - Deductibles and co-pays may apply
        - Some plans require referrals from primary care
        - Out-of-network providers may cost more

        **Financial Assistance Options:**
        - Sliding scale fees based on income
        - Low-cost clinics and community centers
        - Employee assistance programs (EAP)
        - State-funded mental health services
        """)

    # Tips for Finding the Right Therapist
    st.markdown("---")
    st.markdown("### 💡 Tips for Finding the Right Therapist")

    tips = [
        "🎯 **Specialization Matters**: Choose a therapist experienced with your specific concerns",
        "🤝 **Therapeutic Alliance**: Trust and comfort with your therapist is crucial for success",
        "💰 **Cost & Insurance**: Verify coverage and discuss fees upfront",
        "📅 **Availability**: Consider session times that fit your schedule",
        "🌟 **Credentials**: Look for licensed professionals (LCSW, PhD, MD, etc.)",
        "📍 **Format**: Decide between in-person, video, phone, or text therapy",
        "⏰ **Trial Period**: Many therapists offer a free consultation or first session",
        "📝 **Questions to Ask**: Inquire about their approach, experience, and success rates"
    ]

    for tip in tips:
        st.markdown(f"- {tip}")

    st.info("**Remember**: Finding the right therapist may take time. It's okay to try a few before finding the best fit for your needs.")

elif page == "💬 Chat Support":
    st.title("💬 Chat Support")
    st.markdown("Connect with our AI mental health assistant for immediate support, coping strategies, and guidance.")

    # Initialize chat history
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {
                'role': 'assistant',
                'content': "👋 Hi! I'm MindCare's AI support assistant. I'm here to listen, provide coping strategies, and offer guidance. How are you feeling today?",
                'timestamp': datetime.now()
            }
        ]

    # Chat interface
    st.markdown("### 💬 Your Conversation")

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_messages:
            if message['role'] == 'user':
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                                padding: 20px; border-radius: 25px; margin: 15px 0;
                                border-left: 6px solid #f59e0b; max-width: 85%; margin-left: auto; margin-right: 0;
                                box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
                                border: 2px solid #f59e0b;'>
                        <strong style='color: #92400e; font-size: 1.1em; font-weight: bold;'>You:</strong>
                        <div style='color: #92400e; font-size: 1em; margin-top: 8px; line-height: 1.4;'>{message['content']}</div>
                        <div style='color: #a16207; font-size: 0.8em; margin-top: 10px; text-align: right;'>{message['timestamp'].strftime('%I:%M %p')}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
                                padding: 20px; border-radius: 25px; margin: 15px 0;
                                border-left: 6px solid #3b82f6; max-width: 85%;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
                                border: 2px solid #3b82f6;'>
                        <strong style='color: #1e40af; font-size: 1.1em; font-weight: bold;'>🤖 MindCare Assistant:</strong>
                        <div style='color: #1e40af; font-size: 1em; margin-top: 8px; line-height: 1.4;'>{message['content']}</div>
                        <div style='color: #1e3a8a; font-size: 0.8em; margin-top: 10px;'>{message['timestamp'].strftime('%I:%M %p')}</div>
                    </div>
                """, unsafe_allow_html=True)

    # Message input
    st.markdown("---")
    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_area(
            "Type your message here...",
            placeholder="Share what's on your mind...",
            height=100,
            key="chat_input"
        )

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True)
        with col2:
            quick_help = st.form_submit_button("🚨 Crisis Help", use_container_width=True)
        with col3:
            clear_chat = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)

        if submitted and user_message.strip():
            # Add user message
            st.session_state.chat_messages.append({
                'role': 'user',
                'content': user_message.strip(),
                'timestamp': datetime.now()
            })

            # Generate AI response based on user input
            response = generate_chat_response(user_message.strip())
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            st.rerun()

        if quick_help:
            crisis_message = "I'm here to help. If you're in crisis, please call 988 (Suicide & Crisis Lifeline) or text HOME to 741741 (Crisis Text Line). You can also go to your nearest emergency room. You're not alone, and help is available 24/7."
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': crisis_message,
                'timestamp': datetime.now()
            })
            st.rerun()

        if clear_chat:
            st.session_state.chat_messages = [
                {
                    'role': 'assistant',
                    'content': "👋 Hi! I'm MindCare's AI support assistant. I'm here to listen, provide coping strategies, and offer guidance. How are you feeling today?",
                    'timestamp': datetime.now()
                }
            ]
            st.rerun()

    # Quick action buttons
    st.markdown("---")
    st.markdown("### 🛠️ Quick Support Options")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🌟 Coping Strategies", use_container_width=True):
            coping_response = "Here are some quick coping strategies:\n\n1. **Deep Breathing**: Inhale for 4 counts, hold for 4, exhale for 4\n2. **Grounding**: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste\n3. **Progressive Relaxation**: Tense and release each muscle group\n4. **Positive Affirmation**: 'I am safe. I am strong. This feeling will pass.'\n\nWhich one would you like to try?"
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': coping_response,
                'timestamp': datetime.now()
            })
            st.rerun()

    with col2:
        if st.button("😊 Mood Check", use_container_width=True):
            mood_response = "Let's check in on your mood. On a scale of 1-10 (1 being very low, 10 being great), how are you feeling right now? What emotions are you experiencing? Remember, all feelings are valid and it's okay to feel this way."
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': mood_response,
                'timestamp': datetime.now()
            })
            st.rerun()

    with col3:
        if st.button("🎯 Goal Support", use_container_width=True):
            goal_response = "Goals are an important part of mental wellness! What goal are you working on right now? Or would you like help breaking down a larger goal into smaller, manageable steps? Remember, progress is more important than perfection."
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': goal_response,
                'timestamp': datetime.now()
            })
            st.rerun()

    with col4:
        if st.button("📞 Professional Help", use_container_width=True):
            help_response = "If you're looking for professional support, here are some options:\n\n• **988 Suicide & Crisis Lifeline**: Call or text 988\n• **Crisis Text Line**: Text HOME to 741741\n• **Find a Therapist**: Use our Professional Support section\n• **Emergency Services**: Call 911 for immediate danger\n\nWould you like me to help you find specific resources?"
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': help_response,
                'timestamp': datetime.now()
            })
            st.rerun()

    # Chat guidelines
    st.markdown("---")
    with st.expander("💡 Chat Guidelines", expanded=False):
        st.markdown("""
        **What I can help with:**
        - Providing coping strategies and relaxation techniques
        - Offering emotional support and validation
        - Helping you identify and express your feelings
        - Suggesting self-care activities
        - Guiding you toward professional resources

        **Important notes:**
        - I'm an AI assistant, not a licensed therapist
        - I cannot provide medical advice or diagnosis
        - For crisis situations, please contact emergency services
        - All conversations are private and confidential
        - If you need professional help, please consult a licensed mental health provider
        """)

elif page == "💊 Medications":
    st.title("💊 Medication Management")

    # Today's medications summary
    today_meds = [m for m in st.session_state.medications if m['frequency'] != 'PRN']
    taken_today = len([m for m in today_meds if m['taken_today']])
    total_today = len(today_meds)

    if total_today > 0:
        st.metric("Today's Adherence", f"{taken_today}/{total_today}", f"{(taken_today/total_today*100):.0f}%")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ➕ Add Medication")
        with st.form("med_form", clear_on_submit=True):
            med_name = st.text_input("Medication Name", placeholder="e.g., Sertraline")
            med_dosage = st.text_input("Dosage", placeholder="e.g., 50mg")
            med_time = st.time_input("Time to Take")
            med_frequency = st.selectbox("Frequency", ["Daily", "Twice Daily", "As needed (PRN)", "Weekly"])
            med_purpose = st.text_input("Purpose", placeholder="e.g., Anxiety/Depression")

            submitted = st.form_submit_button("➕ Add Medication", use_container_width=True)

            if submitted and med_name:
                add_medication(med_name, med_time.strftime('%I:%M %p'))

    with col2:
        st.markdown("### 📋 Your Medications")

        if st.session_state.medications:
            for med in st.session_state.medications:
                with st.container():
                    col_icon, col_info, col_status = st.columns([0.5, 6, 2])

                    with col_icon:
                        st.markdown("<p style='font-size: 2em; margin: 0;'>💊</p>", unsafe_allow_html=True)

                    with col_info:
                        st.markdown(f"**{med['name']}** ({med.get('dosage', 'N/A')})")
                        st.caption(f"⏰ {med['time']} • {med.get('frequency', 'Daily')} • {med.get('purpose', 'N/A')}")

                    with col_status:
                        if med['taken_today']:
                            st.success("✅ Taken Today")
                        elif med['frequency'] == 'PRN':
                            st.info("💡 As needed")
                        else:
                            if st.button("Mark Taken", key=f"med_{med['id']}", use_container_width=True):
                                toggle_medication(med['id'])

                st.markdown("---")
        else:
            st.info("No medications added yet. Add your first medication above!")

    # Medication history/adherence chart
    st.markdown("### 📊 Adherence History (Last 7 Days)")
    # This would show a simple adherence chart in a real app
    st.info("Medication adherence tracking helps monitor treatment effectiveness. Consult your healthcare provider for any changes.")

elif page == "📔 Journal":
    st.title("📔 Private Journal")
    st.markdown("A safe, private space to document your thoughts and feelings.")
    
    with st.expander("✍️ Write New Entry", expanded=True):
        with st.form("journal_form", clear_on_submit=True):
            entry_content = st.text_area(
                "How are you feeling?",
                placeholder="Write your thoughts and feelings... This is a safe, private space.",
                height=200
            )
            submitted = st.form_submit_button("📝 Save Entry", use_container_width=True)
            
            if submitted and entry_content:
                add_journal_entry(entry_content)
    
    st.markdown("---")
    st.markdown("### Past Entries")
    
    if st.session_state.journal_entries:
        for entry in st.session_state.journal_entries:
            with st.container():
                st.caption(entry['timestamp'].strftime('%B %d, %Y at %I:%M %p'))
                st.markdown(f"""
                    <div style='background: #f9fafb; padding: 20px; border-radius: 12px; 
                                border-left: 4px solid #9333ea; margin-bottom: 20px;'>
                        <p style='color: #1f2937; white-space: pre-wrap; margin: 0;'>{entry['content']}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No journal entries yet. Start writing above!")

elif page == "📚 Education":
    st.title("📚 Educational Resources")
    st.markdown("Learn about depression, its causes, symptoms, and evidence-based treatments.")
    
    resources = [
        {
            'title': 'Understanding Depression',
            'type': 'Article',
            'duration': '5 min read',
            'description': 'Learn about the causes, symptoms, and types of depression.',
            'emoji': '📖',
            'color': '#3b82f6'
        },
        {
            'title': 'Cognitive Behavioral Therapy Basics',
            'type': 'Video',
            'duration': '12 min',
            'description': 'Introduction to CBT techniques for managing depression.',
            'emoji': '🎥',
            'color': '#ef4444'
        },
        {
            'title': 'The Science of Depression',
            'type': 'Article',
            'duration': '8 min read',
            'description': 'How depression affects the brain and body.',
            'emoji': '🧠',
            'color': '#8b5cf6'
        },
        {
            'title': 'Building Healthy Habits',
            'type': 'Video',
            'duration': '15 min',
            'description': 'Evidence-based strategies for daily wellness.',
            'emoji': '💪',
            'color': '#10b981'
        },
        {
            'title': 'Mindfulness for Depression',
            'type': 'Article',
            'duration': '6 min read',
            'description': 'How mindfulness practices can help manage symptoms.',
            'emoji': '🧘',
            'color': '#f59e0b'
        },
        {
            'title': 'Sleep and Mental Health',
            'type': 'Video',
            'duration': '10 min',
            'description': 'The connection between sleep quality and depression.',
            'emoji': '😴',
            'color': '#06b6d4'
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, resource in enumerate(resources):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
                <div style='background: white; padding: 25px; border-radius: 15px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                        <span style='background: {resource['color']}20; color: {resource['color']}; 
                                     padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 600;'>
                            {resource['type']}
                        </span>
                        <span style='color: #9ca3af; font-size: 0.85em;'>{resource['duration']}</span>
                    </div>
                    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                        <span style='font-size: 2.5em; margin-right: 15px;'>{resource['emoji']}</span>
                        <h3 style='margin: 0; color: #1f2937;'>{resource['title']}</h3>
                    </div>
                    <p style='color: #6b7280; margin-bottom: 15px;'>{resource['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"{'▶️ Watch' if resource['type'] == 'Video' else '📖 Read'} Now", 
                        key=f"resource_{idx}", use_container_width=True):
                st.success(f"Opening: {resource['title']}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; color: #6b7280;'>
        <p style='margin: 0 0 10px 0;'><strong>Remember:</strong> You are not alone. Recovery is possible. Help is available.</p>
        <p style='margin: 0; font-size: 0.9em;'>MindCare - Your journey to wellness © 2024 | Crisis Support: 988</p>
    </div>
""", unsafe_allow_html=True)
