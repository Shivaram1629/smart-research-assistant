# Smart Research Assistant

An AI-powered research assistant that provides deep document comprehension, contextual Q&A, and logic-based question generation with document-grounded responses.

## Features

- **Document Upload**: Support for PDF and TXT files
- **Auto Summary**: Instant document summarization (≤150 words)
- **Ask Anything Mode**: Free-form question answering with document citations
- **Challenge Me Mode**: AI-generated comprehension questions with evaluation
- **Contextual Understanding**: All responses grounded in uploaded document content
- **Memory Handling**: Maintains context across follow-up questions

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd smart-research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

4. Run the application:
```bash
streamlit run app.py --server.port 5000
```

5. Open your browser and navigate to `http://localhost:5000`

## Architecture / Reasoning Flow

### System Architecture

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Document        │────│  AI Assistant   │
│   (app.py)      │    │  Processor       │    │  (OpenAI GPT-4o)│
│                 │    │  (PDF/TXT)       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │    Utilities     │
                    │  (Formatting &   │
                    │   Session Mgmt)  │
                    └──────────────────┘
```

### Data Flow

1. **Document Upload**: User uploads PDF/TXT file through Streamlit interface
2. **Text Extraction**: DocumentProcessor extracts and validates text content
3. **Summary Generation**: AIAssistant generates concise summary using GPT-4o
4. **Mode Selection**: User chooses interaction mode (Ask Anything / Challenge Me)
5. **AI Processing**: Questions processed through OpenAI API with document context
6. **Response Display**: Results displayed with proper citations and justifications

### Core Components

#### 1. Document Processor (`document_processor.py`)
- Handles PDF text extraction using pdfplumber
- Supports TXT files with multiple encoding detection
- Validates document content for processing suitability

#### 2. AI Assistant (`ai_assistant.py`)
- Manages OpenAI GPT-4o API interactions
- Implements contextual question answering
- Generates logic-based comprehension questions
- Evaluates user responses with detailed feedback
- Ensures all responses are grounded in document content

#### 3. Main Application (`app.py`)
- Streamlit web interface
- Session state management
- User interaction flow control
- Real-time processing feedback

#### 4. Utilities (`utils.py`)
- Helper functions for text formatting
- Citation formatting
- Session state management
- Error handling utilities

### Reasoning Flow

#### Ask Anything Mode:
1. User submits question
2. System retrieves relevant document passages
3. GPT-4o analyzes question against document content
4. Response generated with specific citations
5. Answer stored in conversation history for context

#### Challenge Me Mode:
1. System analyzes document content
2. GPT-4o generates 3 logic-based questions
3. User submits answers
4. System evaluates responses against expected answers
5. Detailed feedback provided with document references

## Usage

### Document Upload
1. Click "Choose a PDF or TXT file" in the sidebar
2. Select your document (supports research papers, reports, manuals)
3. Wait for processing and summary generation

### Ask Anything Mode
1. Click "Ask Anything" button
2. Type your question in the input field
3. Click "Get Answer" to receive a response with citations
4. View conversation history in expandable sections

### Challenge Me Mode
1. Click "Challenge Me" button
2. Read the AI-generated questions
3. Type your answers in the text areas
4. Submit each answer for evaluation and feedback
5. Click "Generate New Questions" for fresh challenges

## Technical Specifications

- **Frontend**: Streamlit web framework
- **AI Model**: OpenAI GPT-4o
- **Document Processing**: pdfplumber for PDF extraction
- **Deployment**: Replit with autoscale configuration
- **Response Format**: JSON structured responses for consistency
- **Session Management**: Streamlit session state

## Key Features Implementation

### Contextual Understanding
- All AI responses strictly grounded in document content
- No hallucination or external knowledge injection
- Explicit citations for every answer

### Memory Handling
- Maintains conversation history for follow-up questions
- Context-aware responses based on previous interactions
- Session persistence during document analysis

### Answer Evaluation
- Comprehensive scoring system (0-100)
- Detailed feedback with strengths and improvement areas
- Document-based justification for correct answers

## File Structure

```
smart-research-assistant/
├── app.py                 # Main Streamlit application
├── ai_assistant.py        # OpenAI integration and AI logic
├── document_processor.py  # PDF/TXT processing
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md            # This file
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Dependencies

- streamlit
- openai
- pdfplumber

## License

This project is created for educational and research purposes.
