from abc import ABC, abstractmethod
from datetime import date
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Any, Union

class Student:
    def __init__(self, last_name: str, first_name: str, middle_name: str, group_number: str, birth_date: date, address: str = ""):
        self._last_name = last_name
        self._first_name = first_name
        self._middle_name = middle_name
        self._group_number = group_number
        self._birth_date = birth_date
        self._address = address

    # Getters
    @property
    def full_name(self) -> str:
        return f"{self._last_name} {self._first_name} {self._middle_name}"
    
    @property
    def group_number(self) -> str:
        return self._group_number
    
    @property
    def birth_date(self) -> date:
        return self._birth_date
    
    @property
    def address(self) -> str:
        return self._address
    
    # Setters
    @group_number.setter
    def group_number(self, value: str):
        self._group_number = value
    
    @address.setter
    def address(self, value: str):
        self._address = value


class AcademicPerformance(ABC):
    def __init__(self, subjects: List[str], grades: List[int]):
        self._subjects = subjects
        self._grades = grades
    
    @property
    def subjects(self) -> List[str]:
        return self._subjects
    
    @property
    def grades(self) -> List[int]:
        return self._grades
    
    @abstractmethod
    def average_grade(self) -> float:
        pass


class DesiredPerformance(AcademicPerformance):
    def __init__(self, subjects: List[str], desired_grades: List[int]):
        super().__init__(subjects, desired_grades)
    
    def average_grade(self) -> float:
        if not self._grades:
            return 0.0
        return sum(self._grades) / len(self._grades)


class RealPerformance(AcademicPerformance):
    def __init__(self, subjects: List[str], actual_grades: List[int]):
        super().__init__(subjects, actual_grades)
    
    def average_grade(self) -> float:
        if not self._grades:
            return 0.0
        return sum(self._grades) / len(self._grades)


class StudentData:
    def __init__(self, student: Student, real_performance: RealPerformance, desired_performance: DesiredPerformance):
        self._student = student
        self._real_performance = real_performance
        self._desired_performance = desired_performance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "student": {
                "full_name": self._student.full_name,
                "group_number": self._student.group_number,
                "birth_date": self._student.birth_date.isoformat(),
                "address": self._student.address
            },
            "real_performance": {
                "subjects": self._real_performance.subjects,
                "grades": self._real_performance.grades,
                "average_grade": round(self._real_performance.average_grade(), 2)
            },
            "desired_performance": {
                "subjects": self._desired_performance.subjects,
                "desired_grades": self._desired_performance.grades,
                "desired_average": round(self._desired_performance.average_grade(), 2)
            }
        }


class DataStorage(ABC):
    @abstractmethod
    def save(self, data: Dict[str, Any], filename: str) -> None:
        pass


class JSONStorage(DataStorage):
    def save(self, data: Dict[str, Any], filename: str) -> None:
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class XMLStorage(DataStorage):
    def save(self, data: Dict[str, Any], filename: str) -> None:
        def dict_to_xml(tag: str, d: Dict[str, Any]) -> ET.Element:
            elem = ET.Element(tag)
            for key, val in d.items():
                child = ET.Element(key)
                if isinstance(val, dict):
                    child = dict_to_xml(key, val)
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            child.append(dict_to_xml('item', item))
                        else:
                            child_item = ET.Element('item')
                            child_item.text = str(item)
                            child.append(child_item)
                else:
                    child.text = str(val)
                elem.append(child)
            return elem

        root = dict_to_xml('student_data', data)
        tree = ET.ElementTree(root)
        tree.write(f"{filename}.xml", encoding='utf-8', xml_declaration=True)


class CSVStorage(DataStorage):
    def save(self, data: Dict[str, Any], filename: str) -> None:
        import csv
        
        def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str='.') -> Dict[str, Any]:
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    items.append((new_key, ';'.join(map(str, v))))
                else:
                    items.append((new_key, v))
            return dict(items)
        
        flat_data = flatten_dict(data)
        with open(f"{filename}.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=flat_data.keys())
            writer.writeheader()
            writer.writerow(flat_data)
