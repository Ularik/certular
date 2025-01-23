from datetime import date


def content_file_name(directory):
    # file will be uploaded to MEDIA_ROOT/customers/yearmonthday/<filename>
    today = date.today().strftime("%Y-%m-%d")
    return "{directory}/{date}".format(directory=directory, date=today)