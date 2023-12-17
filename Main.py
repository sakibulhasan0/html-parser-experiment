from bs4 import BeautifulSoup
from bs4 import Comment
import re
from table import change_the_D_table
from table_type_2 import change_the_C3_table
from table_top_header_multi_column_all import table_top_header_multi_column_all
import time
start_time = time.time()

with open("raw_article.html", "r", encoding="utf-8") as file:
    html_content = file.read()

with open('modified_file.html', 'w'):
  pass

soup = BeautifulSoup(html_content, 'lxml')

#For Color printing
def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

# remove the comments from the file
article = soup.find('article')
for element in article(text=lambda text: isinstance(text, Comment)):
    element.extract()

# Remove the 'style' attribute from each tag
tags_with_style = soup.find_all(attrs={'style': True})
for tag in tags_with_style:
    del tag['style']

# removes the immidiate h1 tag and replaces with the next h1
h1_inside_article = article.find('h1')
if h1_inside_article:
    next_h1_tag = h1_inside_article.find_next('h1')
    h1_inside_article.extract()
    if next_h1_tag:
        article.insert(0, next_h1_tag)

# change the p tag class
paragraphs = soup.find_all('p')
new_class_name = 'section__text'

for paragraph in paragraphs:
    if 'class' in paragraph.attrs:
        if paragraph['class'] == ['alnRight']:
          paragraph['class'] = [new_class_name, 'section__text--right']
        if paragraph['class'] == ["alnCenter"]:
            paragraph['class'] = [new_class_name]
            div = soup.new_tag('div')
            div['class'] = ["aln-center"]
            new_p = paragraph
            div.append(new_p)
    else:
      paragraph['class'] = new_class_name

# Loop through all tags in the soup and remove the classes
classes_to_remove = ['imageIcon', 'img', 'spTableScroll', 'text']
for tag in soup.find_all(True):
    if 'class' in tag.attrs:
        if(tag['class'] == ["alnRight"]):
          new_p = soup.new_tag('p')
          tag['class'] = ["aln-right"]
          if tag.contents[1]:
            new_p.string = tag.contents[1].get_text(strip=True)
            pattern = r'(?:\(\d{4}年\d{1,2}月\d{1,2}日(?:現在)?\))|\d{4}年\d{1,2}月\d{1,2}日(?:現在)?'
            matches = re.findall(pattern, new_p.get_text(strip=True))
            if(matches):
              new_p['class'] = ["section__text", "section__text-date"]
            else:
              new_p['class'] = ["section__text", "section__text--right"]
            tag.replace_with(new_p)

        if tag['class'] == ["alnCenter"]:
          tag['class'] = ["aln-center"]
          continue
        tag['class'] = [c for c in tag['class'] if c not in classes_to_remove]
        if not tag['class']:
          del tag['class']

# Add tojiru div replcing the <p> tags
p_tags = soup.find_all('p', class_='section__text')
for p_tag in p_tags:
  span_icmClose = p_tag.find('span', class_='icmClose')
  if span_icmClose:
      a_section_link = span_icmClose.find('a', class_='section__link')
      if a_section_link and 'このウインドウを閉じる' in a_section_link.text:
          new_div_tag = BeautifulSoup('''
              <div class="section__button-wrap-function">
                <button class="section__button-close js-close" tabindex="200">
                  <span class="section__button-close-text">閉じる</span>
                </button>
              </div>
          ''', 'html.parser')
          p_tag.replace_with(new_div_tag)

# removes the remaining window close button if any
tojiru_tag = soup.findAll('div', class_='section__button-wrap-function')
if len(tojiru_tag) == 2:
  tojiru_tag[1].extract()


# Remove each <div> without a class attribute
divs_without_class = soup.find_all('div', class_=False)
for div in divs_without_class:
    div.unwrap()

divs_with_class_ = soup.find_all('div', class_="spTableScroll")
# Remove each <div> without a class attribute
for div in divs_with_class_:
    div.unwrap()


# Remove the classes of table elements
tags_to_remove_all_classes = ['table', 'th', 'td', "tbody", "thead", "tr"]

for tag_name in tags_to_remove_all_classes:
    tags = soup.find_all(tag_name)
    for tag in tags:
        del tag['class']

# Change the span class that contains ○ as a child text
target_span = soup.find('span', string='○')
if(target_span):
  del target_span['class']
  grandparent = target_span.find_parent().find_parent()
  new_div = soup.new_tag('div')
  new_div['class'] = 'aln-center'

  parent_li = target_span.find_parent('li')
  if('class' in parent_li.attrs and parent_li['class'] == ['aln-center']):
    grandparent.replace_with(new_div)
    new_div.append(grandparent)
  else:
     print()

# add class to the ul, ol tag
for list_tag in soup.find_all(['ul', 'ol']):
    existing_classes = list_tag.get('class', [])
    if not existing_classes or 'section__list' in existing_classes:
        list_tag['class'] = ['section__list']

# add class to the li tag
for li_tag in soup.find_all('li'):
    if 'class' in li_tag.attrs:
        if li_tag['class'] == ["section__list-link", "section__list-item"]:
          continue
        li_tag['class'] = ['section__list-item']
    else:
        li_tag['class'] = ['section__list-item']

# add class to li>span
for li_tag in soup.find_all('li'):
    span_child = li_tag.find('span', recursive=False)  # Find immediate child <span>
    if span_child:
        if 'class' in span_child.attrs:
            span_child['class'] = ['section__list-char']
        else:
            span_child['class'] = ['section__list-char']

tables = soup.findAll('table')
if(len(tables) >= 0):
  if(len(tables) > 1):
    print(colored(237, 231, 104, "Mulitiple tables found!\n"))
  for table in tables:
    if table:
      a = int(input(colored(202, 2037, 104, "Please choose category: \nIf D type 1\nIf C2 type 2\nIf header is top only with multi column type 3\nFor anything else type 0: ")))
      if (not a): break
      if(a==1):
        change_the_D_table(soup)
      elif (a==2):
        change_the_C3_table(soup)
      elif (a==3):
        table_top_header_multi_column_all(soup)
      else: continue

# delete the paret tag of p with string 記 and change the class
target_p = soup.find('p', string='記')
if(target_p):
  target_p.find_parent().unwrap()
  new_div = soup.new_tag('div')
  new_div['class'] = 'aln-center'
  target_p.replace_with(new_div)
  new_div.append(target_p)

with open('modified_file.html', 'w', encoding='utf-8') as file:
    file.write(soup.article.prettify())

end_time = time.time()
execution_time = round(end_time - start_time, 2)
print(f"{colored(41, 240, 55,'🎉 You completed the page in ' +str(execution_time)+' seconds🎉')}\n{colored(202, 2037, 104, 'Modified HTML has been saved to `modified_file.html`')}")