from abc import ABC, abstractmethod
from datetime import date, datetime
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Union, Optional


class ValidationError(Exception):
    """Виняток для помилок валідації даних"""
    pass

class Student:
    """
    Клас, що представляє студента.
    
    Атрибути:
        _last_name (str): Прізвище студента
        _first_name (str): Ім'я студента
        _middle_name (str): По батькові студента
        _group_number (str): Номер групи
        _birth_date (date): Дата народження
        _address (str): Адреса проживання
    """
    
    def __init__(self, last_name: str, first_name: str, middle_name: str, group_number: str, 
                 birth_date: date, address: str = ""):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.group_number = group_number
        self.birth_date = birth_date
        self.address = address

    # Властивості для доступу до полів
    @property
    def last_name(self) -> str:
        return self._last_name
        
    @last_name.setter
    def last_name(self, value: str):
        if not value or not value.strip():
            raise ValidationError("Прізвище не може бути порожнім")
        self._last_name = value.strip()
    
    @property
    def first_name(self) -> str:
        return self._first_name
        
    @first_name.setter
    def first_name(self, value: str):
        if not value or not value.strip():
            raise ValidationError("Ім'я не може бути порожнім")
        self._first_name = value.strip()
    
    @property
    def middle_name(self) -> str:
        return self._middle_name
        
    @middle_name.setter
    def middle_name(self, value: str):
        if not value or not value.strip():
            raise ValidationError("По батькові не може бути порожнім")
        self._middle_name = value.strip()
    
    @property
    def full_name(self) -> str:
        """Повертає повне ім'я у форматі 'Прізвище Ім'я По батькові'"""
        return f"{self._last_name} {self._first_name} {self._middle_name}"
    
    @property
    def group_number(self) -> str:
        return self._group_number
    
    @group_number.setter
    def group_number(self, value: str):
        if not value or not value.strip():
            raise ValidationError("Номер групи не може бути порожнім")
        self._group_number = value.strip()
    
    @property
    def birth_date(self) -> date:
        return self._birth_date
    
    @birth_date.setter
    def birth_date(self, value: date):
        if not isinstance(value, date):
            raise ValidationError("Невірний формат дати. Очікується об'єкт date")
        if value > date.today():
            raise ValidationError("Дата народження не може бути у майбутньому")
        self._birth_date = value
    
    @property
    def age(self) -> int:
        """Повертає вік студента у роках"""
        today = date.today()
        age = today.year - self._birth_date.year
        if (today.month, today.day) < (self._birth_date.month, self._birth_date.day):
            age -= 1
        return age
    
    @property
    def address(self) -> str:
        return self._address
    
    @address.setter
    def address(self, value: str):
        self._address = value.strip() if value else ""


class AcademicPerformance(ABC):
    """
    Абстрактний клас для представлення успішності студента.
    
    Атрибути:
        _subjects (List[str]): Список предметів
        _grades (List[int]): Список оцінок за відповідні предмети
    """
    
    def __init__(self, subjects: List[str], grades: List[int]):
        self.subjects = subjects
        self.grades = grades
        self._validate_grades()
    
    def _validate_grades(self):
        """Валідація оцінок"""
        if not self._subjects or not self._grades:
            raise ValidationError("Списки предметів та оцінок не можуть бути порожніми")
            
        if len(self._subjects) != len(self._grades):
            raise ValidationError("Кількість предметів та оцінок має бути однаковою")
            
        for subject, grade in zip(self._subjects, self._grades):
            if not isinstance(grade, int) or not (0 <= grade <= 100):
                raise ValidationError(f"Оцінка повинна бути цілим числом від 0 до 100, отримано: {grade}")
            if not subject or not subject.strip():
                raise ValidationError("Назва предмету не може бути порожньою")
    
    @property
    def subjects(self) -> List[str]:
        return self._subjects
        
    @subjects.setter
    def subjects(self, value: List[str]):
        if not value or not all(isinstance(item, str) and item.strip() for item in value):
            raise ValidationError("Список предметів має містити непорожні рядки")
        self._subjects = [item.strip() for item in value]
    
    @property
    def grades(self) -> List[int]:
        return self._grades
        
    @grades.setter
    def grades(self, value: List[int]):
        if not value or not all(isinstance(item, int) for item in value):
            raise ValidationError("Список оцінок має містити цілі числа")
        self._grades = value
        self._validate_grades()
    
    @abstractmethod
    def average_grade(self) -> float:
        pass


class DesiredPerformance(AcademicPerformance):
    """
    Клас, що представляє бажану успішність студента.
    Наслідується від AcademicPerformance.
    """
    
    def __init__(self, subjects: List[str], desired_grades: List[int]):
        super().__init__(subjects, desired_grades)
    
    def average_grade(self) -> float:
        """
        Обчислює середній бал за бажаними оцінками.
        
        Повертає:
            float: Середній бал або 0.0, якщо оцінки відсутні
        """
        if not self._grades:
            return 0.0
        return round(sum(self._grades) / len(self._grades), 2)


class RealPerformance(AcademicPerformance):
    """
    Клас, що представляє реальну успішність студента.
    Наслідується від AcademicPerformance.
    """
    
    def __init__(self, subjects: List[str], actual_grades: List[int]):
        super().__init__(subjects, actual_grades)
    
    def average_grade(self) -> float:
        """
        Обчислює середній бал за реальними оцінками.
        
        Повертає:
            float: Середній бал або 0.0, якщо оцінки відсутні
        """
        if not self._grades:
            return 0.0
        return round(sum(self._grades) / len(self._grades), 2)
    
    def get_letter_grade(self) -> str:
        """
        Повертає буквений еквівалент середнього балу.
        
        Повертає:
            str: Буквений еквівалент оцінки
        """
        avg = self.average_grade()
        if avg >= 90: return 'A'
        elif avg >= 82: return 'B'
        elif avg >= 75: return 'C'
        elif avg >= 67: return 'D'
        elif avg >= 60: return 'E'
        else: return 'F'


class StudentData:
    """
    Клас для зберігання всіх даних про студента.
    
    Атрибути:
        _student (Student): Об'єкт студента
        _real_performance (RealPerformance): Реальна успішність
        _desired_performance (DesiredPerformance): Бажана успішність
    """
    
    def __init__(self, student: Student, real_performance: RealPerformance, 
                 desired_performance: DesiredPerformance):
        if not isinstance(student, Student):
            raise ValidationError("Параметр student має бути екземпляром класу Student")
        if not isinstance(real_performance, RealPerformance):
            raise ValidationError("Параметр real_performance має бути екземпляром класу RealPerformance")
        if not isinstance(desired_performance, DesiredPerformance):
            raise ValidationError("Параметр desired_performance має бути екземпляром класу DesiredPerformance")
            
        self._student = student
        self._real_performance = real_performance
        self._desired_performance = desired_performance
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Перетворює всі дані про студента у словник.
        
        Повертає:
            Dict[str, Any]: Словник з усіма даними про студента
        """
        try:
            return {
                "student": {
                    "full_name": self._student.full_name,
                    "last_name": self._student.last_name,
                    "first_name": self._student.first_name,
                    "middle_name": self._student.middle_name,
                    "group_number": self._student.group_number,
                    "birth_date": self._student.birth_date.isoformat(),
                    "age": self._student.age,
                    "address": self._student.address
                },
                "real_performance": {
                    "subjects": self._real_performance.subjects,
                    "grades": self._real_performance.grades,
                    "average_grade": self._real_performance.average_grade(),
                    "letter_grade": self._real_performance.get_letter_grade()
                },
                "desired_performance": {
                    "subjects": self._desired_performance.subjects,
                    "desired_grades": self._desired_performance.grades,
                    "desired_average": self._desired_performance.average_grade(),
                    "improvement_needed": self._get_improvement_needed()
                }
            }
        except Exception as e:
            raise ValidationError(f"Помилка при перетворенні даних: {str(e)}")
    
    def _get_improvement_needed(self) -> Dict[str, float]:
        """
        Обчислює необхідне покращення для досягнення бажаного середнього балу.
        
        Повертає:
            Dict[str, float]: Словник з необхідним покращенням по кожному предмету
        """
        improvement = {}
        for subj, real, desired in zip(
            self._real_performance.subjects,
            self._real_performance.grades,
            self._desired_performance.grades
        ):
            improvement[subj] = max(0, desired - real)
        return improvement


class DataStorage(ABC):
    """
    Абстрактний базовий клас для зберігання даних.
    """
    
    @abstractmethod
    def save(self, data: Dict[str, Any], filename: str) -> None:
        """
        Абстрактний метод для збереження даних.
        
        Аргументи:
            data (Dict[str, Any]): Дані для збереження
            filename (str): Ім'я файлу для збереження (без розширення)
            
        Винятки:
            ValidationError: Якщо дані не валідні
            IOError: Якщо виникла помилка під час запису у файл
        """
        pass


class JSONStorage(DataStorage):
    """
    Клас для зберігання даних у форматі JSON.
    """
    
    def save(self, data: Dict[str, Any], filename: str) -> None:
        """
        Зберігає дані у JSON файл.
        
        Аргументи:
            data (Dict[str, Any]): Дані для збереження
            filename (str): Ім'я файлу (без розширення)
            
        Винятки:
            ValidationError: Якщо дані не валідні
            IOError: Якщо не вдалося записати у файл
        """
        if not data:
            raise ValidationError("Немає даних для збереження")
            
        try:
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, default=str)
        except (IOError, json.JSONEncodeError) as e:
            raise IOError(f"Помилка при збереженні у JSON: {str(e)}")


class XMLStorage(DataStorage):
    """
    Клас для зберігання даних у форматі XML.
    """
    
    def _dict_to_xml(self, tag: str, d: Dict[str, Any]) -> ET.Element:
        """
        Рекурсивно перетворює словник у XML елемент.
        
        Аргументи:
            tag (str): Тег для кореневого елемента
            d (Dict[str, Any]): Словник для перетворення
            
        Повертає:
            ET.Element: Кореневий XML елемент
        """
        elem = ET.Element(tag)
        for key, val in d.items():
            # Замінюємо пробіли та інші небажані символи у назвах тегів
            safe_key = "".join(c if c.isalnum() else "_" for c in str(key))
            child = ET.Element(safe_key)
            
            if isinstance(val, dict):
                child = self._dict_to_xml(safe_key, val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        child.append(self._dict_to_xml('item', item))
                    else:
                        child_item = ET.Element('item')
                        child_item.text = str(item)
                        child.append(child_item)
            else:
                child.text = str(val) if val is not None else ""
            elem.append(child)
        return elem
    
    def save(self, data: Dict[str, Any], filename: str) -> None:
        """
        Зберігає дані у XML файл.
        
        Аргументи:
            data (Dict[str, Any]): Дані для збереження
            filename (str): Ім'я файлу (без розширення)
            
        Винятки:
            ValidationError: Якщо дані не валідні
            ET.ParseError: Якщо виникла помилка при створенні XML
            IOError: Якщо не вдалося записати у файл
        """
        if not data:
            raise ValidationError("Немає даних для збереження")
            
        try:
            root = self._dict_to_xml('student_data', data)
            tree = ET.ElementTree(root)
            
            # Додаємо форматування для кращого читання
            self._indent(root)
            
            # Записуємо у файл з кодуванням UTF-8 та заголовком
            with open(f"{filename}.xml", 'wb') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
                tree.write(f, encoding='utf-8', xml_declaration=False)
                
        except (ET.ParseError, IOError) as e:
            raise IOError(f"Помилка при збереженні у XML: {str(e)}")
    
    def _indent(self, elem: ET.Element, level: int = 0) -> None:
        """
        Допоміжна функція для форматування XML з відступами.
        
        Аргументи:
            elem (ET.Element): Кореневий елемент
            level (int): Поточний рівень вкладеності
        """
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


class CSVStorage(DataStorage):
    """
    Клас для зберігання даних у форматі CSV.
    """
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Рекурсивно розгладжує вкладений словник.
        
        Аргументи:
            d (Dict[str, Any]): Вхідний словник
            parent_key (str): Батьківський ключ для вкладених словників
            sep (str): Роздільник між рівнями вкладеності
            
        Повертає:
            Dict[str, Any]: Розгладжений словник
        """
        items = []
        for k, v in d.items():
            # Замінюємо пробіли та інші небажані символи у назвах стовпців
            safe_key = "".join(c if c.isalnum() else "_" for c in str(k))
            new_key = f"{parent_key}{sep}{safe_key}" if parent_key else safe_key
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Обробляємо списки, перетворюючи їх у рядок з роздільником
                items.append((new_key, '; '.join(map(str, v))))
            else:
                items.append((new_key, v if v is not None else ""))
        return dict(items)
    
    def save(self, data: Dict[str, Any], filename: str) -> None:
        """
        Зберігає дані у CSV файл.
        
        Аргументи:
            data (Dict[str, Any]): Дані для збереження
            filename (str): Ім'я файлу (без розширення)
            
        Винятки:
            ValidationError: Якщо дані не валідні
            csv.Error: Якщо виникла помилка при записі CSV
            IOError: Якщо не вдалося записати у файл
        """
        if not data:
            raise ValidationError("Немає даних для збереження")
            
        try:
            import csv
            
            # Розгладжуємо вкладений словник
            flat_data = self._flatten_dict(data)
            
            # Відкриваємо файл для запису з обробкою кодування
            with open(f"{filename}.csv", 'w', newline='', encoding='utf-8-sig') as f:
                # Використовуємо DictWriter для запису заголовків
                writer = csv.DictWriter(f, fieldnames=flat_data.keys())
                writer.writeheader()
                writer.writerow(flat_data)
                
        except (csv.Error, IOError) as e:
            raise IOError(f"Помилка при збереженні у CSV: {str(e)}")
