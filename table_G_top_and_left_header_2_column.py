def table_G_top_and_left_header_2_column(table_tag):
  if table_tag:
      table_tag['class'] = 'section__table'
  thead = table_tag.find('thead')
  tbody = table_tag.find('tbody')

  if thead and tbody:
     thead_children = thead.find_all('tr')
     tbody_children = tbody.find_all(recursive=False)
     for i in range(len(thead_children)):
      tbody.insert(i, thead_children[i])

     thead.decompose()

  for tr in table_tag.find_all('tr'):
      tr['class'] = 'section__table-row'

  for th in table_tag.find_all('th'):
    th['class'] = 'section__table-head'

  th = table_tag.find('th')
  th['class'] = 'section__table-head'
  next_th_tag = th.find_next('th')
  next_th_tag['class'] = 'section__table-head'

  tbody = table_tag.find('tbody')
  if tbody:
      tbody['class'] = 'section__table-body'

  for td in table_tag.find_all('td'):
      td['class'] = 'section__table-data'
  return table_tag