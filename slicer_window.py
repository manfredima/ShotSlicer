#coding: utf-8

from pymel.core import *
from .mayaShotSlicer import getShots, launch
from pprint import pprint

shot_list = []
shot_list_d = dict()
shots_mute = []
shot_selected = []


# for dialog window
def rgbTo(r, g, b):
	conv = []
	for e in [r, g, b]:
		v = float(e)/float(255)
		conv.append(v)
	return conv


def getCheckboxValue(value):
	global shot_selected

	print 'VALUE:', value

	if value[1]:
		shot_selected.append(value[0])
	else:
		shot_selected.remove(value[0])

	print 'SS:', shot_selected


# build dialog window
def selectDialog():

	if window('cgf_shots_dialog', q=1, ex=1):
		deleteUI('cgf_shot_dialog')

	wd = window('cgf_shot_dialog', title='Slice Shot select')

	with wd:
		with verticalLayout():
			with horizontalLayout():
				# backgroundColor=(rgbTo(111,6,0))
				text( label='on | off', align='left' )
				separator(height=10, style='single')
				text( label='SHOT NAME', align='left' )
				separator(height=10, style='single')
				text( label='TIME RANGE', align='left' )
				separator(height=10, style='single')
				text( label='MUTE', align='center' )

			separator(height=10, style='double')

			for sn in shot_list_d:
				global shot_selected

				muted = 'NO'
				time_range = "%03d" % (shot_list_d[sn][0]) + ' — ' "%03d" % (shot_list_d[sn][1])
				try:
					if sn in shots_mute:
						muted = 'YES'

					with horizontalLayout():
						#backgroundColor=(rgbTo(111,6,0))
						checkBox( label='', value=True, annotation='Check ' + sn + ' for slice',
							 onCommand=Callback(getCheckboxValue, [sn, 1]),
							offCommand=Callback(getCheckboxValue, [sn, 0]))
						separator(height=10, style='single')
						text( label=sn, align='left', annotation='' )
						separator(height=10, style='single')
						text(label=time_range, align='left', annotation='')
						separator(height=10, style='single')
						text( label=muted, align='center', annotation='' )
				except:
					continue

			separator(height=10, style='double')

			button(label='SLICE SELECTED', backgroundColor=(rgbTo(111, 6, 0)), command=Callback(confirmSelect))
			# btn_confirm = button(label='Import selected')
			# btn_confirm.setCommand(Callback(confirmImport, confirm_set))
			helpLine()


def confirmSelect():
	#pprint(shot_selected, indent=4)

	if window('cgf_shots_dialog', q=1, ex=1):
		deleteUI('cgf_shot_dialog')

	launch(shot_selected)


def run():
	global shot_list_d, shots_mute, shot_selected

	if sceneName():
		getShots()
		from .mayaShotSlicer import shot_list_dict

		shot_list_d = shot_list_dict
		#print 'WINDOW:', shot_list_d

		if not shot_selected:
			shot_list = shot_list_dict.keys()
			shot_selected = shot_list

		selectDialog()

	else:
		system.displayWarning('Maya scene not found')