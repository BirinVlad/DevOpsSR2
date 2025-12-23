from student_management import Student, RealPerformance, DesiredPerformance, StudentData, JSONStorage, XMLStorage, CSVStorage
from datetime import date

def main():
    # Create a student
    student = Student(
        last_name="Іванов",
        first_name="Іван",
        middle_name="Іванович",
        group_number="КН-201",
        birth_date=date(2000, 5, 15),
        address="м. Київ, вул. Хрещатик, 1"
    )

    # Create real performance
    real_performance = RealPerformance(
        subjects=["Математика", "Фізика", "Програмування"],
        actual_grades=[85, 90, 88]
    )

    # Create desired performance
    desired_performance = DesiredPerformance(
        subjects=["Математика", "Фізика", "Програмування"],
        desired_grades=[90, 95, 95]
    )

    # Create student data
    student_data = StudentData(student, real_performance, desired_performance)
    
    # Get data as dictionary
    data = student_data.to_dict()
    
    # Save to different formats
    json_storage = JSONStorage()
    json_storage.save(data, "student_data")
    
    xml_storage = XMLStorage()
    xml_storage.save(data, "student_data")
    
    csv_storage = CSVStorage()
    csv_storage.save(data, "student_data")
    
    print("Дані успішно збережено у файли:")
    print("- student_data.json")
    print("- student_data.xml")
    print("- student_data.csv")

if __name__ == "__main__":
    main()
