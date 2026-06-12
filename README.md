# Career Path Simulator AI

An AI-powered web application that analyzes your current skills and provides personalized career transition recommendations. It simulates career paths, generates tailored advice, and provides interview coaching for your target role.

## Features

- 🎯 **Career Path Simulation** - Analyze potential career transitions based on your skills
- 🤖 **AI-Powered Advice** - Get personalized career guidance using GPT-4.1 Mini via Microsoft Foundry
- 📝 **Interview Coaching** - Generate interview questions for your target role
- 📊 **Career Readiness Scoring** - Track your readiness level (Beginner → Expert Ready)
- 📄 **PDF Report Generation** - Download comprehensive career analysis reports
- ⏱️ **Timeline Estimation** - Get realistic success rates and transition timelines

## Tech Stack

- **Backend**: Flask (Python web framework)
- **AI**: GPT-4.1 Mini via Microsoft Foundry
- **PDF Generation**: ReportLab
- **Frontend**: Flask templates (HTML/Jinja2)
- **Package Manager**: pip

## Installation

### Prerequisites
- Python 3.x
- Microsoft Foundry access and API credentials
- GPT-4.1 Mini model access

### Steps
1. Clone the repository
   ```bash
   git clone https://github.com/deborahf1999/career-path-simulator-ai.git
   cd career-path-simulator-ai
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables
   - Create a `.env` file in the root directory
   - Add your Microsoft Foundry API key: `FOUNDRY_API_KEY=your_api_key_here`
   - Add your Foundry endpoint if required: `FOUNDRY_ENDPOINT=your_endpoint_here`

4. Run the application
   ```bash
   python app.py
   ```

5. Open your browser and visit
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter Your Information**
   - Provide your current job role
   - List your current skills (comma-separated)
   - Specify your target/desired role

2. **Get Instant Analysis**
   - Skill gap assessment
   - Career readiness level (Beginner, Emerging, Career Ready, Expert Ready)
   - Estimated success rate and timeline
   - AI-generated personalized career advice (powered by GPT-4.1 Mini)
   - Interview preparation questions for your target role

3. **Download Report**
   - Generate and download a comprehensive PDF career report
   - Save for future reference or sharing with mentors

## Project Structure

```
career-path-simulator-ai/
├── app.py                    # Main Flask application
├── career_simulator.py       # Career path simulation logic
├── career_engine.py          # Skill analysis and scoring engine
├── ai_career_advisor.py      # Microsoft Foundry integration for career advice
├── interview_coach.py        # Interview question generation
├── pdf_generator.py          # PDF report creation
├── skill_data.py             # Career skill database
├── test_ai.py                # Test suite
├── requirements.txt          # Python dependencies
├── static/                   # Static files (CSS, JS, images)
├── templates/                # HTML templates
│   ├── index.html           # Home page
│   └── result.html          # Results page
└── README.md                # This file
```

## Configuration

### AI Model
This project uses **GPT-4.1 Mini** model accessed through **Microsoft Foundry** for career advice generation, optimized for fast and accurate responses.

### AI Toggle
You can enable/disable AI features by modifying the `USE_AI` variable in `app.py`:
```python
USE_AI = True   # Enable AI features
USE_AI = False  # Disable for testing/development
```

### Microsoft Foundry Integration
The application integrates with Microsoft Foundry for AI capabilities. Ensure your Foundry credentials are properly configured in your `.env` file:
```
FOUNDRY_API_KEY=your_key_here
FOUNDRY_ENDPOINT=your_endpoint_here (if required)
```

## Dependencies

Key packages included in `requirements.txt`:
- Flask (3.1.3) - Web framework
- OpenAI (2.41.1) - AI API integration
- ReportLab (4.5.1) - PDF generation
- python-dotenv (1.2.2) - Environment variable management
- Pillow (12.2.0) - Image processing

See `requirements.txt` for complete list of dependencies.

## Getting Started - Quick Example

1. Go to http://localhost:5000
2. Fill in the form:
   - Current Role: "Junior Developer"
   - Skills: "Python, JavaScript, HTML/CSS"
   - Target Role: "Senior Full Stack Developer"
3. Click Analyze
4. Review your career readiness assessment and AI recommendations
5. Download your career report as PDF

## How It Works

1. **Skill Analysis** - The app analyzes your skills against industry requirements
2. **Scoring** - Generates a readiness score based on skill alignment
3. **AI Advisory** - Uses GPT-4.1 Mini via Microsoft Foundry to provide personalized career transition advice
4. **Interview Prep** - Generates relevant interview questions for your target role
5. **Timeline** - Estimates transition difficulty and success rate based on your skill gap

## Career Readiness Levels

- **Beginner** (0-40): Just starting - needs significant skill development
- **Emerging** (40-70): On the path - moderate skill gaps to address
- **Career Ready** (70-90): Nearly there - minor gaps remain
- **Expert Ready** (90-100): Fully prepared - can transition immediately

## AI Model Information

**Model Used**: GPT-4.1 Mini
- **Provider**: Microsoft Foundry
- **Capabilities**: Fast and efficient responses for career coaching
- **Cost-Efficiency**: Optimized for high-volume queries
- **Specialization**: Professional advice and career guidance

## Future Enhancements

- User authentication and profile management
- Database integration for skill tracking over time
- Advanced analytics and progress visualization
- Integration with job boards and opportunities
- Machine learning for personalized recommendations
- Mobile application support
- Integration with additional AI models

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

Built with ❤️ to help you advance your career
