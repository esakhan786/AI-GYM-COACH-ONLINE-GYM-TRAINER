import logging
from services.config.workout_config import PROMPT

logger = logging.getLogger(__name__)

FALLBACK_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

DEFAULT_FEEDBACKS = {
    "workout_started": "Workout started. Focus on controlled movement and proper form.",
    "set_completed": "Great set! Take a brief breather before your next set.",
    "workout_completed": "Fantastic job! Workout completed with great effort.",
    "workout_ended_early": "You ended your workout early today without finishing all planned sets. Good effort on what you did, but push through and complete the full workout next time!",
}


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt}
        ]

        if self.client:
            for model_name in FALLBACK_MODELS:
                try:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        temperature=0.4,
                    )
                    text = response.choices[0].message.content.strip()
                    self.history.append({"role": "assistant", "content": text})
                    return text
                except Exception as e:
                    error_str = str(e).lower()
                    if "not found" in error_str or "not_found" in error_str or "404" in error_str:
                        logger.warning(f"Groq model {model_name} not found, falling back: {e}")
                        continue
                    logger.error(f"Groq API error with model {model_name}: {e}")
                    break

        if issue:
            return f"Check your form: {issue}"
        return DEFAULT_FEEDBACKS.get(event, "Keep up the great form and stay focused!")

    