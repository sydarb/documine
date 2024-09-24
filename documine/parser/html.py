import logging
from typing import List
from bs4 import BeautifulSoup, NavigableString, Tag

from documine.parser.base import BaseParser
from documine.structures import Element, TitleElement, TextElement, ListElement, TableElement, \
    LinkElement, Metadata

logger = logging.getLogger(__name__)

class HTMLParser(BaseParser):
    def parse(self, file_path: str) -> List[Element]:
        elements = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
        except Exception as e:
            logger.error(f"Failed to parse HTML file {file_path}: {e}")
            return elements
        
        for script in soup(["script", "style", "noscript", "iframe", "embed"]):
            script.extract()

        order_counter = [0]
        body = soup.body if soup.body else soup
        self._traverse_dom(body, elements, order_counter)

        return elements

    def _traverse_dom(self, node, elements, order_counter, parent_xpath=''):
        for child in node.children:
            if isinstance(child, NavigableString):
                continue
                text = child.strip()
                if text:
                    metadata = Metadata(
                        content_type='text',
                        tag_name=child.parent.name,
                        attributes=child.parent.attrs,
                        order=order_counter[0],
                        xpath=parent_xpath,
                    )
                    elements.append(TextElement(content=text, metadata=metadata))
                    order_counter[0] += 1
            elif isinstance(child, Tag):
                xpath = f"{parent_xpath}/{child.name}[{self._get_sibling_index(child)}]"

                # Titles
                if child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    text_content, links = self._extract_text_and_links(child)
                    if text_content.strip():
                        metadata = Metadata(
                            content_type='title',
                            tag_name=child.name,
                            attributes=child.attrs,
                            order=order_counter[0],
                            xpath=xpath,
                            links=links,
                        )
                        elements.append(TitleElement(content=text_content.strip(), metadata=metadata))
                        order_counter[0] += 1

                elif child.name in ['p', 'blockquote', 'span']:
                    text_content, links = self._extract_text_and_links(child)
                    if text_content.strip():
                        metadata = Metadata(
                            content_type='text',
                            tag_name=child.name,
                            attributes=child.attrs,
                            order=order_counter[0],
                            xpath=xpath,
                            links=links,
                        )
                        elements.append(TextElement(content=text_content.strip(), metadata=metadata))
                        order_counter[0] += 1

                # Lists
                elif child.name in ['ul', 'ol']:
                    list_items = []
                    for li in child.find_all('li', recursive=False):
                        item_text = li.get_text(separator=' ', strip=True)
                        if item_text:
                            list_items.append(item_text)
                    if list_items:
                        metadata = Metadata(
                            content_type='list',
                            tag_name=child.name,
                            attributes=child.attrs,
                            order=order_counter[0],
                            xpath=xpath,
                        )
                        elements.append(ListElement(items=list_items, metadata=metadata))
                        order_counter[0] += 1

                # Images
                # elif child.name == 'img':
                #     src = child.get('src')
                #     alt = child.get('alt', '')
                #     if src:
                #         metadata = Metadata(
                #             content_type='image',
                #             tag_name=child.name,
                #             attributes=child.attrs,
                #             order=order_counter[0],
                #             xpath=xpath,
                #         )
                #         elements.append(Image(content=src, metadata=metadata))
                #         order_counter[0] += 1

                # Links
                elif child.name == 'a':
                    text = child.get_text(separator=' ', strip=True)
                    href = child.get('href')
                    if href:
                        metadata = Metadata(
                            content_type='link',
                            tag_name=child.name,
                            attributes=child.attrs,
                            order=order_counter[0],
                            xpath=xpath,
                        )
                        elements.append(LinkElement(text=text, href=href, metadata=metadata))
                        order_counter[0] += 1

                # Tables
                elif child.name == 'table':
                    table_data = self._parse_table(child)
                    if table_data:
                        metadata = Metadata(
                            content_type='table',
                            tag_name=child.name,
                            attributes=child.attrs,
                            order=order_counter[0],
                            xpath=xpath,
                        )
                        elements.append(TableElement(data=table_data, metadata=metadata))
                        order_counter[0] += 1

                # Other elements (including 'div')
                else:
                    # Recursively process child elements
                    self._traverse_dom(child, elements, order_counter, parent_xpath=xpath)
            else:
                continue


    def _get_sibling_index(self, element):
        count = 1
        for sibling in element.previous_siblings:
            if isinstance(sibling, Tag) and sibling.name == element.name:
                count += 1
        return count

    def _parse_table(self, table_tag):
        rows = []
        for row in table_tag.find_all('tr'):
            cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
            rows.append(cols)
        return rows
    
    def _extract_text_and_links(self, element):
        text_parts = []
        links = []

        def recurse(node):
            if isinstance(node, NavigableString):
                text_parts.append(str(node))
            elif isinstance(node, Tag):
                if node.name == 'a':
                    href = node.get('href')
                    link_text = node.get_text(separator=' ', strip=True)
                    start_index = len(''.join(text_parts))
                    # Append link text
                    text_parts.append(link_text)
                    # Record the link info
                    links.append({
                        'href': href,
                        'text': link_text,
                        'start_index': start_index,
                        'end_index': start_index + len(link_text)
                    })
                else:
                    for child in node.contents:
                        recurse(child)

        recurse(element)
        text_content = ''.join(text_parts)
        return text_content, links


