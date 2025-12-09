# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute():
	"""Add default person statuses for CRM Lead Person"""
	statuses = {
		"Active": {
			"color": "green",
			"position": 1,
		},
		"Inactive": {
			"color": "gray",
			"position": 2,
		},
		"Decision Maker": {
			"color": "blue",
			"position": 3,
		},
		"Influencer": {
			"color": "purple",
			"position": 4,
		},
		"Gatekeeper": {
			"color": "orange",
			"position": 5,
		},
		"Champion": {
			"color": "green",
			"position": 6,
		},
		"End User": {
			"color": "cyan",
			"position": 7,
		},
	}

	for status in statuses:
		if frappe.db.exists("CRM Person Status", status):
			continue

		doc = frappe.new_doc("CRM Person Status")
		doc.status_name = status
		doc.color = statuses[status]["color"]
		doc.position = statuses[status]["position"]
		doc.insert(ignore_permissions=True)

