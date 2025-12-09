# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CRMLeadPerson(Document):
	def validate(self):
		self.set_full_name()
		self.validate_primary_email()
		self.validate_primary_phone()

	def set_full_name(self):
		"""Set the full name from first_name and last_name"""
		self.full_name = " ".join(
			filter(None, [self.salutation, self.first_name, self.last_name])
		)

	def validate_primary_email(self):
		"""Ensure only one email is marked as primary"""
		if not self.emails:
			return
		primary_count = sum(1 for e in self.emails if e.is_primary)
		if primary_count > 1:
			frappe.throw(_("Only one email can be set as primary"))
		if primary_count == 0 and len(self.emails) == 1:
			self.emails[0].is_primary = 1

	def validate_primary_phone(self):
		"""Ensure only one phone is marked as primary"""
		if not self.phones:
			return
		primary_count = sum(1 for p in self.phones if p.is_primary)
		if primary_count > 1:
			frappe.throw(_("Only one phone can be set as primary"))
		if primary_count == 0 and len(self.phones) == 1:
			self.phones[0].is_primary = 1

	def get_primary_email(self):
		"""Get the primary email address"""
		for email in self.emails:
			if email.is_primary:
				return email.email
		return self.emails[0].email if self.emails else None

	def get_primary_phone(self):
		"""Get the primary phone number"""
		for phone in self.phones:
			if phone.is_primary:
				return phone.phone
		return self.phones[0].phone if self.phones else None


@frappe.whitelist()
def get_lead_persons(lead):
	"""Get all persons associated with a lead"""
	persons = frappe.get_all(
		"CRM Lead Person",
		filters={"lead": lead},
		fields=[
			"name", "salutation", "first_name", "last_name", "full_name",
			"status", "job_title", "department", "is_primary", "image"
		],
		order_by="is_primary desc, modified desc"
	)
	
	for person in persons:
		# Get primary email
		emails = frappe.get_all(
			"CRM Person Email",
			filters={"parent": person.name},
			fields=["email", "email_type", "is_primary"],
			order_by="is_primary desc"
		)
		person["emails"] = emails
		person["primary_email"] = next((e.email for e in emails if e.is_primary), emails[0].email if emails else None)
		
		# Get primary phone
		phones = frappe.get_all(
			"CRM Person Phone",
			filters={"parent": person.name},
			fields=["phone", "phone_type", "is_primary"],
			order_by="is_primary desc"
		)
		person["phones"] = phones
		person["primary_phone"] = next((p.phone for p in phones if p.is_primary), phones[0].phone if phones else None)
		
		# Get degrees
		degrees = frappe.get_all(
			"CRM Person Degree",
			filters={"parent": person.name},
			fields=["degree", "institution", "year"]
		)
		person["degrees"] = degrees
		
		# Get status color
		if person.status:
			person["status_color"] = frappe.db.get_value("CRM Person Status", person.status, "color") or "gray"
		else:
			person["status_color"] = "gray"
	
	return persons


@frappe.whitelist()
def add_person(lead, person_data):
	"""Add a new person to a lead"""
	if not frappe.has_permission("CRM Lead", "write", lead):
		frappe.throw(_("Not allowed to add person to Lead"), frappe.PermissionError)
	
	import json
	if isinstance(person_data, str):
		person_data = json.loads(person_data)
	
	person = frappe.new_doc("CRM Lead Person")
	person.lead = lead
	person.update(person_data)
	person.insert(ignore_permissions=True)
	
	return person.name


@frappe.whitelist()
def update_person(person_name, person_data):
	"""Update an existing person"""
	person = frappe.get_doc("CRM Lead Person", person_name)
	
	if not frappe.has_permission("CRM Lead", "write", person.lead):
		frappe.throw(_("Not allowed to update person"), frappe.PermissionError)
	
	import json
	if isinstance(person_data, str):
		person_data = json.loads(person_data)
	
	person.update(person_data)
	person.save(ignore_permissions=True)
	
	return person.name


@frappe.whitelist()
def delete_person(person_name):
	"""Delete a person"""
	person = frappe.get_doc("CRM Lead Person", person_name)
	
	if not frappe.has_permission("CRM Lead", "write", person.lead):
		frappe.throw(_("Not allowed to delete person"), frappe.PermissionError)
	
	frappe.delete_doc("CRM Lead Person", person_name, ignore_permissions=True)
	return True


@frappe.whitelist()
def set_primary_person(lead, person_name):
	"""Set a person as primary for a lead"""
	if not frappe.has_permission("CRM Lead", "write", lead):
		frappe.throw(_("Not allowed to set primary person"), frappe.PermissionError)
	
	# Remove primary from all persons of this lead
	frappe.db.sql("""
		UPDATE `tabCRM Lead Person`
		SET is_primary = 0
		WHERE lead = %s
	""", lead)
	
	# Set the specified person as primary
	frappe.db.set_value("CRM Lead Person", person_name, "is_primary", 1)
	
	return True

