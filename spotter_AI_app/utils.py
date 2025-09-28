# from system_admin.models.content_marker_model import ContentMarker
from system_admin.models.user_model import CustomUser


TABLE_MAPPING = {
    "CustomUser": CustomUser,
}


def color_print(text, color):
    """Print text in color"""

    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"

    print(f"{getattr(bcolors, color.upper())}{text}{bcolors.ENDC}")


# def process_content_marker(marker_id_list: list, user_id: int):
#     marker_objects_list = list(
#         ContentMarker.objects.filter(ContentMarkerID__in=marker_id_list).values()
#     )
#     Model = marker_objects_list[0]["ContentMarkerModel"]
#     Field = marker_objects_list[0]["ContentMarkerField"]
#     result = TABLE_MAPPING[Model].objects.filter(UserID=user_id).values(Field)

#     return result


def print_test_header(test_name):
    color_print(
        f"""\n
        ----------------------------------------------------------------------------
                              test: {test_name}
        ----------------------------------------------------------------------------
            """,
        "OKCYAN",
    )
    color_print("## =>  started", "WARNING")


def print_test_passed():
    color_print("## =>  passed", "OKGREEN")


def print_test_failed():
    color_print("## =>  failed", "FAIL")
