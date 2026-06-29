from app.models import TaskStatus

VALID_TRANSITIONS = {
    TaskStatus.ToDo: [TaskStatus.InProgress],
    TaskStatus.InProgress: [TaskStatus.Done],
    TaskStatus.Done: [TaskStatus.InProgress],
}

def validate_status_transition(current, requested):
    if current == requested:
        return True
    return requested in VALID_TRANSITIONS.get(current, [])
