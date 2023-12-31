def table_top_header_multi_column_all(soup):
  table = soup.find('table')
  if table:
      table['class'] = 'section__table section__table-D'
  thead = soup.find('thead')
  if thead:
      thead['class'] = 'section__table-heading'

  for tr in soup.find_all('tr'):
      tr['class'] = 'section__table-row'

  for th in soup.find_all('th'):
      th['class'] = 'section__table-head section__table-head--strong section__table-cell--center'

  tbody = soup.find('tbody')
  if tbody:
      tbody['class'] = 'section__table-body'

  for td in soup.find_all('td'):
      td['class'] = 'section__table-data section__table-cell--center'
      td_string = td.string_s