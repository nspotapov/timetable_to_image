import os
import datetime
from TimetableToImage import Timetable
from PIL import Image, ImageDraw, ImageFont


def get_multiline_text_size(text_string: str, font: ImageFont.FreeTypeFont) -> tuple:
    """
    Calculate size (width, height) of multiline text by text and font

    :param text_string:
    :param font:
    :return: Tuple of width and height
    """
    # https://stackoverflow.com/a/46220683/9263761
    strings = text_string.split('\n')
    text_width = 0
    ascent, descent = font.getmetrics()
    for line in strings:
        text_width = max(font.getmask(line).getbbox()[2], text_width)
    text_height = (ascent + descent) * len(strings)
    return text_width, text_height


def generate_from_timetable_week(
        timetable_week: Timetable.Week,
        timetable_bells: Timetable.Bells = None,
        inverted: bool = False,
        text_promotion: str = None,
        eng_lang: bool = False) -> Image:
    """
    Generate FULL-HD image of timetable

    :param timetable_week: Timetable.Week object
    :param timetable_bells: Timetable.Bells object
    :param inverted: set night theme of image
    :param text_promotion: promotion text on image
    :param eng_lang: set English language of headers and articles
    :return:
    """
    width = 1920
    height = 1080
    #
    have_bells = False
    if timetable_bells is not None:
        have_bells = True
    #
    font_size_article = 40
    font_size_header = 34
    font_size_table_large = 21
    font_size_table_small = 20
    fonts_folder = "Golos-UI"
    #
    table_row_letters_count_large = 18
    table_row_letters_count_small = 22
    #
    color_white = (255, 255, 255)
    color_black = (0, 0, 0)
    content_color = color_black
    background_color = color_white
    table_lines_width = 4
    if inverted:
        content_color = (202, 202, 232)
        background_color = (23, 33, 43)
        table_lines_width = 2
    #
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    #
    article_height_k = 2
    table_header_row_height_k = 1.4
    table_header_rows_count = 2
    table_rows_count = 6
    table_left_header_width = 120
    table_cols_count = 8
    x_left_text_article = 5
    y_top_table_header = font_size_article * article_height_k
    y_top_text_article = y_top_table_header / 5
    x_left_text_group_name = x_left_text_article + 400
    #
    font_regular_article = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_regular.ttf"), font_size_article)
    font_bold_article = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_bold.ttf"), font_size_article)
    #
    font_regular_header = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_regular.ttf"), font_size_header)
    font_medium_header = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_medium.ttf"), font_size_header)
    font_bold_header = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_bold.ttf"), font_size_header)
    #
    font_regular_table_large = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_regular.ttf"), font_size_table_large)
    #
    font_regular_table_small = ImageFont.truetype(
        os.path.join("../..", "fonts", fonts_folder, "font_regular.ttf"),
        font_size_table_small)
    #
    text_timetable_for_group = "Расписание группы: "
    if eng_lang:
        text_timetable_for_group = "Timetable for group: "
    # article "Timetable group: "
    draw.text((x_left_text_article, y_top_text_article), text_timetable_for_group,
              font=font_regular_article,
              fill=content_color)

    # article promotion
    if text_promotion is not None:
        text_width, _ = get_multiline_text_size(text_promotion, font_regular_article)
        draw.text(((width - text_width) / 2, y_top_text_article), text_promotion,
                  font=font_regular_article,
                  fill=content_color)

    # article group name
    draw.text((x_left_text_group_name, y_top_text_article), timetable_week.group,
              font=font_bold_article,
              fill=content_color)

    # article week number
    if timetable_week.number is not None:
        text_week = "Неделя:"
        if eng_lang:
            text_week = "Week:"
        draw.text((width - 215, y_top_text_article), text_week,
                  font=font_regular_article,
                  fill=content_color)
        draw.text((width - 55, y_top_text_article), str(timetable_week.number),
                  font=font_bold_article,
                  fill=content_color)

    # article week dates
    if timetable_week.begin is not None and timetable_week.end is not None:
        week_begin = timetable_week.begin.strftime("%d.%m")
        week_end = timetable_week.end.strftime("%d.%m")
        text_period = f"{week_begin} - {week_end}"
        draw.text((width - 500, y_top_text_article), text_period,
                  font=font_bold_article,
                  fill=content_color)

    # horizontal header
    for i in range(table_header_rows_count):
        draw.line((0, y_top_table_header + font_size_header * table_header_row_height_k * i, width,
                   y_top_table_header + font_size_header * table_header_row_height_k * i),
                  fill=content_color, width=table_lines_width)

    # horizontal table
    y_top_table = y_top_table_header + \
                  font_size_header * table_header_row_height_k * table_header_rows_count
    table_row_height = (height - y_top_table) / table_rows_count
    for i in range(table_rows_count):
        draw.line((0, y_top_table + table_row_height * i, width, y_top_table + table_row_height * i),
                  fill=content_color, width=table_lines_width)

    # vertical header + table
    x_left_table = table_left_header_width
    table_col_width = (width - table_left_header_width) / table_cols_count
    for i in range(table_cols_count):
        draw.line((x_left_table + table_col_width * i, y_top_table_header,
                   x_left_table + table_col_width * i, height), fill=content_color,
                  width=table_lines_width)

    # text pair
    text_pair = "Пара"
    if eng_lang:
        text_pair = "Pair"
    draw.text((15, y_top_table_header), text_pair, font=font_medium_header, fill=content_color)

    # text time
    text_time = "Время"
    if eng_lang:
        text_time = "Time"
    draw.text((6, y_top_table_header + font_size_header * table_header_row_height_k), text_time,
              font=font_medium_header, fill=content_color)

    # pair number and time
    x_center_first_pair_col = (x_left_table + (x_left_table + table_col_width)) / 2
    for i in range(table_cols_count):
        draw.text((x_center_first_pair_col - 10 + table_col_width * i, y_top_table_header),
                  str(i + 1),
                  font=font_medium_header, fill=content_color)
        if have_bells:
            bell = timetable_bells.bells[i]
            bell: Timetable.Bell
            text_time = f"{bell.begin.strftime('%H:%M')}-{bell.end.strftime('%H:%M')}"
            draw.text((x_left_table + 20 + table_col_width * i,
                       y_top_table_header + font_size_header * table_header_row_height_k),
                      text_time,
                      font=font_medium_header, fill=content_color)

    # pairs by days
    for i in range(table_rows_count):
        timetable_day = timetable_week.days[i]
        timetable_day: Timetable.Day
        y_shift_day_name = 50
        # if date set - write it
        if timetable_day.date is not None:
            y_shift_day_name = 40
            day_date = timetable_day.date
            day_date: datetime.date
            text_date = day_date.strftime("%d.%m")
            draw.text((15, y_top_table + 90 + table_row_height * i),
                      text_date,
                      font=font_regular_header, fill=content_color)
        # write day of week
        draw.text((35, y_top_table + y_shift_day_name + table_row_height * i),
                  Timetable.Week.DAYS_NAME[i],
                  font=font_bold_header, fill=content_color)
        # write timetable
        x_left_pair = x_left_table
        for j, timetable_pair in enumerate(timetable_day.pairs):
            timetable_pair: Timetable.Pair
            y_top_pair = y_top_table + table_row_height * i
            lesson_font = font_regular_table_large
            row_split = table_row_letters_count_large
            single_lesson = True
            if len(timetable_pair.lessons) > 1:
                single_lesson = False
                lesson_font = font_regular_table_small
                row_split = table_row_letters_count_small
            for v, lesson in enumerate(timetable_pair.lessons):
                lesson: Timetable.Lesson
                text_lesson = lesson.get_splitted_string(row_split)
                text_width, text_height = get_multiline_text_size(text_lesson, lesson_font)
                # try write text into cell
                target_height = table_row_height - table_lines_width
                if not single_lesson:
                    target_height = table_row_height / 2 - table_lines_width
                if text_height > target_height:
                    # if it doesn't fit, then change the font until it fits.
                    new_text_font = lesson_font
                    ind = 0
                    while text_height > target_height:
                        ind += 1
                        new_text_font = ImageFont.truetype(
                            os.path.join(os.getcwd(), "fonts", fonts_folder, "font_regular.ttf"),
                            new_text_font.size - 1)
                        text_lesson = lesson.get_splitted_string(row_split + ind)
                        text_width, text_height = get_multiline_text_size(text_lesson,
                                                                          new_text_font)
                        lesson_font = new_text_font

                x_shift = (table_col_width - text_width) / 2
                if single_lesson:
                    y_shift = (table_row_height - text_height) / 2
                else:
                    y_shift = (table_row_height / 2 - text_height) / 2
                    if v == 1:
                        y_shift = (table_row_height / 2 - text_height) / 2 + table_row_height / 2

                draw.multiline_text(
                    (
                        x_left_pair + x_shift + table_col_width * j,
                        y_top_pair + y_shift
                    ),
                    text_lesson,
                    font=lesson_font,
                    fill=content_color,
                    align="center"
                )
    #
    return image
