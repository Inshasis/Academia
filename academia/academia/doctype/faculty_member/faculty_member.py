# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
from frappe import _
import re
from datetime import datetime

from academia.academia.doctype.faculty_member_academic_ranking.faculty_member_academic_ranking import FacultyMemberAcademicRanking

from academia.academia.doctype.faculty_member_academic_services.faculty_member_academic_services import FacultyMemberAcademicServices

from academia.academia.doctype.faculty_member_activity.faculty_member_activity import FacultyMemberActivity
from academia.academia.doctype.faculty_member_award_and_appreciation_certificate.faculty_member_award_and_appreciation_certificate import FacultyMemberAwardandAppreciationCertificate
from academia.academia.doctype.faculty_member_conference_and_workshop.faculty_member_conference_and_workshop import FacultyMemberConferenceandWorkshop
from academia.academia.doctype.faculty_member_course.faculty_member_course import FacultyMemberCourse
from academia.academia.doctype.faculty_member_language.faculty_member_language import FacultyMemberLanguage

from academia.academia.doctype.faculty_member_training_course.faculty_member_training_course import FacultyMemberTrainingCourse
from academia.academia.doctype.faculty_member_university_and_community_service.faculty_member_university_and_community_service import FacultyMemberUniversityandCommunityService
from frappe.types import DF

class FacultyMember(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academia.doctype.faculty_member_academic_ranking.faculty_member_academic_ranking import FacultyMemberAcademicRanking
        from academia.academia.doctype.faculty_member_academic_services.faculty_member_academic_services import FacultyMemberAcademicServices
        from academia.academia.doctype.faculty_member_activity.faculty_member_activity import FacultyMemberActivity
        from academia.academia.doctype.faculty_member_award_and_appreciation_certificate.faculty_member_award_and_appreciation_certificate import FacultyMemberAwardandAppreciationCertificate
        from academia.academia.doctype.faculty_member_conference_and_workshop.faculty_member_conference_and_workshop import FacultyMemberConferenceandWorkshop
        from academia.academia.doctype.faculty_member_course.faculty_member_course import FacultyMemberCourse
        from academia.academia.doctype.faculty_member_language.faculty_member_language import FacultyMemberLanguage
        from academia.academia.doctype.faculty_member_training_course.faculty_member_training_course import FacultyMemberTrainingCourse
        from academia.academia.doctype.faculty_member_university_and_community_service.faculty_member_university_and_community_service import FacultyMemberUniversityandCommunityService
        from frappe.types import DF

        academic_rank: DF.Link
        academic_services: DF.TableMultiSelect[FacultyMemberAcademicServices]
        company: DF.Link
        courses: DF.TableMultiSelect[FacultyMemberCourse]
        date: DF.Date | None
        date_of_joining_in_service: DF.Date | None
        date_of_joining_in_university: DF.Date | None
        decision_attachment: DF.Attach | None
        decision_number: DF.Int
        department: DF.Link | None
        employee: DF.Link
        employment_type: DF.Data | None
        faculty: DF.Link | None
        faculty_member_academic_ranking: DF.Table[FacultyMemberAcademicRanking]
        faculty_member_activity: DF.Table[FacultyMemberActivity]
        faculty_member_award_and_appreciation_certificate: DF.Table[FacultyMemberAwardandAppreciationCertificate]
        faculty_member_conference_and_workshop: DF.Table[FacultyMemberConferenceandWorkshop]
        faculty_member_name: DF.Data
        faculty_member_name_english: DF.Data | None
        faculty_member_training_course: DF.Table[FacultyMemberTrainingCourse]
        faculty_member_university_and_community_service: DF.Table[FacultyMemberUniversityandCommunityService]
        from_another_university: DF.Link | None
        general_field: DF.Data | None
        google_scholar_profile_link: DF.Data | None
        image: DF.AttachImage | None
        languages: DF.TableMultiSelect[FacultyMemberLanguage]
        naming_series: DF.Literal["ACAD-FM-"]
        nationality: DF.Link | None
        specialist_field: DF.Data | None
    # end: auto-generated types
    

    # end: auto-generated types

    # Start of validate controller hook
    def validate(self):
        # Calling functions
        self.validate_duplicate_employee()
        self.validate_date()
        self.validate_url()
    # End of validate controller hook
   
    # FN: validate duplicate 'employee' field
    def validate_duplicate_employee(self):
          if self.employee:
            exist_employee = frappe.get_value("Faculty Member", {"employee": self.employee, "name": ["!=", self.name]}, "faculty_member_name")
            if exist_employee:
                frappe.throw(f"Employee {self.employee} is already assigned to {exist_employee}")    
    # End of the function

    # FN: validate 'date_of_joining_in_university' and 'date_of_joining_in_service' fields
    def validate_date(self):
        today = datetime.now().date()
        if self.date_of_joining_in_university and self.date_of_joining_in_service:
            # "Converting the date of appointment in service to a date "
            date_of_joining_in_service = datetime.strptime(self.date_of_joining_in_service, "%Y-%m-%d").date()
            date_of_joining_in_university = datetime.strptime(self.date_of_joining_in_university, "%Y-%m-%d").date()
            #  "Ensure that the date of appointment in service is before the date of appointment in the university."
            if date_of_joining_in_service >= date_of_joining_in_university:
                frappe.throw(_("Date of Service Appointment must be before Date of University Appointment"))
            elif date_of_joining_in_service > today:
                frappe.throw(_("Date of Service Appointment cannot be after today's date"))
            elif date_of_joining_in_university > today:
                frappe.throw(_("Date of University Appointment cannot be after today's date"))
    # End of the function

    # FN: validate 'google_scholar_profile_link' field
    def validate_url(self):
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        if self.google_scholar_profile_link:
            if not url_pattern.match(self.google_scholar_profile_link):
                frappe.throw("Google Scholar Profile Link is not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function

		



