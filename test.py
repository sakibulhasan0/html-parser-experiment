from bs4 import BeautifulSoup
from bs4 import Comment

with open("testfile.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'lxml')

# remove the comments from the file
article = soup.find('article')
for element in article(text=lambda text: isinstance(text, Comment)):
    element.extract()

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
        paragraph['class'] = [new_class_name]
    else:
        paragraph['class'] = new_class_name

# removes divs with class alnright
classes_to_remove = ['alnRight', 'class2', 'class3']

# Find all <div> elements with the specified classes and remove them
for class_name in classes_to_remove:
    divs_to_remove = soup.find_all('div', class_=class_name)
    for div in divs_to_remove:
        div.extract()

# replace the close window p tag with div

# closeWindowTag = soup.find('p.section__text:has(span.icmClose:has(a.section__link:contains("このウインドウを閉じる")))')
# print(closeWindowTag)
# if closeWindowTag:
#     print(closeWindowTag)
#     new_div_tag = BeautifulSoup('''
#         <div class="section__button-wrap-function">
#           <button class="section__button-close js-close" tabindex="200">
#             <span class="section__button-close-text">閉じる</span>
#           </button>
#         </div>
#     ''', 'lxml')
#     closeWindowTag.replace_with(new_div_tag)

p_tag = soup.find('p', class_='section__text')

# Iterate through <p> tags and find the one with the specified child elements
span_icmClose = p_tag.find('span', class_='icmClose')
if span_icmClose:
    a_section_link = span_icmClose.find('a', class_='section__link')
    if a_section_link and 'このウインドウを閉じる' in a_section_link.text:
        # Replace the <p> tag with a new <div> containing the specified structure
        new_div_tag = BeautifulSoup('''
            <div class="section__button-wrap-function">
              <button class="section__button-close js-close" tabindex="200">
                <span class="section__button-close-text">閉じる</span>
              </button>
            </div>
        ''', 'html.parser')
        p_tag.replace_with(new_div_tag)


# removes the remaining window close button if any
# closeWindowTag = soup.find('p.section__text:has(span.icmClose:has(a.section__link:contains("このウインドウを閉じる")))')
# if closeWindowTag:
#     closeWindowTag.extract()


with open('modified_example.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())

print("Modified HTML has been saved to 'modified_example.html'")