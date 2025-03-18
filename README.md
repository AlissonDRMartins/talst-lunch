# TALST Lunch

A Streamlit application for managing and scheduling employee time slots with Supabase backend integration.

![TALST Logo](https://static.wixstatic.com/media/5ef07f_6416d9829dc4405385d15d6ca52bd186~mv2.png/v1/fill/w_108,h_35,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/5ef07f_6416d9829dc4405385d15d6ca52bd186~mv2.png)

## 📋 Overview

This application provides an intuitive interface for scheduling employees into predefined time slots. It features:

- Real-time availability checking
- User-friendly appointment scheduling
- Automatic slot management
- Capacity limits for each time slot
- Visual confirmation of bookings

## 🚀 Features

- **Two-Shift Scheduling**: Organize appointments across two distinct shifts
- **Capacity Management**: Automatically limits each time slot to a maximum of 10 people
- **Visual Feedback**: Shows available slots and confirms selections
- **Real-time Database**: Integrates with Supabase for immediate updates
- **Responsive Design**: Works across different screen sizes
- **Brand-consistent UI**: Follows TALST's brand identity and color scheme

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend/Database**: Supabase
- **Data Processing**: Pandas
- **Styling**: Custom CSS integrated with Streamlit components

## 📊 Database Structure

The application uses a Supabase table named `employees` with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| name | string | Employee name |
| booked | boolean | Whether employee is booked |
| scheduled_time | time | Selected time slot |

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.7+
- pip
- Supabase account and project

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/talst-agendamento.git
   cd talst-agendamento
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.streamlit/secrets.toml` file with your Supabase credentials:
   ```toml
   SUPABASE_URL = "your-supabase-url"
   SUPABASE_KEY = "your-supabase-key"
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🕒 Available Time Slots

### First Shift
- 11:50
- 12:10
- 12:30

### Second Shift
- 13:02
- 13:22
- 13:42

## 🖥️ Usage Guide

1. **Select an Employee**: Choose from the available unbooked employees in the sidebar
2. **Choose a Time Slot**: Click on an available time slot button
3. **Confirm Booking**: After selecting a time slot, click the "Confirmar Agendamento" button
4. **Review Bookings**: View the table of employees booked for the selected time slot

## 🔒 Security Considerations

- Supabase API keys are stored in Streamlit's secure secrets management
- No sensitive employee data is displayed publicly
- Basic validation prevents overbooking of time slots

## 🎨 Customization

The application uses TALST's brand colors:
- White: `#ffffff`
- Light Gray: `#b0b0b0`
- Brand Green: `#8eb6a7`
- Dark Green: `#637970`
- Black: `#111111`

To modify the appearance, edit the CSS section at the top of the application.

## 📝 Requirements

- streamlit
- supabase
- pandas

## 🤝 Contributing

If you'd like to contribute to this project, please:
1. Fork the repository
2. Create a new branch for your feature
3. Add your changes
4. Submit a pull request

## 📄 License

This project is proprietary and belongs to TALST. All rights reserved.

## 📞 Contact

For more information, visit [www.talst.com.br](https://www.talst.com.br)