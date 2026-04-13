
from enum import Enum

class defaultStatusEnum(str, Enum):
    ACTIVE = "Active"
    DEACTIVE = "Deactive"
    DELETED = "Deleted"

class inquiryStatus(str, Enum):
    COMPLETED = "completado"
    ONGOING = "processando"
    FAILED = "falha"


