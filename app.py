import pandas as pd
import plotly.express as px

import os

import dash
import dash_table
import numpy as np


import datetime
from datetime import datetime as dt
from datetime import date, timedelta

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import re

import base64
import datetime
import io

import random

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import xlrd
import json

from github import Github
from github import InputGitTreeElement

from dash import no_update

import pandas as pd
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css'],suppress_callback_exceptions=True)
server = app.server


UPLOAD_DIRECTORY = "app_uploaded_files"
LOCAL_DATA = "local_data"


global update_i

update_i=0

def upload_file_git(file_path):

	global update_i

	user = "CryKun-Sudo"
	password = "Mmaladie123!!!"
	g = Github(user,password)
	repo = g.get_user().get_repo('Supply_rachida')

	file_list = [

	file_path

	]

	file_names = [
	   
	   file_path
	]

	commit_message = 'python update %s'%update_i
	master_ref = repo.get_git_ref('heads/master')
	master_sha = master_ref.object.sha
	base_tree = repo.get_git_tree(master_sha)
	element_list = list()
	for i, entry in enumerate(file_list):
	    with open(entry) as input_file:
	        data = input_file.read()
	    if entry.endswith('.png'):
	        data = base64.b64encode(data)
	    element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
	    element_list.append(element)
	tree = repo.create_git_tree(element_list, base_tree)
	parent = repo.get_git_commit(master_sha)
	commit = repo.create_git_commit(commit_message, tree, [parent])
	master_ref.edit(commit.sha)

	update_i+=1


def list_file_git(path):


	user = "CryKun-Sudo"
	password = "Mmaladie123!!!"
	g = Github(user,password)
	repo = g.get_user().get_repo('Supply_rachida')

	contents = repo.get_contents(path)

	list_files = []

	for con in contents:
		list_files.append(con.name)

	return list_files

if not os.path.exists(UPLOAD_DIRECTORY):
	os.makedirs(UPLOAD_DIRECTORY)

def replace_typeform(element):
	element = element.strip(' ').lower()
	if element=="forma":
		element = "FORM A"
	elif element == "formcm":
		element = "FORM CM"
	else:
		element = element.upper()

	return element

def replace_diametre(element):
	element = element.strip(' ')
	element = element.replace(',','.')
	return element

global reference

reference = pd.read_csv(os.path.join(LOCAL_DATA,"reference.csv"))

reference.loc[reference.Diametre=="105","Diametre"] = "10.5"

reference["Artikel"] = reference["Artikel"].astype(str)

reference["Type/Form"] = list(reference["Type/Form"].map(replace_typeform))

reference["Diametre"] = list(reference["Diametre"].map(replace_diametre))

global reference_ffr

reference_ffr = pd.read_csv(os.path.join(LOCAL_DATA,"Reference_ffr.csv"))

reference_ffr["Artikel"] = reference_ffr["Artikel"].astype(str)

reference_ffr["Type/Form"] = list(reference_ffr["Type/Form"].astype(str).map(replace_typeform))

reference_ffr["Diametre"] = list(reference_ffr["Diametre"].astype(str).map(replace_diametre))

global df_table1

try:
	df_table1 = pd.read_csv(os.path.join(LOCAL_DATA,"sheet1.csv"))
	df_table1["Artikel"] = df_table1["Artikel"].astype(str)
except Exception:
	df_table1 = pd.DataFrame()





df = pd.DataFrame()

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
	'position': 'fixed',
	'top': 0,
	'left': 0,
	'bottom': 0,
	'width': '20%',
	'padding': '20px 10px',
	'background-color': '#f8f9fa',
	'overflow': 'auto',
}

# the style arguments for the main content page.
CONTENT_STYLE = {
	'margin-left': '25%',
	'margin-right': '5%',
	'top': 0,
	'padding': '20px 10px'
}

TEXT_STYLE = {
	'textAlign': 'center',
	'color': '#191970'
}

CARD_TEXT_STYLE = {
	'textAlign': 'center',
	'color': '#0074D9'
}






controls = dbc.FormGroup(
	[
		html.H3('FDC', style={
			'textAlign': 'center', 'color':'Red'
		}),
		html.Hr(),
		html.P('Artikel', style={
			'textAlign': 'center'
		}),
		dcc.Dropdown(
			id='dropdown',
			options=[
			],
			value=[],  # default value
			multi=True,
		),
		dcc.RadioItems(
			id="Artikel_Selector",
			options=[
				{"label": "All ", "value": "all"},
				{"label": "Selected ", "value": "selected"},
			],
			value="all",
			labelStyle={"display": "inline-block"},style={'textAlign': 'center'}
		),
		html.Hr(),
		html.P('Farbe', style={
			'textAlign': 'center'
		}),
		dcc.Dropdown(
			id='dropdown_farbe',
			options=[
			],
			value=[],  # default value
			multi=True,
		),
		dcc.RadioItems(
			id="Farbe_Selector",
			options=[
				{"label": "All ", "value": "all"},
				{"label": "Selected ", "value": "selected"},
			],
			value="all",
			labelStyle={"display": "inline-block"},style={'textAlign': 'center'}
		),
		html.Hr(),
		html.P('Größe', style={
			'textAlign': 'center'
		}),
		dcc.Dropdown(
			id='dropdown_Größe',
			options=[
			],
			value=[],  # default value
			multi=True,
		),
		dcc.RadioItems(
			id="Größe_Selector",
			options=[
				{"label": "All ", "value": "all"},
				{"label": "Selected ", "value": "selected"},
			],
			value="all",
			labelStyle={"display": "inline-block"},style={'textAlign': 'center'}
		),
		html.Hr(),
		html.H3('FFR', style={
			'textAlign': 'center', 'color':'Red'
		}),
		html.P('Artikel', style={
			'textAlign': 'center'
		}),
		dcc.Dropdown(
			id='dropdown_artikel_ffr',
			options=[
			],
			value=[],  # default value
			multi=True,
		),
		dcc.RadioItems(
			id="Artikel_Selector_ffr",
			options=[
				{"label": "All ", "value": "all"},
				{"label": "Selected ", "value": "selected"},
			],
			value="all",
			labelStyle={"display": "inline-block"},style={'textAlign': 'center'}
		),
		html.Hr(),
		html.P('Farbe', style={
			'textAlign': 'center'
		}),
		dcc.Dropdown(
			id='dropdown_farbe_ffr',
			options=[
			],
			value=[],  # default value
			multi=True,
		),
		dcc.RadioItems(
			id="Farbe_Selector_ffr",
			options=[
				{"label": "All ", "value": "all"},
				{"label": "Selected ", "value": "selected"},
			],
			value="all",
			labelStyle={"display": "inline-block"},style={'textAlign': 'center'}
		),
		html.Hr(),
		html.P('Größe', style={
			'textAlign': 'center'
		}),
		dcc.Dropdown(
			id='dropdown_Größe_ffr',
			options=[
			],
			value=[],  # default value
			multi=True,
		),
		dcc.RadioItems(
			id="Größe_Selector_ffr",
			options=[
				{"label": "All ", "value": "all"},
				{"label": "Selected ", "value": "selected"},
			],
			value="all",
			labelStyle={"display": "inline-block"},style={'textAlign': 'center'}
		),
		html.Hr(),
	]
)




sidebar = html.Div(
	[
		html.H2('Parameters', style=TEXT_STYLE),
		html.Hr(),
		controls
	],
	style=SIDEBAR_STYLE,
)



content_before_first_row = dbc.Row([

	dbc.Col(
		dbc.Card(

	html.Div([
	dcc.Upload(
		id='upload-data',
		children=html.Div([
			'Drag and Drop or ',
			html.A('Select Files')
		]),
		style={
			'width': '100%',
			'height': '60px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center',
			'margin': '10px'
		},
		# Allow multiple files to be uploaded
		multiple=True
	),
	html.Div(id='output-data-upload',style=CARD_TEXT_STYLE),
])
))
])

content_table_1 = dbc.Row([

	dbc.Col(
		dbc.Card(

			dash_table.DataTable(id='table1',
								 data=df.to_dict('records'),
								 columns = [{'id': c, 'name': c} for c in df.columns],
								 editable=False,
								filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)'
															}
														],
								style_header={
													'backgroundColor': 'rgb(230, 230, 230)',
													'fontWeight': 'bold'
											}
														)

			))




	])




content_first_row = dbc.Row([
	dbc.Col(
		dbc.Card(
			[

				dbc.CardBody(
					[
						html.H4(id='card_title_1', children=['Artikel'], className='card-title',
								style=CARD_TEXT_STYLE),
						html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
					]
				)
			]
		),
		md=3
	),
	dbc.Col(
		dbc.Card(
			[

				dbc.CardBody(
					[
						html.H4('Menge', className='card-title', style=CARD_TEXT_STYLE),
						html.P(id='card_text_2', children=['Sample text.'], style=CARD_TEXT_STYLE),
					]
				),
			]

		),
		md=3
	),
	dbc.Col(
		dbc.Card(
			[
				dbc.CardBody(
					[
						html.H4('Farbe', className='card-title', style=CARD_TEXT_STYLE),
						html.P(id='card_text_3', children=['Sample text.'], style=CARD_TEXT_STYLE),
					]
				),
			]

		),
		md=3
	),
	dbc.Col(
		dbc.Card(
			[
				dbc.CardBody(
					[
						html.H4('Größe', className='card-title', style=CARD_TEXT_STYLE),
						html.P(id='card_text_4', children=['Sample text.'], style=CARD_TEXT_STYLE),
					]
				),
			]
		),
		md=3
	)
])



content_second_row = dbc.Row(
	[
		dbc.Col(
			dcc.Graph(id='graph_1',figure={}), md=12
		),
		dbc.Col(
			dbc.Card([
				html.H4("REF' FDC", className="card-title",style=TEXT_STYLE),
				dash_table.DataTable(id='table2',
								 data=df.to_dict('records'),
								 columns = [{'id': c, 'name': c,'deletable':False,'renamable':False} for c in df.columns],
								 editable=False,
								filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								# export_format='xlsx',
							 #    export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)'
															}
														],
								style_header={
													'backgroundColor': 'rgb(230, 230, 230)',
													'fontWeight': 'bold'
											}
														),

				html.Div([

					dcc.ConfirmDialog(
										id='confirm_add',
										message='Message Here !',
									),
					dcc.ConfirmDialog(
										id='confirm_mod',
										message='Message Here !',
									),
					dcc.ConfirmDialog(
										id='confirm_del',
										message='Message Here !',
									),

					html.Div(id='output-confirm'),
					html.Div(id='output-confirm_mod'),
					html.Div(id='output-confirm_del'),

					dbc.Row([

											
						dbc.Col(
							dbc.FormGroup(
								[
									dbc.Label("Artikel", html_for="example-artikel-grid"),
									dbc.Input(
										type="text",
										id="example-artikel-grid",
										placeholder="Artikel...",
									),
								]
							),
							width=3,
						),
						dbc.Col(
							dbc.FormGroup(
								[
									dbc.Label("Type/Form", html_for="example-typeform-grid"),
									dbc.Input(
										type="text",
										id="example-typeform-grid",
										placeholder="Type/Form...",
									),
								]
							),
							width=3,
						),

						dbc.Col(
							dbc.FormGroup(
								[
									dbc.Label("Diametre", html_for="example-Diametre-grid"),
									dbc.Input(
										type="text",
										id="example-Diametre-grid",
										placeholder="Diametre...",
									),
								]
							),
							width=3,
						),

						dbc.Col(
							dbc.FormGroup(

								[
									dbc.Row([html.Div(dbc.Button("Add", color="primary",id="submit_form",size="sm"),style={'margin-top':20,'padding-left':20}),
											  html.Div(dbc.Button("Mod", color="warning",id="submit_form_mod",size="sm"),style={'margin-top':20,'padding-left':5}),
											  html.Div(dbc.Button("Del", color="danger",id="submit_form_del",size="sm"),style={'margin-top':20,'padding-left':5})]),
									
							
								]
							),
							width=3,
						),

					],
					form=True,)


			

					
					],style=CARD_TEXT_STYLE),


				

						

				]),


		),
		dbc.Col(


				dbc.Card([

				html.H4("FDC", className="card-title",style=TEXT_STYLE),

				dash_table.DataTable(id='table3',
								 data=df.to_dict('records'),
								 columns = [],
								 #editable=True,
								filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								# export_format='xlsx',
							 #    export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)',
																'if': {'column_editable': True},
																'backgroundColor': 'rgb(119,136,153)',
																'color':'white',
																'fontWeight': 'bold',
																
															
															}
														],
								style_header={		
													'fontWeight': 'bold',						
													'backgroundColor': 'rgb(230, 230, 230)',													
													
											}
														),
				
				html.Div(id='output_save_fdc',style=CARD_TEXT_STYLE),				
				dbc.Card([dbc.CardBody(html.Div(dbc.Button("Save", color="primary",id="save_stuf",size="lg"),style=CARD_TEXT_STYLE),),]),
				html.Div(id='intermediate-data', style={'display': 'none'}),
				html.Div(id='intermediate-data-2', style={'display': 'none'}),

						

				]),
			
		)
	]
)


content_third_row = dbc.Row(
	[
		dbc.Col(
					dbc.Col(
			dbc.Card([
				dash_table.DataTable(id='table4',
								 data=df.to_dict('records'),
								 columns = [{'id': c, 'name': c,'deletable':False,'renamable':True} for c in df.columns],
								 editable=False,
								#filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								export_format='xlsx',
								export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)'
															}
														],
								style_header={
													'backgroundColor': 'rgb(230, 230, 230)',
													'fontWeight': 'bold'
											}
														),

						

				]),


		),
		)
	]
)



content_fourth_row = dbc.Row(
	[
		dbc.Col(
			dcc.Graph(id='graph_5',figure={}), md=6
		),
		dbc.Col(
			dcc.Graph(id='graph_6',figure={}), md=6
		)
	]
)

content_fifth_row = dbc.Row(
	[
		
		dbc.Col(
			dbc.Card([
				html.H4("REF' FFR", className="card-title",style=TEXT_STYLE),
				dash_table.DataTable(id='table5',
								 data=reference_ffr.to_dict('records'),
								 columns = [{'id': c, 'name': c,'deletable':False,'renamable':False} for c in reference_ffr.columns],
								 editable=False,
								filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								# export_format='xlsx',
							 #    export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in reference_ffr.columns		
														],
								style_data_conditional=[
															{
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)'
															}
														],
								style_header={
													'backgroundColor': 'rgb(230, 230, 230)',
													'fontWeight': 'bold'
											}
														),

				html.Div([

					dcc.ConfirmDialog(
										id='confirm_add_ffr',
										message='Message Here !',
									),
					dcc.ConfirmDialog(
										id='confirm_mod_ffr',
										message='Message Here !',
									),
					dcc.ConfirmDialog(
										id='confirm_del_ffr',
										message='Message Here !',
									),

					html.Div(id='output-confirm_ffr'),
					html.Div(id='output-confirm_mod_ffr'),
					html.Div(id='output-confirm_del_ffr'),

					dbc.Row([

											
						dbc.Col(
							dbc.FormGroup(
								[
									dbc.Label("Artikel", html_for="example-artikel-grid_ffr"),
									dbc.Input(
										type="text",
										id="example-artikel-grid_ffr",
										placeholder="Artikel...",
									),
								]
							),
							width=3,
						),
						dbc.Col(
							dbc.FormGroup(
								[
									dbc.Label("Type/Form", html_for="example-typeform-grid_ffr"),
									dbc.Input(
										type="text",
										id="example-typeform-grid_ffr",
										placeholder="Type/Form...",
									),
								]
							),
							width=3,
						),

						dbc.Col(
							dbc.FormGroup(
								[
									dbc.Label("Diametre", html_for="example-Diametre-grid_ffr"),
									dbc.Input(
										type="text",
										id="example-Diametre-grid_ffr",
										placeholder="Diametre...",
									),
								]
							),
							width=3,
						),

						dbc.Col(
							dbc.FormGroup(

								[
									dbc.Row([html.Div(dbc.Button("Add", color="primary",id="submit_form_ffr",size="sm"),style={'margin-top':20,'padding-left':20}),
											  html.Div(dbc.Button("Mod", color="warning",id="submit_form_mod_ffr",size="sm"),style={'margin-top':20,'padding-left':5}),
											  html.Div(dbc.Button("Del", color="danger",id="submit_form_del_ffr",size="sm"),style={'margin-top':20,'padding-left':5})]),
									
							
								]
							),
							width=3,
						),

					],
					form=True,)


			

					
					],style=CARD_TEXT_STYLE),


				

						

				]),


		),
		dbc.Col(


				dbc.Card([

				html.H4("FFR", className="card-title",style=TEXT_STYLE),

				dash_table.DataTable(id='table6',
								 data=df.to_dict('records'),
								 columns = [],
								 #editable=True,
								filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								# export_format='xlsx',
							 #    export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)',
																'if': {'column_editable': True},
																'backgroundColor': 'rgb(119,136,153)',
																'color':'white',
																'fontWeight': 'bold',
																
															
															}
														],
								style_header={		
													'fontWeight': 'bold',						
													'backgroundColor': 'rgb(230, 230, 230)',													
													
											}
														),

				html.Div(id='output_save_ffr',style=CARD_TEXT_STYLE),	
				dbc.Card([dbc.CardBody(html.Div(dbc.Button("Save", color="primary",id="save_stuf_ffr",size="lg"),style=CARD_TEXT_STYLE),),]),
				# html.Div(id='intermediate-data_ffr', style={'display': 'none'}),
				# html.Div(id='intermediate-data-2_ffr', style={'display': 'none'}),

						

				]),
			
		)
	]
)


content_sixth_row = dbc.Row(
	[
		dbc.Col(
					dbc.Col(
			dbc.Card([
				dash_table.DataTable(id='table7',
								 data=df.to_dict('records'),
								 columns = [{'id': c, 'name': c,'deletable':False,'renamable':True} for c in df.columns],
								 editable=False,
								#filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								export_format='xlsx',
								export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)'
															}
														],
								style_header={
													'backgroundColor': 'rgb(230, 230, 230)',
													'fontWeight': 'bold'
											}
														),

						

				]),


		),
		)
	]
)

content_seventh_row = dbc.Row(
	[
		dbc.Col(
			dcc.Graph(id='graph_8',figure={}), md=6
		),
		dbc.Col(
			dcc.Graph(id='graph_9',figure={}), md=6
		)
	]
)

content_eighth_row = dbc.Row(
	[
		dbc.Col(
			dcc.Graph(id='graph_10',figure={}), md=6
		),
		dbc.Col(
			dcc.Graph(id='graph_11',figure={}), md=6
		)
	]
)


content_before_eighth_row = dbc.Row(
	[
		dbc.Col(
					dbc.Col(
			dbc.Card([
				dash_table.DataTable(id='table8',
								 data=df.to_dict('records'),
								 columns = [{'id': c, 'name': c,'deletable':False,'renamable':True} for c in df.columns],
								 editable=False,
								#filter_action="native",
								sort_action="native",
								sort_mode="multi",
								row_selectable=False,
								row_deletable=False,
								selected_rows=[],
								page_action="native",
								page_current= 0,
								page_size= 10,
								export_format='xlsx',
								export_headers='display',
								merge_duplicate_headers=True,
								style_cell_conditional=[
															{
																'if': {'column_id': c},
																'textAlign': 'center'
															} for c in df.columns		
														],
								style_data_conditional=[
															{
																'if': {'row_index': 'odd'},
																'backgroundColor': 'rgb(248, 248, 248)'
															}
														],
								style_header={
													'backgroundColor': 'rgb(230, 230, 230)',
													'fontWeight': 'bold'
											}
														),

						

				]),


		),
		)
	]
)



content = html.Div(
	[
		html.H2('Analytics Dashboard Template', style=TEXT_STYLE),
		html.Hr(),
		html.H5('Import File'),
		content_before_first_row,
		html.Br(),
		content_table_1,
		html.Hr(),
		content_first_row,
		html.Hr(),
		content_second_row,
		html.Hr(),
		content_third_row,
		content_fourth_row,
		content_fifth_row,
		content_sixth_row,
		content_seventh_row,
		content_before_eighth_row,
		content_eighth_row,
	],
	style=CONTENT_STYLE
)

app.layout = html.Div([sidebar, content])



def parse_contents(contents, filename):
	content_type, content_string = contents.split(',')

	data = contents.encode("utf8").split(b";base64,")[1]
	
	with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
		fp.write(base64.decodebytes(data))

	decoded = base64.b64decode(content_string)
	try:
		if 'csv' in filename:
			# Assume that the user uploaded a CSV file
			df = pd.read_csv(
				io.StringIO(decoded.decode('utf-8')))
		elif 'xls' in filename:
			# Assume that the user uploaded an excel file
			df = pd.read_excel(io.BytesIO(decoded))
	except Exception as e:
		print(e)
		return html.Div([
			'There was an error processing this file.'
		])

	return html.H5(filename)  
   

def prepare_xls(xls_file_path):

	global update_i

	xls = xlrd.open_workbook(r'%s'%(xls_file_path), on_demand=True)
	sheet_list = xls.sheet_names()

	sheets = []

	for x in sheet_list:
		sheets.append(pd.read_excel(xls_file_path,sheet_name=x))

	sheet1 = sheets[0]

	sheet1 = sheet1[["Packung","Artikel","Farbe","Größe","Menge"]]
	sheet1 = sheet1.fillna(0)
	for col in sheet1.columns:
		sheet1[col] = pd.to_numeric(sheet1[col],errors="coerce")
		
	nan_rows_index = sheet1[np.isnan(sheet1["Artikel"])].index

	sheet1 = sheet1.drop(nan_rows_index,axis=0).reset_index(drop=True)
	for col in sheet1.columns:
		sheet1[col] = sheet1[col].astype(int)
	sheet1.to_csv(os.path.join(LOCAL_DATA,"sheet1.csv"),index=False,encoding="utf-8")

	upload_file_git("local_data/sheet1.csv")

	return sheet1


def prepare_lists_artikels_farbes_grobe(dff):

	artikels = list(dff["Artikel"].unique())

	artikels.sort()

	farbes = list(dff["Farbe"].unique())

	farbes.sort()

	grobes = list(dff["Größe"].unique())

	grobes.sort()

	farbe_options = [{"label": str(k), "value": str(k)} for k in farbes]

	artikel_options = [{"label": str(k), "value": str(k)} for k in artikels]

	grobe_options = [{"label": str(k), "value": str(k)} for k in grobes]

	return [farbe_options,artikel_options,grobe_options]


@app.callback([Output('output-data-upload', 'children'),Output('table1','data'),Output('table1','columns'),Output('card_text_1','children'),Output('card_text_2','children'),Output('graph_1',"figure"),Output('dropdown','options'),Output("dropdown_farbe","options"),Output("dropdown_Größe","options"),Output('card_text_3','children'),Output('card_text_4','children'),Output('dropdown_artikel_ffr','options'),Output("dropdown_farbe_ffr","options"),Output("dropdown_Größe_ffr","options")],
			  [Input('upload-data', 'contents'),Input('Artikel_Selector',"value"),Input("Farbe_Selector","value"),Input("Größe_Selector","value"),Input('dropdown','value'),Input("dropdown_farbe","value"),Input('dropdown_Größe','value')],
			  [State('upload-data', 'filename')])
def update_output(list_of_contents, artikel_selector,farbe_selector, grobe_selector,artikel_values, farbe_values, grobe_values,list_of_names):
	if list_of_contents is not None:
		children = [
			parse_contents(c, n) for c, n in
			zip(list_of_contents, list_of_names)]

		if "xls" in list_of_names[0]:

			dff = prepare_xls(os.path.join(UPLOAD_DIRECTORY,list_of_names[0]))


			farbe_options,artikel_options,grobe_options = prepare_lists_artikels_farbes_grobe(dff)

			if artikel_selector == "selected":
				if artikel_values != []:
					dff = dff[dff.Artikel.isin(artikel_values)]


			if farbe_selector == "selected":
				if farbe_values != []:
					dff = dff[dff.Farbe.isin(farbe_values)]

			if grobe_selector == "selected":
				if grobe_values != []:
					dff = dff[dff.Größe.isin(grobe_values)]

			summe_artikel = len(dff["Artikel"].unique())

			summe_menge = dff["Menge"].sum()

			summe_farbe = len(dff["Farbe"].unique())

			summe_gorbe = len(dff["Größe"].unique())


			check = dff.groupby(["Artikel","Farbe"]).sum()["Menge"].reset_index()

			fig1 = px.bar(check,x="Artikel",y="Menge",color="Farbe",barmode="group",hover_name="Menge",title="Menge Pro Artikel")
			fig1 = fig1.update_layout(xaxis_type='category')

			dff["Artikel"] = dff["Artikel"].astype(str)

		return children,dff.to_dict('records'),[{'id': c, 'name': c} for c in dff.columns],summe_artikel,summe_menge,fig1,artikel_options,farbe_options,grobe_options,summe_farbe,summe_gorbe,artikel_options,farbe_options,grobe_options
		# ,sheet2.to_dict('records'),columns_table3
	else:

		dff = df_table1

		farbe_options,artikel_options,grobe_options = prepare_lists_artikels_farbes_grobe(dff)

		if artikel_selector == "selected":
			if artikel_values != []:
				dff = dff[dff.Artikel.isin(artikel_values)]


		if farbe_selector == "selected":
			if farbe_values != []:
				dff = dff[dff.Farbe.isin(farbe_values)]

		if grobe_selector == "selected":
			if grobe_values != []:
				dff = dff[dff.Größe.isin(grobe_values)]

		summe_artikel = len(dff["Artikel"].unique())

		summe_menge = dff["Menge"].sum()

		summe_farbe = len(dff["Farbe"].unique())

		summe_gorbe = len(dff["Größe"].unique())


		check = dff.groupby(["Artikel","Farbe"]).sum()["Menge"].reset_index()

		fig1 = px.bar(check,x="Artikel",y="Menge",color="Farbe",barmode="group",hover_name="Menge",title="Menge Pro Artikel")
		fig1 = fig1.update_layout(xaxis_type='category')

		return "Loaded Saved Sheet1.csv",dff.to_dict('records'),[{'id': c, 'name': c} for c in dff.columns],summe_artikel,summe_menge,fig1,artikel_options,farbe_options,grobe_options,summe_farbe,summe_gorbe,artikel_options,farbe_options,grobe_options
		# ,None,[]


#State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')
@app.callback([Output('table2','data'),Output('table2','columns')],
			  [Input('Artikel_Selector',"value"),Input('dropdown','value'),Input('output-confirm', 'children'),Input('output-confirm_mod','children'),Input('output-confirm_del','children')],
			  )
def filter_table2(artikel_selector,artikel_values,children,children_mod,children_del):
	
	global reference

	
# 	if artikel_selector == "selected":
# 		artikels = artikel_values
# 	else:
# 		artikels = reference["Artikel"].unique()

# 	dff = reference[reference.Artikel.isin(artikels)]

	columns = [{'id': c, 'name': c} for c in reference.columns]

	return reference.to_dict('records'),columns




@app.callback([Output('table3','data'),Output('table3','columns')],
			  [Input('table1','data'),Input('table1','columns'),Input('output-data-upload', 'children'),Input('output-confirm', 'children'),Input('output-confirm_mod','children'),Input('output-confirm_del','children'),Input('table2','data')],
			  )
def filter_table3(data,column,children_upload,children_add,children_mod,children_del,data_table2):

	global reference

	if ((data!=None) and (children_upload=="Loaded Saved Sheet1.csv") and ("sheet2.csv" not in os.listdir(LOCAL_DATA))) or ((data!=None) and (children_upload!="Loaded Saved Sheet1.csv")):
			
		sheet1 = pd.DataFrame.from_dict(data=data)

		sheet1["Artikel"] = sheet1["Artikel"].astype(str)

		sheet2 = pd.DataFrame(columns=["Artikel","Stuf03","Stuf11","Stuf12","Menge"])

		sheet2["Artikel"] = sheet1.groupby(["Artikel"]).sum()["Menge"].index
		sheet2["Menge"] = sheet1.groupby(["Artikel"]).sum()["Menge"].values


		dff = reference

		sheet2 = pd.merge(sheet2,dff, on='Artikel')

		sheet2["Stuf03"] = 0
		sheet2["Stuf11"] = 0
		sheet2["Stuf12"] = 0


		columns = []

		for c in sheet2.columns:
			if "stuf" in c.lower():
				columns.append({'id':c,'name':c,'editable':True})
			else:
				columns.append({'id':c,'name':c,'editable':False})
				
		

		#columns = [{'id': c, 'name': c} for c in sheet2.columns]

		return sheet2.to_dict('records'),columns

	elif (data!=None) and (children_upload=="Loaded Saved Sheet1.csv") and ("sheet2.csv" in os.listdir(LOCAL_DATA)) :

		sheet1 = pd.DataFrame.from_dict(data=data)

		sheet2 = pd.read_csv(os.path.join(LOCAL_DATA,"sheet2.csv"))

		sheet2["Artikel"] = sheet2["Artikel"].astype(str)

		dff = reference

		dff["Artikel"] = dff["Artikel"].astype(str)

		if len(dff)>len(sheet2):

			row_ = dff[dff.Artikel.isin(sheet2.Artikel)==False].copy(deep=True)

			row_["Stuf03"] = 0
			row_["Stuf11"] = 0
			row_["Stuf12"] = 0

			try:
				row_["Menge"] = sheet1[sheet1.Artikel==row_.Artikel.values[0]]["Menge"].sum()
			except Exception:
				row_["Menge"] = 0

			row_ = row_[["Artikel","Stuf03","Stuf11","Stuf12","Menge","Type/Form","Diametre"]].reset_index(drop=True)

			sheet2 = pd.concat([sheet2,row_],ignore_index=True)

		else:
			
			sheet2 = sheet2[sheet2.Artikel.isin(dff.Artikel)==True].copy(deep=True)

			sheet2_ = pd.merge(sheet2,dff,on=["Artikel","Type/Form","Diametre"],how="right")[["Artikel","Stuf03","Stuf11","Stuf12","Menge","Type/Form","Diametre"]].fillna(0)

			sheet2_right = pd.merge(sheet2_,sheet2,on=["Artikel","Stuf03","Stuf11","Stuf12","Menge","Type/Form","Diametre"],how="right")

			sheet2_left = pd.merge(sheet2_,sheet2,on=["Artikel","Stuf03","Stuf11","Stuf12","Menge","Type/Form","Diametre"],how="left")

			sheet2_right["Type/Form"] = sheet2_left["Type/Form"]
			sheet2_right["Diametre"] = sheet2_left["Diametre"]

			sheet2 = sheet2_right

		sheet2.to_csv(os.path.join(LOCAL_DATA,"sheet2.csv"),index=False,encoding="utf-8")

		#upload_file_git("local_data/sheet2.csv")

		columns = []

		for c in sheet2.columns:
			if "stuf" in c.lower():
				columns.append({'id':c,'name':c,'editable':True})
			else:
				columns.append({'id':c,'name':c,'editable':False})

		return sheet2.to_dict('records'),columns

	else:

		return None,[]




@app.callback([Output('confirm_add', 'displayed'),Output('confirm_add','message')],
				[Input('submit_form','n_clicks')],
			  [State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')])
def display_confirm(submit_n_clicks,artikel_input,typeform_input,diametre_input):
	
	global reference

	if (submit_n_clicks) and (artikel_input!=None) and (typeform_input!=None) and (diametre_input!=None):

		if artikel_input != None:

			list_artikels = list(reference["Artikel"].unique())

			list_artikels = [str(x) for x in list_artikels]

			if (artikel_input in list_artikels):
				message = "Artikel = %s Exists in Reference"%artikel_input
				displayed = True
			else:
				message = "%s Doesn't Exists in Reference : Press Ok To Add."%artikel_input
				displayed = True

		return displayed,message

	else:
		
		return False,""

@app.callback([Output('confirm_mod', 'displayed'),Output('confirm_mod','message')],
				[Input('submit_form_mod','n_clicks')],
			  [State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')])
def display_confirm_mod(submit_n_clicks,artikel_input,typeform_input,diametre_input):
	
	global reference

	if (submit_n_clicks) and (artikel_input!=None) and (typeform_input!=None) and (diametre_input!=None):

		if artikel_input != None:

			list_artikels = list(reference["Artikel"].unique())

			list_artikels = [str(x) for x in list_artikels]

			if (artikel_input in list_artikels):
				message = "Artikel = %s Exists in Reference, Press Ok To Modify."%artikel_input
				displayed = True
			else:
				message = "%s Doesn't Exists in Reference."%artikel_input
				displayed = True

		return displayed,message

	else:
		
		return False,""

@app.callback([Output('confirm_del', 'displayed'),Output('confirm_del','message')],
				[Input('submit_form_del','n_clicks')],
			  [State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')])
def display_confirm_del(submit_n_clicks,artikel_input,typeform_input,diametre_input):
	
	global reference

	if (submit_n_clicks) and (artikel_input!=None) and (typeform_input!=None) and (diametre_input!=None):

		if artikel_input != None:

			list_artikels = list(reference["Artikel"].unique())

			list_artikels = [str(x) for x in list_artikels]

			if (artikel_input in list_artikels):
				message = "Artikel = %s Exists in Reference, Press Ok To Delete."%artikel_input
				displayed = True
			else:
				message = "%s Doesn't Exists in Reference."%artikel_input
				displayed = True

		return displayed,message

	else:
		
		return False,""


		##################

@app.callback([Output('confirm_add_ffr', 'displayed'),Output('confirm_add_ffr','message')],
				[Input('submit_form_ffr','n_clicks')],
			  [State('example-artikel-grid_ffr','value'),State('example-typeform-grid_ffr','value'),State('example-Diametre-grid_ffr','value')])
def display_confirm_ffr(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	if (submit_n_clicks) and (artikel_input!=None) and (typeform_input!=None) and (diametre_input!=None):

		if artikel_input != None:

			list_artikels = list(reference_ffr["Artikel"].unique())

			list_artikels = [str(x) for x in list_artikels]

			if (artikel_input in list_artikels):
				message = "Artikel = %s Exists in Reference"%artikel_input
				displayed = True
			else:
				message = "%s Doesn't Exists in Reference : Press Ok To Add."%artikel_input
				displayed = True

		return displayed,message

	else:
		
		return False,""

@app.callback([Output('confirm_mod_ffr', 'displayed'),Output('confirm_mod_ffr','message')],
				[Input('submit_form_mod_ffr','n_clicks')],
			  [State('example-artikel-grid_ffr','value'),State('example-typeform-grid_ffr','value'),State('example-Diametre-grid_ffr','value')])
def display_confirm_mod(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	if (submit_n_clicks) and (artikel_input!=None) and (typeform_input!=None) and (diametre_input!=None):

		if artikel_input != None:

			list_artikels = list(reference_ffr["Artikel"].unique())

			list_artikels = [str(x) for x in list_artikels]

			if (artikel_input in list_artikels):
				message = "Artikel = %s Exists in Reference, Press Ok To Modify."%artikel_input
				displayed = True
			else:
				message = "%s Doesn't Exists in Reference."%artikel_input
				displayed = True

		return displayed,message

	else:
		
		return False,""

@app.callback([Output('confirm_del_ffr', 'displayed'),Output('confirm_del_ffr','message')],
				[Input('submit_form_del_ffr','n_clicks')],
			  [State('example-artikel-grid_ffr','value'),State('example-typeform-grid_ffr','value'),State('example-Diametre-grid_ffr','value')])
def display_confirm_del(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	if (submit_n_clicks) and (artikel_input!=None) and (typeform_input!=None) and (diametre_input!=None):

		if artikel_input != None:

			list_artikels = list(reference_ffr["Artikel"].unique())

			list_artikels = [str(x) for x in list_artikels]

			if (artikel_input in list_artikels):
				message = "Artikel = %s Exists in Reference, Press Ok To Delete."%artikel_input
				displayed = True
			else:
				message = "%s Doesn't Exists in Reference."%artikel_input
				displayed = True

		return displayed,message

	else:
		
		return False,""

		############################""


@app.callback([Output('table5','data'),Output('table5','columns')],
			  [Input('Artikel_Selector_ffr',"value"),Input('dropdown_artikel_ffr','value'),Input('output-confirm_ffr', 'children'),Input('output-confirm_mod_ffr','children'),Input('output-confirm_del_ffr','children')],)
def filter_table2(artikel_selector,artikel_values,children,children_mod,children_del):



	if artikel_selector == "selected":
		artikels = artikel_values
	else:
		artikels = reference_ffr["Artikel"].unique()

	dff = reference_ffr[reference_ffr.Artikel.isin(artikels)]


	columns = [{'id': c, 'name': c} for c in dff.columns]

	return dff.to_dict('records'),columns		




####


@app.callback(Output('output-confirm', 'children'),
			  [Input('confirm_add', 'submit_n_clicks')],
			  [State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')])
def update_output(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	global reference

	if submit_n_clicks:

		list_artikels = list(reference["Artikel"].unique())

		list_artikels = [str(x) for x in list_artikels]

		if (artikel_input not in list_artikels):

		

			to_add = pd.DataFrame(columns=reference.columns.values,data=[[artikel_input,typeform_input,diametre_input]])

			reference = reference.append(to_add,ignore_index=True)

			#reference.to_csv(os.path.join(LOCAL_DATA,"reference.csv"),index=False,encoding="utf-8")

			#upload_file_git("local_data/reference.csv")

		

			return "%s - %s - %s Added to References."%(artikel_input,typeform_input,diametre_input)
		else:

			return "Not Added Because Artikel = %s Exists in References"%artikel_input
	else:

		return ""


@app.callback(Output('output-confirm_mod', 'children'),
			  [Input('confirm_mod', 'submit_n_clicks')],
			  [State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')])
def update_output_mod(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	global reference

	if submit_n_clicks:

		list_artikels = list(reference["Artikel"].unique())

		list_artikels = [str(x) for x in list_artikels]

		if (artikel_input not in list_artikels):

			return "%s is Not in References."%(artikel_input)

		else:

			row_ref = reference[reference.Artikel==artikel_input]

			reference.loc[reference.Artikel==artikel_input] = [[artikel_input,typeform_input,diametre_input]]

			#reference.to_csv(os.path.join(LOCAL_DATA,"reference.csv"),index=False,encoding="utf-8")

			#upload_file_git("local_data/reference.csv")

			return "Reference %s, %s, %s Modified to : %s, %s, %s"%(artikel_input,row_ref["Type/Form"].values[0],row_ref["Diametre"].values[0],artikel_input,typeform_input,diametre_input)
	else:

		return ""

@app.callback(Output('output-confirm_del', 'children'),
			  [Input('confirm_del', 'submit_n_clicks')],
			  [State('example-artikel-grid','value'),State('example-typeform-grid','value'),State('example-Diametre-grid','value')])
def update_output_del(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	global reference

	if submit_n_clicks:

		list_artikels = list(reference["Artikel"].unique())

		list_artikels = [str(x) for x in list_artikels]

		if (artikel_input not in list_artikels):

			return "%s is Not in References."%(artikel_input)

		else:

			row_ref = reference[reference.Artikel==artikel_input]

			reference = reference.drop(row_ref.index,axis=0)

			#reference.to_csv(os.path.join(LOCAL_DATA,"reference.csv"),index=False,encoding="utf-8")

			#upload_file_git("local_data/reference.csv")

			return "Reference %s, %s, %s Deleted From References."%(artikel_input,row_ref["Type/Form"].values[0],row_ref["Diametre"].values[0])
	else:

		return ""


############################


@app.callback(Output('output-confirm_ffr', 'children'),
			  [Input('confirm_add_ffr', 'submit_n_clicks')],
			  [State('example-artikel-grid_ffr','value'),State('example-typeform-grid_ffr','value'),State('example-Diametre-grid_ffr','value')])
def update_output(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	global reference_ffr

	if submit_n_clicks:

		list_artikels = list(reference_ffr["Artikel"].unique())

		list_artikels = [str(x) for x in list_artikels]

		if (artikel_input not in list_artikels):

		

			to_add = pd.DataFrame(columns=reference_ffr.columns.values,data=[[artikel_input,typeform_input,diametre_input]])

			reference_ffr = reference_ffr.append(to_add,ignore_index=True)

			reference_ffr.to_csv(os.path.join(LOCAL_DATA,"Reference_ffr.csv"),index=False,encoding="utf-8")

			#upload_file_git("local_data/Reference_ffr.csv")

		

			return "%s - %s - %s Added to References."%(artikel_input,typeform_input,diametre_input)
		else:

			return "Not Added Because Artikel = %s Exists in References"%artikel_input
	else:

		return ""


@app.callback(Output('output-confirm_mod_ffr', 'children'),
			  [Input('confirm_mod_ffr', 'submit_n_clicks')],
			  [State('example-artikel-grid_ffr','value'),State('example-typeform-grid_ffr','value'),State('example-Diametre-grid_ffr','value')])
def update_output_mod(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	global reference_ffr

	if submit_n_clicks:

		list_artikels = list(reference_ffr["Artikel"].unique())

		list_artikels = [str(x) for x in list_artikels]

		if (artikel_input not in list_artikels):

			return "%s is Not in References."%(artikel_input)

		else:

			row_ref = reference_ffr[reference_ffr.Artikel==artikel_input]

			reference_ffr.loc[reference_ffr.Artikel==artikel_input] = [[artikel_input,typeform_input,diametre_input]]

			reference_ffr.to_csv(os.path.join(LOCAL_DATA,"Reference_ffr.csv"),index=False,encoding="utf-8")

			#upload_file_git("local_data/Reference_ffr.csv")

			return "Reference %s, %s, %s Modified to : %s, %s, %s"%(artikel_input,row_ref["Type/Form"].values[0],row_ref["Diametre"].values[0],artikel_input,typeform_input,diametre_input)
	else:

		return ""

@app.callback(Output('output-confirm_del_ffr', 'children'),
			  [Input('confirm_del_ffr', 'submit_n_clicks')],
			  [State('example-artikel-grid_ffr','value'),State('example-typeform-grid_ffr','value'),State('example-Diametre-grid_ffr','value')])
def update_output_del(submit_n_clicks,artikel_input,typeform_input,diametre_input):

	global reference_ffr

	if submit_n_clicks:

		list_artikels = list(reference_ffr["Artikel"].unique())

		list_artikels = [str(x) for x in list_artikels]

		if (artikel_input not in list_artikels):

			return "%s is Not in References."%(artikel_input)

		else:

			row_ref = reference_ffr[reference_ffr.Artikel==artikel_input]

			reference_ffr = reference_ffr.drop(row_ref.index,axis=0)

			reference_ffr.to_csv(os.path.join(LOCAL_DATA,"Reference_ffr.csv"),index=False,encoding="utf-8")

			#upload_file_git("local_data/Reference_ffr.csv")

			return "Reference %s, %s, %s Deleted From References."%(artikel_input,row_ref["Type/Form"].values[0],row_ref["Diametre"].values[0])
	else:

		return ""




############################

@app.callback([Output('table6','data'),Output('table6','columns')],
			  [Input('Artikel_Selector_ffr',"value"),Input('dropdown_artikel_ffr','value'),Input('output-confirm_ffr', 'children'),Input('table1','data'),Input('table1','columns'),Input('output-confirm_mod_ffr','children'),Input('output-confirm_del_ffr','children'),Input('output-data-upload','children')])
def filter_table6(artikel_selector,artikel_values,children,data,column,children_mod,children_del,children_upload):

	global reference_ffr

	if artikel_selector == "selected":
		artikels = artikel_values
	else:
		artikels = reference_ffr["Artikel"].unique()

	if ((data!=None) and (children_upload=="Loaded Saved Sheet1.csv") and ("sheet3.csv" not in os.listdir(LOCAL_DATA) )) or ((data!=None) and (children_upload!="Loaded Saved Sheet1.csv")):

		sheet1 = pd.DataFrame.from_dict(data=data)

		sheet1["Artikel"] = sheet1["Artikel"].astype(str)

		sheet2 = pd.DataFrame(columns=["Artikel","Stuf03","Stuf11","Stuf12","Menge"])

		sheet2["Artikel"] = sheet1.groupby(["Artikel"]).sum()["Menge"].index
		sheet2["Menge"] = sheet1.groupby(["Artikel"]).sum()["Menge"].values




		dff = reference_ffr[reference_ffr.Artikel.isin(artikels)]

		sheet2 = pd.merge(sheet2,dff, on='Artikel')

		sheet2["Stuf03"] = 0
		sheet2["Stuf11"] = 0
		sheet2["Stuf12"] = 0

		columns = []

		for c in sheet2.columns:
			if "stuf" in c.lower():
				columns.append({'id':c,'name':c,'editable':True})
			else:
				columns.append({'id':c,'name':c,'editable':False})
				
		

		#columns = [{'id': c, 'name': c} for c in sheet2.columns]

		return sheet2.to_dict('records'),columns

	elif (data!=None) and (children_upload=="Loaded Saved Sheet1.csv") and ("sheet3.csv" in os.listdir(LOCAL_DATA)):


		sheet2 = pd.read_csv(os.path.join(LOCAL_DATA,"sheet3.csv"))

		columns = []

		for c in sheet2.columns:
			if "stuf" in c.lower():
				columns.append({'id':c,'name':c,'editable':True})
			else:
				columns.append({'id':c,'name':c,'editable':False})

		return sheet2.to_dict('records'),columns


	else:

		return None,[]



############################

@app.callback([Output('table7','data'),Output('table7','columns')],
	[Input('table6', 'data'),Input('table6','columns')])
def update_inter(data,columns):
	if (data!=None) and (data!=[]):
		table6 = pd.DataFrame.from_dict(data=data)
		for col in ["Stuf03","Stuf11","Stuf12"]:
			table6[col] = pd.to_numeric(table6[col],errors="coerce").fillna(0)
		table6["Summe"] = table6["Stuf03"].astype(int)+table6["Stuf11"].astype(int)+table6["Stuf12"].astype(int)+table6["Menge"].astype(int)

		columns = [{'id': c, 'name': c} for c in table6.columns]

		return table6.to_dict('records'),columns	

	return None,[]



############################


@app.callback([Output('graph_8','figure'),Output('graph_9','figure')],
	[Input('table7', 'data'),Input('table7','columns')])
def update_graph_7(data,columns):
	if data!=None:
		table7 = pd.DataFrame.from_dict(data=data)
		summe_typeform = table7.groupby("Type/Form").sum().reset_index().sort_values(by="Summe",ascending=False)
		fig2 = px.bar(summe_typeform,x="Type/Form",y="Summe",barmode="stack",hover_name="Type/Form",color="Type/Form",text="Summe",title="Total Pro Type/Form")
		fig2 = fig2.update_layout(xaxis_type='category')

		summe_diametre = table7.groupby("Diametre").sum().reset_index().sort_values(by="Summe",ascending=False)
		fig3 = px.bar(summe_diametre,x="Diametre",y="Summe",barmode="stack",hover_name="Diametre",color="Diametre",text="Summe",title="Total Pro Diametre")
		fig3 = fig3.update_layout(xaxis_type='category')

		return [fig2,fig3]

	else:
		return no_update



############################


@app.callback([Output('table8','data'),Output('table8','columns'),Output('table8','style_data_conditional')],
	[Input('table7', 'data'),Input('table7','columns'),Input('table4', 'data'),Input('table4','columns')])
def update_inter(data_7,columns_7,data_4,columns_4):
	if (data_7!=None) and (data_7!=[]) and (data_4!=None) and (data_4!=[]):
		table7 = pd.DataFrame.from_dict(data=data_7)
		table4 = pd.DataFrame.from_dict(data=data_4)

		for col in ["Stuf03","Stuf11","Stuf12","Menge","Summe"]:
			table7[col] = pd.to_numeric(table7[col],errors="coerce").fillna(0)
			table4[col] = pd.to_numeric(table4[col],errors="coerce").fillna(0)

		table8 = pd.concat([table4, table7], ignore_index=True)

		table8 = table8.groupby(["Type/Form","Diametre"]).sum().reset_index()

		

		columns = [{'id': c, 'name': c} for c in table8.columns]

		list_colors = ["PaleVioletRed","HotPink","LightPink","DarkOrchid","OldLace","AliceBlue","DarkTurquoise","LightCyan","LawnGreen","ForestGreen","LightCoral","Gold","RoyalBlue","Burlywood"]
		
		random.shuffle(list_colors)

		style_data_conditional=[]
		i=0

		for elem in list(table8["Type/Form"].unique()):
			style_data_conditional.append({
			'if': {
				'filter_query': '{Type/Form} eq "%s"'%(elem),
				

			},
			'backgroundColor': '%s'%(list_colors[i]),
			'color':'black',
			'fontWeight': 'bold',
			},)
			i+=1

		return table8.to_dict('records'),columns,style_data_conditional	

	return None,[],[]


############################


@app.callback([Output('graph_10','figure'),Output('graph_11','figure')],
	[Input('table8', 'data'),Input('table8','columns')])
def update_graph_8(data,columns):
	if data!=None:
		table8 = pd.DataFrame.from_dict(data=data)
		summe_typeform = table8.groupby("Type/Form").sum().reset_index().sort_values(by="Summe",ascending=False)

		fig2 = px.bar(summe_typeform,x="Type/Form",y="Summe",barmode="stack",hover_name="Type/Form",color="Type/Form",text="Summe",title="Total Pro Type/Form")
		fig2 = fig2.update_layout(xaxis_type='category')

		summe_typeform_bis = table8.groupby(["Type/Form",'Diametre']).sum().reset_index()


		#summe_diametre = table4.groupby("Diametre").sum().reset_index().sort_values(by="Summe",ascending=False)
		fig3 = px.bar(summe_typeform_bis,x="Type/Form",y="Summe",barmode="stack",hover_name="Diametre",color="Diametre",text="Summe",title="Total Pro Type/Form Pro Diametre")
		fig3 = fig3.update_layout(xaxis_type='category')

		return [fig2,fig3]

	else:
		return no_update


############################



@app.callback([Output('table4','data'),Output('table4','columns')],
	[Input('table3', 'data'),Input('table3','columns')],)
def update_inter(data,columns):
	if (data!=None) and (data!=[]):
		table4 = pd.DataFrame.from_dict(data=data)
		for col in ["Stuf03","Stuf11","Stuf12"]:
			table4[col] = pd.to_numeric(table4[col],errors="coerce").fillna(0)
		table4["Summe"] = table4["Stuf03"].astype(int)+table4["Stuf11"].astype(int)+table4["Stuf12"].astype(int)+table4["Menge"].astype(int)

		columns = [{'id': c, 'name': c} for c in table4.columns]

		return table4.to_dict('records'),columns	

	return None,[]


###########################################

@app.callback([Output('output_save_fdc','children')],
	[Input('save_stuf', 'n_clicks'),Input('table3','data'),Input('table3','columns')])
def save_table3_fdc(n_clicks,data,columns):
	global update_i
	if n_clicks!=None:
		table3 = pd.DataFrame.from_dict(data=data)
		table3.to_csv(os.path.join(LOCAL_DATA,"sheet2.csv"),index=False,encoding="utf-8")
		#upload_file_git("local_data/sheet2.csv")
		return ["FDC Saved."]
	else:
		return [""]

@app.callback([Output('output_save_ffr','children')],
	[Input('save_stuf_ffr', 'n_clicks'),Input('table6','data'),Input('table6','columns')])
def save_table6_ffr(n_clicks,data,columns):
	global update_i
	if n_clicks!=None:
		table6 = pd.DataFrame.from_dict(data=data)
		table6.to_csv(os.path.join(LOCAL_DATA,"sheet3.csv"),index=False,encoding="utf-8")
		#upload_file_git("local_data/sheet3.csv")
		return ["FFR Saved."]
	else:
		return [""]


###########################################



@app.callback([Output('graph_5','figure'),Output('graph_6','figure')],
	[Input('table4', 'data'),Input('table4','columns')])
def update_graph_6(data,columns):
	if data!=None:
		table4 = pd.DataFrame.from_dict(data=data)
		summe_typeform = table4.groupby("Type/Form").sum().reset_index().sort_values(by="Summe",ascending=False)
		fig2 = px.bar(summe_typeform,x="Type/Form",y="Summe",barmode="stack",hover_name="Type/Form",color="Type/Form",text="Summe",title="Total Pro Type/Form")
		fig2 = fig2.update_layout(xaxis_type='category')

		summe_diametre = table4.groupby("Diametre").sum().reset_index().sort_values(by="Summe",ascending=False)
		fig3 = px.bar(summe_diametre,x="Diametre",y="Summe",barmode="stack",hover_name="Diametre",color="Diametre",text="Summe",title="Total Pro Diametre")
		fig3 = fig3.update_layout(xaxis_type='category')

		return [fig2,fig3]

	else:
		return no_update


if __name__ == '__main__':
	app.run_server(debug=False)
