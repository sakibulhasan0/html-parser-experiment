def change_the_C3_table(soup):
  table = soup.find('table')
  if table:
      table['class'] = 'section__table section__table-C-3'
  thead = soup.find('thead')
  if thead:
      thead['class'] = 'section__table-heading'

  for tr in soup.find_all('tr'):
      tr['class'] = 'section__table-row'

  for th in soup.find_all('th'):
      th['class'] = 'section__table-head section__table-w-30'

  tbody = soup.find('tbody')
  if tbody:
      tbody['class'] = 'section__table-body section__table-pc'

  for td in soup.find_all('td'):
      td['class'] = 'section__table-data'

  sp_tbody = create_sp_tbody(soup)
  tbody.insert_before(sp_tbody)


def create_sp_tbody(soup):
  existing_tbody = soup.find('tbody')
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