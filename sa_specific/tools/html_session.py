#!/usr/bin/env python
#
#

import os, sys, pickle, string, os.path

def mkdir(d):
	try: os.mkdir(d)
	except OSError: pass

def html_escape(s):
	s = string.replace(s, '&', "&amp;")
	s = string.replace(s, '<', "&lt;")
	s = string.replace(s, '>', "&gt;")
	s = string.replace(s, '"', "&quot;")
	return s

def css():
	return """
<!--
html { background: #e25923 ; color: black }
body { background: #e25923 ; color: black }
th { text-align: left }
h1 { text-align: center }
-->
"""

class HtmlElem:
	def __init__(self, name):
		self.name = name

	def __call__(self, *data, **kwds):
		new = HtmlElem(self.name)
		new.data = data
		new.kwds = kwds
		return new

	def __str__(self):
		if self.kwds:
			kwds = [""]
			for k,v in self.kwds.items():
				k = string.replace(k, "_", "-")
				if v is None: kwds.append("%s" % k)
				else: kwds.append("%s=\"%s\"" % (k,v))
			kwds = string.join(kwds)
		else: kwds = ""
		open_tag  = "<%s%s>" % (string.lower(self.name), kwds)
		close_tag = "</%s>\n"  % (string.lower(self.name))
		if len(self.data):
			return open_tag + string.join(map(str, self.data), "") + close_tag
		else:
			return open_tag

class HtmlPage:
	def __init__(self, title = None, style = None):
		self.head = []
		self.body = []
		self.head.append(HtmlElem("meta")(
			http_equiv="content-type",
			content="text/html; charset=UTF-8",
		))
		if title is not None:
			self.head.append(HtmlElem("title")(title))
		if style is not None:
			self.head.append(HtmlElem("style")(style, type="text/css"))

	def append_head(self, itme):
		self.head.append(item)

	def append_body(self, item):
		self.body.append(item)

	append = append_body

	def __str__(self):
		html  = HtmlElem("html")
		head  = HtmlElem("head")
		title = HtmlElem("title")
		body  = HtmlElem("body")
		page = str(
			html(
				apply(head, self.head),
				apply(body, self.body),
			)
		)
		return page

	def write(self, filename, overwrite = 0):
		if os.path.exists(filename) and not overwrite: return
		outfile = open(filename, "w")
		outfile.write(str(self))
		outfile.close()

class TableElem:
	def __init__(self, *data, **kwds):
		self.data = list(data)
		self.kwds = kwds

	def append(self, datum):
		self.data.append(datum)

	def extend(self, datum):
		self.data.extend(datum)

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		self.data[key] = value

	def __len__(self):
		return len(self.data)

	def __str__(self):
		if not len(self): return ""
		html_elem = HtmlElem(self.__class__.__name__)
		return "%s" % apply(html_elem, self.data, self.kwds)

class Table(TableElem): pass
class Tr(TableElem): pass
class Th(TableElem): pass
class Td(TableElem): pass

class WayObject:
	def class_name(self):
		return self.__class__.__name__

	def script(self):
		# XXX: add code to emit
		a_href = HtmlElem("a")
		ws  = self.data["WayScript"]
		wsv = self.data["WayScriptVersion"]
		if not ws or not wsv: return "---"
		script_name = ws["script_name"]
		script_vers = wsv["version"]

		ws_link  = "WayScript.%s.html" % (ws["id"])
		wsv_link = "WayScriptVersion.%s.html" % (wsv["id"])
		wsv_source = wsv["source"]

		h1 = HtmlElem("h1")
		h2 = HtmlElem("h2")
		hr = HtmlElem("hr")
		p = HtmlElem("p")
		pre = HtmlElem("pre")

		ws_table = Table(
			Tr(Th("Name")       , Td(script_name)),
			Tr(Th("ID")         , Td(ws["id"])),
			Tr(Th("Description"), Td(ws["script_desc"])),
			Tr(Th("Policy")     , Td(ws["policy"])),
			Tr(Th("Status")     , Td(ws["status"])),
			Tr(Th("Created By") , Td("%s on %s" % (
				ws["created_by"],
				ws["create_dt"],
				))),
			Tr(Th("Current Ver Set By"), Td("%s on %s" % (
				ws["current_version_set_by"],
				ws["current_version_set_dt"],
				))),
			border = 1
		)

		title = "Detailed info on Script %s" % script_name
		page = HtmlPage(title = title, style = css())
		page.append(h1("The Way It Was"))
		page.append(hr())
		page.append(h2(title))
		page.append(p(ws_table))
		page.write(ws_link)

		wsv_table = Table(
			Tr(Th("ID")                       , Td(wsv["id"])),
			Tr(Th("Comments for this Version"), Td(wsv["comments"])),
			Tr(Th("policy for this Version")  , Td(wsv["policy"])),
			Tr(Th("Version uploaded By")      , Td("%s on %s" % (
				wsv["uploaded_by"],
				wsv["upload_dt"],
				))),
			border = 1
		)
		title = "Viewing all info about script %s version %s" % (
			script_name, script_vers,
		)
		page = HtmlPage(title = title, style = css())
		page.append(h1("The Way It Was"))
		page.append(hr())
		page.append(h2(title))
		page.append(p(wsv_table))
		page.append(hr())
		page.append(pre(html_escape(wsv_source)))
		page.write(wsv_link)

		return "%s~%s" % (
			a_href(script_name, href=ws_link),
			a_href(script_vers, href=wsv_link),
		)

	def params(self):
		table = Table(border=1) 
		pre = HtmlElem("pre")
		for k,v in self.data["params"].items():
			if type(v) == type("") \
			and self.class_name() == "SessionCommand":
				v = pre(html_escape(str(v)))
			else:
				v = html_escape(str(v))
			table.append(Tr(Td(k), Td(v)))
		return table

	def results(self):
		table = Table(border=1)
		pre = HtmlElem("pre")
		for k,v in self.data["results"].items():
			if k == "$session_id":
				sub_session_dir = string.split(str(v), 'L')[0]
				v = '<a href="%s/index.html">%s</a>' % (sub_session_dir, v)
			elif type(v) == type("") \
			and self.class_name() == "SessionCommand":
				v = pre(html_escape(str(v)))
			else:
				v = html_escape(str(v))
			table.append(Tr( Td(k), Td(v)))
		return table

	def host_link(self):
		srvc_inst_id = eval(self.data["srvc_inst_id"])
		msi = self.session["MegaServiceInstance"][srvc_inst_id]
		msi_link = "MegaServiceInstance.%s.html" % msi["id"]
	
		host_table = Table(
			Tr(Td("Service Instance ID"), Td(msi["id"])),
			Tr(Td("Host name")          , Td(msi.get("host_name",""))),
			Tr(Td("System name")        , Td(msi["system_name"])),
			Tr(Td("IP address")         , Td(msi["ip_address"])),
			Tr(Td("Device ID")          , Td(msi["dvc_id"])),
			Tr(Td("Port")               , Td(msi["port"])),
			Tr(Td("Service Type")       , Td(msi["srvc_type"])),
			Tr(Td("Data Center")        , Td(msi.get("data_center_name",""))),
			Tr(Td("Account")            , Td(msi.get("acct_name",""))),
			border = 1
		)
		a_href = HtmlElem("a")
		h1 = HtmlElem("h1")
		h2 = HtmlElem("h2")
		hr = HtmlElem("hr")
		p = HtmlElem("p")

		title = "Service Instance %s" % msi["id"]
		page = HtmlPage(title = title, style = css())
		page.append(h1("The Way It Was"))
		page.append(hr())
		page.append(h2(title))
		page.append(p(host_table))
		page.write(msi_link)

		return a_href(msi["system_name"], href = msi_link)

	def host(self):
		srvc_inst_id = eval(self.data["srvc_inst_id"])
		msi = self.session["MegaServiceInstance"][srvc_inst_id]
		return msi["system_name"]

	def port(self):
		srvc_inst_id = eval(self.data["srvc_inst_id"])
		msi = self.session["MegaServiceInstance"][srvc_inst_id]
		return msi["port"]

	def notified(self):
		return {"1":"YES", "0":"NO"}.get(self.data["notify_flg"])

	def service(self):
		srvc_inst_id = eval(self.data["srvc_inst_id"])
		msi = self.session["MegaServiceInstance"][srvc_inst_id]
		return msi["srvc_type"]

	def session_cmd_id_link(self):
		a_href = HtmlElem("a")
		cmd_id = self.data["id"]
		return a_href(cmd_id, href="SessionCommand.%s.html" % cmd_id)

	def session_id(self):
		ses_id = self.data["session_id"]
		if self.class_name() == "Session":
			return ses_id
		else:
			a_href = HtmlElem("a")
			return a_href(ses_id, href="index.html")

	def accounts(self):
		return string.join(self.data["Account"])

	def default(self, name):
#		print self.class_name(), name
		val = self.data.get(name, "---")
		if val == None or val == "None": val = "---"
		return val

	def __getattr__(self, name):
		return lambda x = self, y = name: x.default(y)

class SessionCommand(WayObject):
	__table_info1 = [
		("Command ID"   , "session_cmd_id"),
		("Status"       , "status"),
		("Script"       , "script"),
		("Timeout type" , "timeout_type"),
		("Timeout time" , "timeout_dt"),
		("Notified?"    , "notified"),
		("Method"       , "method"),
		("Tag"          , "tag"),
		("Host"         , "host_link"),
		("Port"         , "port"),
		("Service"      , "service"),
		("Init time"    , "init_dt"),
		("Poke time"    , "poke_dt"),
		("Start time"   , "start_dt"),
		("End time"     , "end_dt"),
		("File"         , "module"),
		("Line"         , "step"),
		("Session"      , "session_id"),
		("Params"       , "params"),
		("Results"      , "results"),
	]
	__table_info2 = [
		("ID"      , "session_cmd_id_link"),
		("Host"    , "host"),
		("Port"    , "port"),
		("Method"  , "method"),
		("Tag"     , "tag"),
		("Status"  , "status"),
		("Timeout?", "timeout_type"),
		("Created" , "init_dt"),
		("Finished", "end_dt"),
	]
	def __init__(self, session_command, session = None):
		self.data = session_command
		self.session = session

	def emit(self):
		sc = self.data
		session_cmd_id = sc["session_cmd_id"]
		table = Table(border=1)
		for k,v in self.__table_info1:
			if v in ["params","results"]:
				inner_table = apply(getattr(self, v))
				rowspan = len(inner_table)
				if not rowspan:
					table.append(Tr(Td(k), Td("---", colspan = 2)))
					continue
				table.append(
					Tr(
						Td(k, rowspan = rowspan),
						inner_table[0][0],
						inner_table[0][1],
					)
				)
				table.extend(inner_table.data[1:])
			else:
				table.append(
					Tr(
						Td(k),
						Td(apply(getattr(self, v)), colspan = 2 ),
					)
				)
		h1 = HtmlElem("h1")
		h2 = HtmlElem("h2")
		hr = HtmlElem("hr")
		title = "Command ID %s Details" % sc["session_cmd_id"]
		page = HtmlPage(title = title, style = css())
		page.append(h1("The Way It Was"))
		page.append(hr())
		page.append(h2("Command ID %s" % session_cmd_id))
		page.append(table)
		page.write("SessionCommand.%s.html" % (session_cmd_id))
		
		row = Tr()
		for k, v in self.__table_info2:
			row.append(Td(apply(getattr(self, v))))

		return row

	def header_row(self):
		row = Tr()
		for k, v in self.__table_info2:
			row.append(Td(k))
		return row

class Session(WayObject):
	__table_info = [
		("Session ID"  , "session_id"),
		("Status"      , "status"),
		("Script"      , "script"),
		("Username"    , "SecurityUser"),
		("Initiator"   , "host_name"),
		("Accounts"    , "accounts"),
		("Sched time"  , "sched_dt"),
		("Start time"  , "start_dt"),
		("End time"    , "end_dt"),
		("Agent name"  , "agent_name"),
		("Owner name"  , "owner_name"),
		("Description" , "session_desc"),
		("Params"      , "params"),
		("Results"     , "results"),
	]

	def __init__(self, session):
		self.data = session

	def emit(self):
		session = self.data
		session_id = session["session_id"]
		session_dir = string.split(str(session_id), 'L')[0]
		mkdir(session_dir)
		os.chdir(session_dir)

		# main table
		main_table = Table(border=1)
		for k,v in self.__table_info:
			if v in ["params","results"]:
				inner_table = apply(getattr(self, v))
				rowspan = len(inner_table)
				if not rowspan:
					main_table.append(Tr(Td(k), Td("---", colspan = 2)))
					continue
				main_table.append(
					Tr(
						Td(k, rowspan = rowspan),
						inner_table[0][0],
						inner_table[0][1],
					)
				)
				main_table.extend(inner_table.data[1:])
			else:
				main_table.append(
					Tr(
						Td(k),
						Td(apply(getattr(self, v)), colspan = 2 ),
					)
				)
		# commands table
		command_table = Table(border=1)
		command_ids = session["SessionCommand"].keys()
		command_ids.sort()
		header_row = SessionCommand(None).header_row()
		command_table.append(Tr(Td(
			"%s Commands - [using data from truth]" % len(command_ids), 
			colspan = len(header_row),
			align = "center",
		)))
		command_table.append(header_row)
		for command_id in command_ids:
			sc = SessionCommand(session["SessionCommand"][command_id], session)
			command_table.append(sc.emit())

		subsession_ids = session["SubSession"].keys()
		for ssid in subsession_ids:
			subsession = Session(session["SubSession"][ssid])
			subsession.emit()

		p = HtmlElem("p")
		h1 = HtmlElem("h1")
		h2 = HtmlElem("h2")
		hr = HtmlElem("hr")
		title = "Session ID %s Details" % session_id
		page = HtmlPage(title = title, style = css())
		page.append(h1("The Way It Was"))
		page.append(hr())
		page.append(h2("Session ID %s" % session_id))
		page.append(p(main_table))
		page.append(hr())
		page.append(p(command_table))
		page.write("index.html")
		os.chdir("..")

def main(args):
	for filename in args:
		f = open(filename)
		session = Session(pickle.load(f))
		session.emit()
		f.close()
	
if __name__ == "__main__": main(sys.argv[1:])
