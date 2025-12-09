import json
import frappe


def execute():
	"""Add contacts_section and persons_section to CRM Lead Side Panel layout"""
	if not frappe.db.exists("CRM Fields Layout", {"dt": "CRM Lead", "type": "Side Panel"}):
		return

	layout_doc = frappe.get_doc("CRM Fields Layout", {"dt": "CRM Lead", "type": "Side Panel"})
	
	if not layout_doc.layout:
		return
	
	layout = json.loads(layout_doc.layout)
	
	# Check if contacts_section already exists
	has_contacts = any(
		section.get("name") == "contacts_section" or section.get("label") == "Contacts"
		for section in layout
	)
	
	# Check if persons_section already exists
	has_persons = any(
		section.get("name") == "persons_section" or section.get("label") == "Persons"
		for section in layout
	)
	
	# Find person_section or person_tab index to insert sections after it
	person_section_index = None
	for i, section in enumerate(layout):
		if section.get("name") in ("person_tab", "person_section") or section.get("label") == "Person":
			person_section_index = i
			break
	
	insert_index = person_section_index + 1 if person_section_index is not None else 0
	
	if not has_persons:
		persons_section = {
			"label": "Persons",
			"name": "persons_section",
			"opened": True,
			"editable": False
		}
		layout.insert(insert_index, persons_section)
		insert_index += 1
	
	if not has_contacts:
		contacts_section = {
			"label": "Contacts",
			"name": "contacts_section",
			"opened": True,
			"editable": False,
			"contacts": []
		}
		layout.insert(insert_index, contacts_section)
	
	layout_doc.layout = json.dumps(layout)
	layout_doc.save(ignore_permissions=True)

