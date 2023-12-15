def change_the_D_table(soup):
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
      p_tag = soup.new_tag('p')
      p_tag["class"] = ['section__price', 'section__price--middle']
      p_tag.append("年")


      numeric_part = ''.join(c for c in td.string if c.isdigit() or c == '.')
      span_tag = soup.new_tag('span')
      span_tag["class"] = ['section__price--number']
      span_tag.append(numeric_part)
      p_tag.append(span_tag)

      p_tag.append(span_tag)
      p_tag.append("%")
      td.clear()
      td.append(p_tag)

