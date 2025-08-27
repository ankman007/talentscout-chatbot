from typing import Dict

class Response:
    """Generate chatbot response messages."""

    @staticmethod
    def summary_response(answers: Dict[str, str]) -> str:
        """Return a formatted summary of candidate information."""
        summary = (
            "Okay, here's a summary of the information gathered from the conversation between you and TalentScout, "
            "the AI hiring assistant:\n\n"
            "### Candidate Information:\n"
            f"- **Email:** {answers.get('email', 'N/A')}\n"
            f"- **Full Name:** {answers.get('full_name', 'N/A')}\n"
            f"- **Phone Number:** {answers.get('phone', 'N/A')} "
            "(Country code missing - needs clarification if not provided)\n"
            f"- **Years of Experience:** {answers.get('experience', 'N/A')} years\n"
            f"- **Previous Roles:** {answers.get('previous_role', 'N/A')}\n"
            f"- **Key Responsibilities:** {answers.get('key_responsibilities', 'N/A')}\n"
            f"- **Desired Position:** {answers.get('position', 'N/A')}\n"
            f"- **Preferred Location:** {answers.get('location', 'N/A')}\n"
            f"- **Tech Stack:** {answers.get('tech_stack', 'N/A')}\n"
        )
        return summary