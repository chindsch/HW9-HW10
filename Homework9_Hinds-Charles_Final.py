""" Chelsea Hinds-Charles
    SSW 810
    Homework 9: Student and Instructor summary tables
"""

import os
import logging
import unittest
from collections import defaultdict
from prettytable import PrettyTable



class Repository:
    """Repository class to read files, validate files, and create contains for data storage"""
    
    def __init__(self,cwd):
        """validate path for directory"""
        self.cwd = cwd

        
        self.studentdict = {}  # key: student cwid value: instance of class student
        self.instructordict = {}  # key: instructor cwid value: instance of class Instructor
        
        self.student(os.path.join(cwd,'students.txt'))
        self.instructor(os.path.join(cwd,'instructors.txt'))
        self.gradesprocessing(os.path.join(cwd,'grades.txt'))
            
    
    def student(self,path):
        """validate student file and create primary student dictionary"""
        try:
            sfile = open(path, 'r')
        except FileNotFoundError:
            logging.exception('There is an error with opening the student file in this directory')
        else:
            if sfile.readlines() == ['\n']:
                print('This file is an empty!')
            else:
                sfile.seek(0)
                for lines in sfile:
                    fields = lines.strip().split('\t')
                    if len(fields) != 3:
                        raise ValueError('Number of fields on line not expected')
                    studentid, studentname, studentmajor = lines.strip().split('\t')
                    self.studentdict[studentid] = Student(studentid,studentname,studentmajor)


    def instructor(self, path):
        """Validate instructors file and create primary instructors dictionary"""
        try:
            ifile = open(path, 'r')
        except FileNotFoundError:
            logging.exception('There is an error with opening the file to analyze')
        else:
            if ifile.readlines() == ['\n']:
                print('This file is an empty!')
            else:
                ifile.seek(0)
                for lines in ifile:
                    fields = lines.strip().split('\t')
                    if len(fields) != 3:
                        raise ValueError('Number of fields on line not expected')
                    instructorid,instructorname,instructordept = lines.strip().split('\t')
                    self.instructordict[instructorid] = Instructor(instructorid,instructorname,instructordept)

                
    def gradesprocessing(self,path):
        """validate grades file, and create course grade dictionary for students info"""
        try:
            gfile = open(path, 'r')
        except FileNotFoundError:
            logging.exception('There is an error with opening the file to analyze')
        else:
            if gfile.readlines() == ['\n']:
                print('This file is an empty!')
            else:
                gfile.seek(0)
                for lines in gfile:
                    fields = lines.strip().split('\t')
                    if len(fields) != 4:
                        raise ValueError('Number of fields on line not expected')
                    studentid,studentcourse, studentgrade,instructorid = lines.strip().split('\t')
                    if studentid in self.studentdict:
                        s = self.studentdict[studentid]
                        s.add_coursegrade(studentcourse, studentgrade)
                    else:
                        print('Unknown student found')
                        
                    if instructorid in self.instructordict:
                        self.instructordict[instructorid].add_coursestudent(studentcourse)
                    else:
                        print('Unknown Instructor found')


    def ptablestudent(self):
        """Print all students prettytable"""
        pt = PrettyTable(field_names = ['CWID','Name','Completed Courses'])
        for s in self.studentdict.values():  # s is an instance of class Student
            pt.add_row(s.studentdetails())
        print(pt)
        
    
    def ptableinstructor(self):
        """Print all instructors prettytable"""
        pt = PrettyTable(field_names = ['CWID','Name','Dept','Course','Students'])
        for i in self.instructordict.values(): # i is an instance of class Instructor
            for line in i.instructordetails():
                pt.add_row(line)
        print(pt)





        
class Student:
    """Student class for creating an instance of one student, and printing individual details"""

    
    def __init__(self,studentid, studentname, studentmajor):
        self.studentid = studentid
        self.studentname = studentname
        self.studentmajor = studentmajor
        self.coursegrades = {}  # key: course name value: grade
        
    def add_coursegrade(self,course,grade):
        self.coursegrades[course] = grade
        
    def studentdetails(self):
        return [self.studentid, self.studentname, sorted(self.coursegrades.keys())] 
        
   
class Instructor:
    """Instructor class for creating an instance of one instructor, and printing individual details"""
    
    def __init__(self,instructorid,instructorname, instructordept ):
        self.instructorid = instructorid
        self.instructorname = instructorname
        self.instructordept = instructordept
        self.coursestudents = defaultdict(int)  # key: course name value: number of students
        
    def add_coursestudent(self,course):
        self.coursestudents[course] += 1
    
    def instructordetails(self):
        """ return one line at a time with id, name, course, number of students """
        for course, studentnum in self.coursestudents.items():
            yield [self.instructorid, self.instructorname, self.instructordept, course, studentnum]
            
    def one_instructordetails(self):
        """ return one line at a time with id, name, course, number of students """
        for course, studentnum in self.coursestudents.items():
            return [self.instructorid, self.instructorname, self.instructordept, course, studentnum]
 

def main():
    """main() function to assign directory for files, and to print prettytables"""
    cwd = '/Users/chelseacharles/Documents/Spring2018Courses/SSW810/PythonHomework'
    repo = Repository(cwd)
    repo.ptablestudent()
    repo.ptableinstructor()
    
    
    
if __name__ == '__main__':
    main()









class StudentsTest(unittest.TestCase):
    """Testing Student.studentdetails() method"""
    
    
    def test_studentdetails(self):
        """test cases for studentdetails() method"""
        student = Student('10103', 'Baldwin, C','SFEN')
        student.add_coursegrade('SSW 567', 'A')
        self.assertEqual(student.studentdetails(), ['10103', 'Baldwin, C', ['SSW 567']])



class InstructorTest(unittest.TestCase):
    """Testing Instructor.instructordetails() method"""
    
    
    def test_instructordetails(self):
        """test cases for instructordetails() method"""
        instructor = Instructor('98763','Newton, I','SYEN')
        instructor.add_coursestudent('SYS 660')
        self.assertEqual(instructor.one_instructordetails(), ['98763', 'Newton, I', 'SYEN', 'SYS 660', 1])



class RepositoryTest(unittest.TestCase):
    """Testing Repository class methods"""
    
    
    def test_Repository(self):
        """test cases for Repository class methods"""
        cwd = '/Users/chelseacharles/Documents/Spring2018Courses/SSW810/test_repo'
        repo = Repository(cwd)  #Instance of instructor used for testing
        self.assertEqual(repo.student(os.path.join(cwd,'students.txt')), None)
        self.assertEqual(repo.instructor(os.path.join(cwd,'instructors.txt')), None)
        self.assertEqual(repo.gradesprocessing(os.path.join(cwd,'grades.txt')), None)




if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    












        
        
        
