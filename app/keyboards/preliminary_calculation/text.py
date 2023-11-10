from app.schemas.ButtonInfoSchema import ButtonInfo

preliminary_calculation_text_button_info = ButtonInfo(text="Отправить текстом", callback_data="text")
preliminary_calculation_pdf_button_info = ButtonInfo(text="Загрузить документ/фото", callback_data="pdf",)
