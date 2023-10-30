from pydantic import BaseModel


class ButtonInfo(BaseModel):
    text: str
    callback_data: str

    def filter(self, text: str) -> bool:
        return self.callback_data == text
