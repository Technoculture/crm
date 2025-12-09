import json
import frappe


def execute():
	"""Add contacts_section to CRM Lead Side Panel layout"""
	if not frappe.db.exists("CRM Fields Layout", {"dt": "CRM Lead", "type": "Side Panel"}):
		return

	layout_doc = frappe.get_doc("CRM Fields Layout", {"dt": "CRM Lead", "type": "Side Panel"})
	
	if not layout_doc.layout:
		return
	
	layout = json.loads(layout_doc.layout)
	
	# Check if contacts_section already exists
	for section in layout:
		if section.get("name") == "contacts_section" or section.get("label") == "Contacts":
			return
	
	# Find person_tab index to insert contacts_section after it
	person_tab_index = None
	for i, section in enumerate(layout):
		if section.get("name") == "person_tab" or section.get("label") == "Person":
			person_tab_index = i
			break
	
	contacts_section = {
		"label": "Contacts",
		"name": "contacts_section",
		"opened": True,
		"editable": False,
		"contacts": []
	}
	
	if person_tab_index is not None:
		layout.insert(person_tab_index + 1, contacts_section)
	else:
		# Insert at beginning if person_tab not found
		layout.insert(0, contacts_section)
	
	layout_doc.layout = json.dumps(layout)
	layout_doc.save(ignore_permissions=True)

