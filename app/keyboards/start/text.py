from app.schemas.ButtonInfoSchema import ButtonInfo

insurance_live_button_info = ButtonInfo(text="Страхование жизни", callback_data="live_incurance")
insurance_property_button_info = ButtonInfo(text="Страхование имущества", callback_data="property_incurance")
insurance_live_and_property_button_info = ButtonInfo(text="Страхование жизни + имущества", callback_data="live_and_property")
executed_documents_button_info = ButtonInfo(text="Оформленные документы", callback_data="executed_documents")
download_dicuments_button_info = ButtonInfo(text="Отправить оформленные документы", callback_data="download_documents")

