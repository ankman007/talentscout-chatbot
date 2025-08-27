from typing import Dict

class Prompt:
    """Templates and prompts for AI interactions."""

    @staticmethod
    def generate_tech_questions(answers: Dict[str, str]) -> str:
        """Return a prompt for generating technical interview questions."""
        return (
            "You are an AI hiring assistant. Generate exactly 5 **technical interview questions** "
            "tailored for the following candidate based on their details:\n"
            f"{answers}\n\n"
            "Requirements:\n"
            "- Adapt the difficulty and focus of the questions to the candidate's years of experience:\n"
            "   * Junior (0–2 years): focus on practical skills, fundamentals, and direct coding scenarios.\n"
            "   * Mid-level (3–5 years): include problem-solving, debugging, API design, and applied use of their tech stack.\n"
            "   * Senior (6+ years): emphasize system design, architecture, scalability, trade-offs, leadership, and advanced best practices.\n"
            "- If the candidate's current or previous role is different from their desired role, include questions that test readiness for the new role.\n"
            "- Always use 'you' and 'your' in the questions.\n"
            "- Do NOT include explanations or reasoning in brackets or otherwise.\n"
            "- Output only a numbered list (1 to 5).\n"
            "- Keep the questions concise, clear, and professional."
        )

    @staticmethod
    def tech_question_guide() -> str:
        """Return a guidance message before technical questions."""
        return (
            "To help you prepare, we've curated 5 technical questions that align closely with your profile and experience.  \n"
            "These questions reflect what you’re most likely to encounter in interviews and will give you a head start in showcasing your skills effectively."
        )

    @staticmethod
    def tech_end_message() -> str:
        """Return a closing message after technical questions."""
        return (
            "Thank you for using our service. We’ll notify you via email if any opportunities matching your skill set become available.  \n"
            "To end this session, you may type ‘exit’, ‘quit’, or ‘close chat’."
        )
