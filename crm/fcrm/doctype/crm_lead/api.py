import frappe
from frappe import _


@frappe.whitelist()
def get_lead_contacts(name):
	"""Get all contacts associated with a lead"""
	contacts = frappe.get_all(
		"CRM Contacts",
		filters={"parenttype": "CRM Lead", "parent": name},
		fields=["contact", "is_primary"],
		distinct=True,
	)
	lead_contacts = []
	for contact in contacts:
		if not contact.contact:
			continue

		is_primary = contact.is_primary
		contact_doc = frappe.get_doc("Contact", contact.contact).as_dict()

		_contact = {
			"name": contact_doc.name,
			"image": contact_doc.image,
			"full_name": contact_doc.full_name,
			"email": contact_doc.email_id,
			"mobile_no": contact_doc.mobile_no,
			"is_primary": is_primary,
		}
		lead_contacts.append(_contact)
	return lead_contacts


@frappe.whitelist()
def add_contact(lead, contact):
	"""Add a contact to a lead"""
	if not frappe.has_permission("CRM Lead", "write", lead):
		frappe.throw(_("Not allowed to add contact to Lead"), frappe.PermissionError)

	lead_doc = frappe.get_cached_doc("CRM Lead", lead)
	
	# Check if contact already exists
	for existing_contact in lead_doc.contacts:
		if existing_contact.contact == contact:
			frappe.throw(_("Contact already added to this lead"))
	
	lead_doc.append("contacts", {"contact": contact})
	lead_doc.save()
	return True


@frappe.whitelist()
def remove_contact(lead, contact):
	"""Remove a contact from a lead"""
	if not frappe.has_permission("CRM Lead", "write", lead):
		frappe.throw(_("Not allowed to remove contact from Lead"), frappe.PermissionError)

	lead_doc = frappe.get_cached_doc("CRM Lead", lead)
	lead_doc.contacts = [d for d in lead_doc.contacts if d.contact != contact]
	lead_doc.save()
	return True


@frappe.whitelist()
def set_primary_contact(lead, contact):
	"""Set a contact as primary for a lead"""
	if not frappe.has_permission("CRM Lead", "write", lead):
		frappe.throw(_("Not allowed to set primary contact for Lead"), frappe.PermissionError)

	lead_doc = frappe.get_cached_doc("CRM Lead", lead)
	lead_doc.set_primary_contact(contact)
	lead_doc.save()
	return True

