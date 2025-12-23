from student_management import (
    Student, RealPerformance, DesiredPerformance, StudentData, 
    JSONStorage, XMLStorage, CSVStorage, ValidationError
)
from datetime import date
import sys

def create_student():
    """Створює об'єкт студента з валідацією введених даних."""
    print("\n=== Введення даних студента ===")
    
    while True:
        try:
            last_name = input("Введіть прізвище: ").strip()
            first_name = input("Введіть ім'я: ").strip()
            middle_name = input("Введіть по батькові: ").strip()
            group_number = input("Введіть номер групи: ").strip()
            
            # Введення дати народження
            while True:
                try:
                    birth_date_str = input("Введіть дату народження (рррр-мм-дд): ").strip()
                    year, month, day = map(int, birth_date_str.split('-'))
                    birth_date = date(year, month, day)
                    break
                except ValueError as e:
                    print(f"Помилка: {e}. Спробуйте ще раз.")
            
            address = input("Введіть адресу (необов'язково): ").strip()
            
            student = Student(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                group_number=group_number,
                birth_date=birth_date,
                address=address
            )
            return student
            
        except ValidationError as e:
            print(f"Помилка валідації: {e}")
            print("Будь ласка, спробуйте ще раз.\n")
        except Exception as e:
            print(f"Неочікувана помилка: {e}")
            sys.exit(1)

def create_performance(performance_type: str):
    """Створює об'єкт успішності (реальної або бажаної)."""
    print(f"\n=== Введення {performance_type} успішності ===")
    
    while True:
        try:
            subjects = []
            grades = []
            
            # Введення кількості предметів
            while True:
                try:
                    num_subjects = int(input("Введіть кількість предметів: ").strip())
                    if num_subjects <= 0:
                        print("Кількість предметів має бути більше 0")
                        continue
                    break
                except ValueError:
                    print("Будь ласка, введіть ціле число.")
            
            # Введення даних по кожному предмету
            for i in range(1, num_subjects + 1):
                subject = input(f"\nПредмет {i}: ").strip()
                while not subject:
                    print("Назва предмету не може бути порожньою")
                    subject = input(f"Предмет {i}: ").strip()
                
                while True:
                    try:
                        grade = int(input(f"Оцінка за предмет '{subject}': ").strip())
                        if not (0 <= grade <= 100):
                            print("Оцінка має бути в діапазоні від 0 до 100")
                            continue
                        break
                    except ValueError:
                        print("Будь ласка, введіть ціле число.")
                
                subjects.append(subject)
                grades.append(grade)
            
            # Повертаємо відповідний об'єкт успішності
            if performance_type == "реальної":
                return RealPerformance(subjects=subjects, actual_grades=grades)
            else:
                return DesiredPerformance(subjects=subjects, desired_grades=grades)
                
        except ValidationError as e:
            print(f"Помилка валідації: {e}")
            print("Будь ласка, спробуйте ще раз.\n")
        except Exception as e:
            print(f"Неочікувана помилка: {e}")
            sys.exit(1)

def save_student_data(student_data, filename_prefix):
    """Зберігає дані студента у різних форматах."""
    try:
        data = student_data.to_dict()
        
        # Створюємо екземпляри класів для зберігання
        storages = {
            'JSON': JSONStorage(),
            'XML': XMLStorage(),
            'CSV': CSVStorage()
        }
        
        # Зберігаємо у всіх форматах
        saved_files = []
        for format_name, storage in storages.items():
            try:
                filename = f"{filename_prefix}_{format_name.lower()}"
                storage.save(data, filename)
                saved_files.append(f"{filename}.{format_name.lower()}")
                print(f"Дані успішно збережено у форматі {format_name}")
            except Exception as e:
                print(f"Помилка при збереженні у форматі {format_name}: {e}")
        
        return saved_files
        
    except Exception as e:
        print(f"Помилка при збереженні даних: {e}")
        return []

def display_student_info(student_data):
    """Виводить інформацію про студента у зручному вигляді."""
    data = student_data.to_dict()
    student = data['student']
    real = data['real_performance']
    desired = data['desired_performance']
    
    print("\n" + "="*50)
    print(f"ІНФОРМАЦІЯ ПРО СТУДЕНТА".center(50))
    print("="*50)
    
    # Інформація про студента
    print("\n👤 ОСОБИСТІ ДАНІ")
    print(f"ПІБ: {student['full_name']}")
    print(f"Група: {student['group_number']}")
    print(f"Вік: {student['age']} років")
    print(f"Адреса: {student['address'] or 'не вказано'}")
    
    # Реальна успішність
    print("\n📊 РЕАЛЬНА УСПІШНІСТЬ")
    for subj, grade in zip(real['subjects'], real['grades']):
        print(f"- {subj}: {grade}")
    print(f"Середній бал: {real['average_grade']} ({real['letter_grade']})")
    
    # Бажана успішність
    print("\n🎯 БАЖАНА УСПІШНІСТЬ")
    for subj, grade in zip(desired['subjects'], desired['desired_grades']):
        print(f"- {subj}: {grade} (поточний: {real['grades'][desired['subjects'].index(subj)]})")
    print(f"Бажаний середній бал: {desired['desired_average']}")
    
    # Потрібне покращення
    print("\n📈 ПОТРІБНЕ ПОКРАЩЕННЯ")
    for subj, improvement in desired['improvement_needed'].items():
        if improvement > 0:
            print(f"- {subj}: +{improvement} балів")
    
    print("\n" + "="*50 + "\n")

def main():
    print("="*50)
    print("ПРОГРАМА ОБЛІКУ УСПІШНОСТІ СТУДЕНТІВ".center(50))
    print("="*50)
    
    try:
        # Створення об'єктів
        student = create_student()
        print("\nВведення реальної успішності:")
        real_performance = create_performance("реальної")
        
        print("\nВведення бажаної успішності:")
        print("Примітка: кількість предметів має співпадати з реальною успішністю")
        
        # Перевірка кількості предметів
        while True:
            desired_performance = create_performance("бажаної")
            if len(desired_performance.subjects) != len(real_performance.subjects):
                print("Помилка: Кількість предметів має співпадати з реальною успішністю")
                continue
                
            # Перевірка відповідності предметів
            if desired_performance.subjects != real_performance.subjects:
                print("Помилка: Списки предметів мають співпадати")
                print(f"Очікувано: {', '.join(real_performance.subjects)}")
                continue
            break
        
        # Створення об'єкта з даними студента
        student_data = StudentData(student, real_performance, desired_performance)
        
        # Вивід інформації
        display_student_info(student_data)
        
        # Збереження даних
        filename = input("\nВведіть префікс для імені файлу (або натисніть Enter для 'student_data'): ").strip()
        filename = filename if filename else 'student_data'
        
        saved_files = save_student_data(student_data, filename)
        
        if saved_files:
            print("\n✅ Успішно збережено файли:")
            for file in saved_files:
                print(f"- {file}")
        else:
            print("\n❌ Не вдалося зберегти жодного файлу")
        
    except KeyboardInterrupt:
        print("\n\nРоботу програми перервано користувачем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Сталася критична помилка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
