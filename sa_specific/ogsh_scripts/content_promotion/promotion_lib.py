import re
import time

# looks for the "Promotion level: blah" line in the description of the folder
# If it finds it, it replaces the value with the environment name passed in
# If it doesn't find it, it will append this line to the end of the description
def updateDesc(fldr, env):
	promo_str = "Promotion level: "
	promo_regex = re.compile(promo_str + "(.*)")
	desc = fldr.getDescription()

	if not promo_regex.search(desc):
		# doesn't yet have a promotion level, we'll append this as the last line
		# in the desc
		desc = desc + "\n\n" + promo_str + env
	else:
		# has a promotion level line, we'll just substitute it for the new level
		desc = promo_regex.sub(promo_str + env, desc)

	fldr.setDescription(desc)

# adds some notes to the desc
def addNotes(fldr, notes, promodemo, env):
	desc = fldr.getDescription()
	desc = desc + "\n----------------------------------\n" 
	desc = desc + "Notes from %s of folder to %s on %s:\n" % (promodemo, env, time.ctime(time.time()))
	desc = desc + notes
	
	fldr.setDescription(desc)

