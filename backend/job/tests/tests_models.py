from django.test import TestCase
from job.models import Case

# Проверить модель Case на длину названия - не более 50 символов


class CaseModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса.
        # Значение slug не указываем, ждём, что при создании объекта
        # оно создастся автоматически из title.
        # А title сделаем таким, чтобы после транслитерации
        # он стал более 100 символов
        # (буква "ж" транслитерируется в два символа: "zh")
        cls.case = Case.objects.create(
            title='Ж' * 50,
            description='Тестовый текст'
        )

    # def test_text_convert_to_slug(self):
    #     """Содержимое поля title преобразуется в slug."""
    #     case = CaseModelTest.case
    #     slug = case.slug
    #     self.assertEqual(slug, 'zh'*50)

    def test_title_max_length_not_exceed(self):
        # """
        # Длинный slug обрезается и не превышает max_length
        # поля slug в модели.
        #
        # """
        case = CaseModelTest.case
        max_length_title = case._meta.get_field('title').max_length
        length_title = len(case.title)
        self.assertEqual(max_length_title, length_title)
