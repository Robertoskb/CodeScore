import os


def get_path_names(folder_path: str) -> list:
    try:
        return [name for name in os.listdir(folder_path)
                if os.path.isdir(f'{folder_path}/{name}')
                ]
    except FileNotFoundError:
        return []


def get_exams(exams_path: str = 'media/exams') -> list:
    return get_path_names(exams_path)


def get_questions(exam_name: str) -> list:
    return get_path_names(f'media/exams/{exam_name}')
