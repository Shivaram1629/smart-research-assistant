import streamlit as st
import os
from document_processor import DocumentProcessor
from ai_assistant import AIAssistant
from utils import clear_session_state, format_citation

# Page configuration
st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "document_content" not in st.session_state:
    st.session_state.document_content = ""
if "document_summary" not in st.session_state:
    st.session_state.document_summary = ""
if "document_name" not in st.session_state:
    st.session_state.document_name = ""
if "interaction_mode" not in st.session_state:
    st.session_state.interaction_mode = None
if "challenge_questions" not in st.session_state:
    st.session_state.challenge_questions = []
if "challenge_answers" not in st.session_state:
    st.session_state.challenge_answers = {}
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# Initialize processors
doc_processor = DocumentProcessor()
ai_assistant = AIAssistant()

# Main title
st.title("📚 Smart Research Assistant")
st.markdown("Upload a document and engage with AI-powered comprehension and reasoning")

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=['pdf', 'txt'],
        help="Upload a research paper, report, or any structured English document"
    )
    
    if uploaded_file is not None:
        # Process new document
        if uploaded_file.name != st.session_state.document_name:
            clear_session_state()
            st.session_state.document_name = uploaded_file.name
            
            with st.spinner("Processing document..."):
                try:
                    # Extract text from document
                    document_text = doc_processor.extract_text(uploaded_file)
                    st.session_state.document_content = document_text
                    
                    # Generate summary
                    summary = ai_assistant.generate_summary(document_text)
                    st.session_state.document_summary = summary
                    
                    st.success("Document processed successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
    
    # Document info
    if st.session_state.document_content:
        st.subheader("📋 Document Info")
        st.write(f"**File:** {st.session_state.document_name}")
        st.write(f"**Length:** {len(st.session_state.document_content):,} characters")
        
        if st.button("🗑️ Clear Document"):
            clear_session_state()
            st.rerun()

# Main content area
if not st.session_state.document_content:
    st.info("👈 Please upload a document to begin")
    st.markdown("""
    ### Features:
    - 📖 **Document Analysis**: Upload PDF or TXT files for intelligent processing
    - 🤔 **Ask Anything**: Get contextual answers based on document content
    - 🧠 **Challenge Me**: Test your comprehension with AI-generated questions
    - 📝 **Auto Summary**: Instant document summarization upon upload
    - 🔗 **Document Citations**: Every answer includes source references
    """)
else:
    # Display document summary
    if st.session_state.document_summary:
        st.subheader("📄 Document Summary")
        st.info(st.session_state.document_summary)
    
    # Mode selection
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤔 Ask Anything", use_container_width=True):
            st.session_state.interaction_mode = "ask_anything"
            st.rerun()
    
    with col2:
        if st.button("🧠 Challenge Me", use_container_width=True):
            st.session_state.interaction_mode = "challenge_me"
            if not st.session_state.challenge_questions:
                with st.spinner("Generating challenge questions..."):
                    try:
                        questions = ai_assistant.generate_challenge_questions(
                            st.session_state.document_content
                        )
                        st.session_state.challenge_questions = questions
                    except Exception as e:
                        st.error(f"Error generating questions: {str(e)}")
            st.rerun()
    
    # Display selected mode
    if st.session_state.interaction_mode == "ask_anything":
        st.divider()
        st.subheader("🤔 Ask Anything Mode")
        st.write("Ask any question about the document content. I'll provide answers based on the uploaded material.")
        
        # Q&A interface
        user_question = st.text_input(
            "Your question:",
            placeholder="What is the main argument of this document?",
            key="qa_input"
        )
        
        if st.button("Get Answer") and user_question:
            with st.spinner("Analyzing question and generating answer..."):
                try:
                    answer_data = ai_assistant.answer_question(
                        user_question, 
                        st.session_state.document_content,
                        st.session_state.qa_history
                    )
                    
                    # Add to history
                    st.session_state.qa_history.append({
                        "question": user_question,
                        "answer": answer_data["answer"],
                        "citation": answer_data["citation"]
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
        
        # Display Q&A history
        if st.session_state.qa_history:
            st.divider()
            st.subheader("💬 Conversation History")
            
            for i, qa in enumerate(reversed(st.session_state.qa_history)):
                with st.expander(f"Q{len(st.session_state.qa_history)-i}: {qa['question'][:100]}..."):
                    st.write("**Question:**")
                    st.write(qa['question'])
                    st.write("**Answer:**")
                    st.write(qa['answer'])
                    st.write("**Source Reference:**")
                    st.info(qa['citation'])
    
    elif st.session_state.interaction_mode == "challenge_me":
        st.divider()
        st.subheader("🧠 Challenge Me Mode")
        st.write("Test your understanding with these AI-generated questions based on the document.")
        
        if st.session_state.challenge_questions:
            for i, question_data in enumerate(st.session_state.challenge_questions):
                st.write(f"**Question {i+1}:**")
                st.write(question_data["question"])
                
                # User answer input
                user_answer = st.text_area(
                    f"Your answer to question {i+1}:",
                    key=f"answer_{i}",
                    height=100
                )
                
                if st.button(f"Submit Answer {i+1}", key=f"submit_{i}") and user_answer:
                    with st.spinner("Evaluating your answer..."):
                        try:
                            evaluation = ai_assistant.evaluate_answer(
                                question_data["question"],
                                user_answer,
                                question_data["expected_answer"],
                                st.session_state.document_content
                            )
                            
                            st.session_state.challenge_answers[i] = {
                                "user_answer": user_answer,
                                "evaluation": evaluation
                            }
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error evaluating answer: {str(e)}")
                
                # Display evaluation if available
                if i in st.session_state.challenge_answers:
                    eval_data = st.session_state.challenge_answers[i]["evaluation"]
                    
                    # Score display
                    score = eval_data["score"]
                    if score >= 80:
                        st.success(f"Score: {score}/100 - Excellent!")
                    elif score >= 60:
                        st.warning(f"Score: {score}/100 - Good")
                    else:
                        st.error(f"Score: {score}/100 - Needs improvement")
                    
                    # Detailed feedback
                    st.write("**Feedback:**")
                    st.write(eval_data["feedback"])
                    
                    st.write("**Expected Answer:**")
                    st.info(question_data["expected_answer"])
                    
                    st.write("**Document Reference:**")
                    st.info(eval_data["citation"])
                
                st.divider()
            
            # Reset challenge button
            if st.button("🔄 Generate New Questions"):
                st.session_state.challenge_questions = []
                st.session_state.challenge_answers = {}
                with st.spinner("Generating new challenge questions..."):
                    try:
                        questions = ai_assistant.generate_challenge_questions(
                            st.session_state.document_content
                        )
                        st.session_state.challenge_questions = questions
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating questions: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
Built with Streamlit and OpenAI GPT-4o | Designed for intelligent document comprehension
</div>
""", unsafe_allow_html=True)

