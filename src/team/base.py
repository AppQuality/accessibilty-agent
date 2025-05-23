from pydantic import BaseModel

# Shared output model
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str