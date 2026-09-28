from app.models import DigitalTwin


def create_digital_twin(
    name: str,
    goals: list[str],
    preferences: list[str],
    tasks: list
):
    return DigitalTwin(
        name=name,
        goals=goals,
        preferences=preferences,
        tasks=tasks
    )