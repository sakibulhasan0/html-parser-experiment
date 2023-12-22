def change_the_C3_table(soup, table_tag):
  # table_tag = soup.find('table')
  if table_tag:
      table_tag['class'] = 'section__table section__table-C-3'
  thead = table_tag.find('thead')
  if thead:
      thead['class'] = 'section__table-heading'

  for tr in table_tag.find_all('tr'):
      tr['class'] = 'section__table-row'

  for th in table_tag.find_all('th'):
      th['class'] = 'section__table-head section__table-w-20'

  tbody = table_tag.find('tbody')
  if tbody:
      tbody['class'] = 'section__table-body section__table-pc'

  for td in table_tag.find_all('td'):
      td['class'] = 'section__table-data'

  sp_tbody = create_sp_tbody(soup, table_tag)
  tbody.insert_before(sp_tbody)
  return table_tag


def create_sp_tbody(soup, table_tag):
  existing_tbody = table_tag.find('tbody')
  th_tags = existing_tbody.find_all('th')
  td_tags = existing_tbody.find_all('td')
  new_tbody = soup.new_tag('tbody')
  new_tbody['class']= 'section__table-body section__table-sp'
  for th, td in zip(th_tags, td_tags):
    new_tr_th = soup.new_tag('tr')
    new_tr_th['class']= ['section__table-row']
    new_th = soup.new_tag('th')
    new_th['class']=['section__table-head']
    new_th.string = th.get_text(strip=True)
    new_tr_th.append(new_th)
    new_tbody.append(new_tr_th)

    new_tr_td = soup.new_tag('tr')
    new_tr_td['class'] = ['section__table-row']
    new_td = soup.new_tag('td')
    new_td['class'] = ['section__table-data']
    new_td.string = td.get_text(strip=True)
    new_tr_td.append(new_td)
    new_tbody.append(new_tr_td)

  return new_tbody