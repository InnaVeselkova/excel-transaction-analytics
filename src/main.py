from src.views import get_main_info, get_personal_transfers
from views import get_report

if __name__ == "__main__":
    print(get_main_info("2018-03-20 12:11:12"))
    print(get_personal_transfers())
    print(get_report())
