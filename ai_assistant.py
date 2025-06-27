import json
import os
from openai import OpenAI
from typing import List, Dict, Any

class AIAssistant:
    """AI-powered assistant for document comprehension and reasoning."""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    def generate_summary(self, document_text: str) -> str:
        """
        Generate a concise summary of the document (≤150 words).
        
        Args:
            document_text: Full text content of the document
            
        Returns:
            str: Document summary
        """
        try:
            prompt = f"""
            Please provide a concise summary of the following document in no more than 150 words.
            Focus on the main themes, key arguments, and important findings.
            Make the summary informative and well-structured.
            
            Document content:
            {document_text[:8000]}  # Truncate for API limits
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert document analyst. Create clear, concise summaries that capture the essence of academic and professional documents."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def answer_question(self, question: str, document_text: str, conversation_history: List[Dict] = None) -> Dict[str, str]:
        """
        Answer a user question based on document content with proper citation.
        
        Args:
            question: User's question
            document_text: Full document content
            conversation_history: Previous Q&A for context
            
        Returns:
            dict: Answer and citation information
        """
        try:
            # Build context from conversation history
            context = ""
            if conversation_history:
                context = "Previous conversation:\n"
                for qa in conversation_history[-3:]:  # Last 3 Q&As for context
                    context += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
            
            prompt = f"""
            You are an expert document analyst. Answer the user's question based ONLY on the provided document content.
            
            Important guidelines:
            1. Base your answer strictly on the document content provided
            2. Do not add information from your general knowledge
            3. If the answer cannot be found in the document, clearly state this
            4. Provide specific references to support your answer
            5. Be thorough but concise
            
            {context}
            
            Document content:
            {document_text}
            
            User question: {question}
            
            Please respond in JSON format with the following structure:
            {{
                "answer": "Your detailed answer based on the document",
                "citation": "Specific reference to the document section/paragraph that supports this answer",
                "confidence": "high/medium/low based on how directly the document addresses the question"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise document analyst. Always ground your responses in the provided text and include specific citations."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"Failed to answer question: {str(e)}")
    
    def generate_challenge_questions(self, document_text: str) -> List[Dict[str, str]]:
        """
        Generate 3 logic-based comprehension questions from the document.
        
        Args:
            document_text: Full document content
            
        Returns:
            list: List of question dictionaries
        """
        try:
            prompt = f"""
            Based on the provided document, generate exactly 3 challenging questions that test deep comprehension and logical reasoning.
            
            Question requirements:
            1. Questions should require analysis, inference, or synthesis of information
            2. Avoid simple factual recall questions
            3. Focus on relationships, implications, and deeper understanding
            4. Each question should have a clear, document-based answer
            5. Questions should cover different aspects/sections of the document
            
            Document content:
            {document_text}
            
            Please respond in JSON format with the following structure:
            {{
                "questions": [
                    {{
                        "question": "The challenging question text",
                        "expected_answer": "Detailed expected answer based on the document",
                        "reasoning_required": "Brief description of the type of reasoning needed"
                    }}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator who creates challenging comprehension questions that test critical thinking and document understanding."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.4
            )
            
            result = json.loads(response.choices[0].message.content)
            return result["questions"]
            
        except Exception as e:
            raise Exception(f"Failed to generate challenge questions: {str(e)}")
    
    def evaluate_answer(self, question: str, user_answer: str, expected_answer: str, document_text: str) -> Dict[str, Any]:
        """
        Evaluate user's answer to a challenge question.
        
        Args:
            question: The original question
            user_answer: User's response
            expected_answer: Expected answer for comparison
            document_text: Document content for verification
            
        Returns:
            dict: Evaluation results with score and feedback
        """
        try:
            prompt = f"""
            Evaluate the user's answer to the question based on the document content.
            
            Question: {question}
            
            User's Answer: {user_answer}
            
            Expected Answer: {expected_answer}
            
            Document content (for reference):
            {document_text[:6000]}  # Truncate for API limits
            
            Evaluation criteria:
            1. Accuracy: How well does the answer align with document content?
            2. Completeness: Does it address all aspects of the question?
            3. Understanding: Does it demonstrate comprehension of key concepts?
            4. Evidence: Is the answer supported by document content?
            
            Please respond in JSON format:
            {{
                "score": 85,
                "feedback": "Detailed feedback explaining the evaluation",
                "strengths": "What the user did well",
                "areas_for_improvement": "What could be better",
                "citation": "Document reference that supports the correct answer"
            }}
            
            Score should be 0-100, where:
            - 90-100: Excellent, comprehensive understanding
            - 80-89: Good understanding with minor gaps
            - 70-79: Adequate understanding but missing key points
            - 60-69: Basic understanding but significant gaps
            - Below 60: Poor understanding or major inaccuracies
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert evaluator who provides fair, constructive feedback on comprehension answers based on document evidence."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"Failed to evaluate answer: {str(e)}")
    
    def extract_relevant_passages(self, question: str, document_text: str, num_passages: int = 3) -> List[str]:
        """
        Extract the most relevant passages from the document for a given question.
        
        Args:
            question: The question to find relevant content for
            document_text: Full document text
            num_passages: Number of passages to extract
            
        Returns:
            list: Most relevant text passages
        """
        try:
            # Split document into chunks (paragraphs or sections)
            chunks = [chunk.strip() for chunk in document_text.split('\n\n') if len(chunk.strip()) > 50]
            
            if len(chunks) <= num_passages:
                return chunks
            
            prompt = f"""
            Given the following question and document chunks, identify the {num_passages} most relevant chunks that would help answer the question.
            
            Question: {question}
            
            Document chunks:
            {json.dumps(chunks[:20], indent=2)}  # Limit for API
            
            Please respond in JSON format:
            {{
                "relevant_chunk_indices": [0, 5, 12]
            }}
            
            Return the indices of the most relevant chunks in order of relevance.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying relevant text passages for question answering."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            indices = result.get("relevant_chunk_indices", [])
            
            return [chunks[i] for i in indices if i < len(chunks)]
            
        except Exception:
            # Fallback: return first few chunks
            chunks = [chunk.strip() for chunk in document_text.split('\n\n') if len(chunk.strip()) > 50]
            return chunks[:num_passages]

