import textwrap


class Lesson:
    def __init__(self):
        self.group = None
        self.name = None
        self.room = None
        self.teacher = None

    def __str__(self):
        return ', '.join([self.name, self.teacher, self.room])

    def get_splitted_string(self, limit):
        room = ""
        for letter in self.room:
            if letter != ' ':
                room += letter

        teacher = self.teacher
        teacher_words = teacher.split()
        teacher_flag = True
        if len(teacher_words) != 2:
            teacher_flag = False

        name = self.name
        if teacher_flag:
            t = ', '.join([name, teacher, room])
        else:
            t = name

        if teacher_flag:
            return textwrap.fill(text=t, width=limit)

        t_lines = textwrap.wrap(text=t, width=limit)

        last_line = t_lines[-1]

        t_last_line = last_line + ', ' + teacher
        t_wrap = textwrap.wrap(text=t_last_line, width=limit)
        if len(t_wrap) > 1:
            if len(textwrap.wrap(text=teacher + ',', width=limit)) == 1:
                t_lines[-1] += ','
                t_lines.append(teacher)

        else:
            t_lines.pop()
            t_lines += t_wrap

        last_line = t_lines[-1]
        t_last = last_line + ', ' + room
        if len(textwrap.wrap(text=t_last, width=limit)) == 1:
            t_lines[-1] = t_last
        else:
            t_lines[-1] += ',\n' + room

        string = '\n'.join(t_lines)

        return string
