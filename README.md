# Career Path Simulator AI

An AI-powered career simulator and resume builder that analyzes your current skills, suggests career transitions, generates a polished CV, and supports interview practice. It combines career guidance, AI-generated advice, and a downloadable resume workflow in one Flask app.

## Features

- 🎯 **Career Path Simulation** - Analyze potential career transitions based on your skills
- 🤖 **AI-Powered Advice** - Get personalized career guidance using GPT-4.1 Mini via Microsoft Foundry
- 📝 **Interview Coaching** - Generate interview questions and practice answering them in-app
- 🎙️ **Interview Feedback** - Receive interview-style coaching feedback and a simple answer-quality score
- 📄 **CV / Resume Builder** - Create a structured resume from your skills, role, experience, projects, and education details
- 👤 **Personal Resume Fields** - Include full name, phone, email, and date of birth in the generated CV
- 📥 **PDF Download** - Download the generated CV as a PDF for sharing or printing
- 📊 **Career Readiness Scoring** - Track your readiness level (Beginner → Expert Ready)
- ⏱️ **Timeline Estimation** - Get realistic success rates and transition timelines

## Tech Stack

- **Backend**: Flask (Python web framework)
- **AI**: GPT-4.1 Mini via Azure OpenAI / Microsoft Foundry
- **PDF Generation**: ReportLab
- **Frontend**: Flask templates (HTML/Jinja2) with custom CSS
- **Testing**: unittest regression tests for CV generation and fallback handling
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
   - Add your Azure OpenAI / Foundry credentials:
     - `AZURE_OPENAI_API_KEY=your_api_key_here`
     - `AZURE_OPENAI_ENDPOINT=your_endpoint_here`
   - If your environment uses Foundry-style keys, keep the same values in the variables expected by the app

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

3. **Build and Download Your CV**
   - Fill in your current role, skills, and experience details
   - Add personal information such as name, phone, email, and date of birth
   - Generate a polished resume and download it as a PDF

4. **Practice Interview**
   - Use the interview arena to read the current question and type your answer
   - Get quick coaching feedback on clarity, structure, and answer quality
   - Move through questions one by one and earn momentum for practice sessions

## Project Structure

```
career-path-simulator-ai/
├── app.py                    # Main Flask application and routes
├── ai_career_advisor.py      # AI career advice integration
├── ai_utils.py               # Utility helpers for AI workflows
├── career_engine.py          # Skill analysis and scoring engine
├── career_momentum.py        # Momentum / progress mechanics
├── career_simulator.py       # Career path simulation logic
├── cv_generator.py           # Resume / CV generation and fallback logic
├── cv_pdf.py                 # PDF resume generation
├── future_self_chat.py       # Future-self chat assistant
├── interview_coach.py        # Interview question generation and coaching
├── pdf_generator.py          # PDF report creation
├── skill_data.py             # Career skill database
├── test_ai.py                # Existing test suite
├── test_cv_generator.py      # CV generation regression tests
├── requirements.txt          # Python dependencies
├── static/                   # CSS and frontend assets
├── templates/                # Flask HTML templates
│   ├── cv_form.html         # Resume builder form
│   ├── cv.html              # Generated resume page
│   ├── interview_practice.html  # Interview practice page
│   ├── index.html           # Home page
│   └── result.html          # Results page
└── README.md                # This file
```

## Recent Updates

The latest version of the app includes:
- a fuller resume/CV generation path with richer fallback content
- a CV form that collects personal contact details for the PDF
- a more complete interview-practice experience with answer feedback
- improved question rendering and resume formatting for the generated PDF

## Configuration

### AI Model
This project uses **GPT-4.1 Mini** through **Azure OpenAI / Microsoft Foundry** for career advice and interview preparation, optimized for fast and accurate responses.

### AI Toggle
You can enable/disable AI features by modifying the `USE_AI` variable in `app.py`:
```python
USE_AI = True   # Enable AI features
USE_AI = False  # Disable for testing/development
```

### Azure OpenAI / Foundry Integration
The application integrates with Azure OpenAI / Foundry for AI capabilities. Ensure your credentials are properly configured in your `.env` file:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
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
3. **AI Advisory** - Uses GPT-4.1 Mini via Foundry/Azure OpenAI to provide personalized career transition advice
4. **Resume Building** - Uses your role, skills, and experience to generate a structured CV and PDF
5. **Interview Prep** - Generates relevant interview questions and supports practice with coaching feedback
6. **Momentum** - Tracks progress and rewards useful actions in the app

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
