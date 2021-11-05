import requests
import pandas as pd
import json

def run(year, tax_amt):
	pd.options.display.float_format = '{:,.2f}'.format

	agency_req = requests.get('https://api.usaspending.gov/api/v2/references/toptier_agencies')
	agency_json = agency_req.json()['results']
	df = pd.DataFrame.from_dict(agency_json)

	agency_ids = df['agency_id'].to_list()
	agency_names = df['agency_name'].to_list()

	'''
	filters = {"filters":{"recipient_id":"1c3edaaa-611b-840c-bf2b-fd34df49f21f-P","time_period":[{"start_date":"2020-01-01","end_date":"2020-12-31"}]},"limit":99}
	request = requests.post('https://api.usaspending.gov/api/v2/search/spending_by_category/district', json=filters)
	for entity in request.json()['results']:
		print(entity)
	'''
	data = []
	for agency,agency_name in zip(agency_ids,agency_names):
	    request = requests.get('https://api.usaspending.gov/api/v2/federal_obligations/?fiscal_year='+str(year)+'&funding_agency_id='+str(agency)+'&limit=500&page=1')
	    req_json = request.json()['results']
	    for element in req_json:
	        element['agency_id'] = agency
	        element['agency_name'] = agency_name
	        data.append(element)

	output = pd.DataFrame.from_dict(data)
	output = output.drop(['id','account_number','agency_id'], axis = 1)
	output.obligated_amount = output.obligated_amount.astype(float)
	output = output.sort_values('obligated_amount', ignore_index=True, ascending=False)
	output['obligated_amount_pct'] = output['obligated_amount'] / output['obligated_amount'].sum()
	output = output.drop(['obligated_amount'], axis = 1)
	output['your_contribution'] = round(output['obligated_amount_pct'] * tax_amt, 2)
	output['obligated_amount_pct'] = round(output['obligated_amount_pct']*100, 2)
	output = output[output['your_contribution']>=0.01]
	output = output[['agency_name', 'account_title', 'your_contribution', 'obligated_amount_pct']]
	output.columns = ['Agency', 'Account', 'Your Contribution', 'Allocation %']

	output_text = output.to_markdown(index=False)
	return output_text