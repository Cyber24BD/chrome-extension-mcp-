"""
Advanced Markdown Converter Service
Converts HTML to well-formatted Markdown using multiple strategies
"""

from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
import html2text
from markdownify import markdownify as md
import re


class MarkdownConverter:
    """Advanced HTML to Markdown converter with multiple strategies"""
    
    def __init__(self):
        # Configure html2text converter
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False
        self.h2t.body_width = 0  # Don't wrap lines
        self.h2t.unicode_snob = True
        self.h2t.skip_internal_links = False
        self.h2t.inline_links = True
        self.h2t.protect_links = True
        self.h2t.mark_code = True
    
    def convert(
        self, 
        html: str, 
        method: str = "html2text",
        clean: bool = True,
        preserve_tables: bool = True,
        preserve_code: bool = True
    ) -> Dict[str, Any]:
        """
        Convert HTML to Markdown with advanced formatting
        
        Args:
            html: HTML content to convert
            method: Conversion method - "html2text", "markdownify", or "auto"
            clean: Whether to clean up the HTML before conversion
            preserve_tables: Keep table formatting
            preserve_code: Keep code block formatting
            
        Returns:
            Dictionary with markdown content and metadata
        """
        
        if not html or not html.strip():
            return {
                "markdown": "",
                "method": method,
                "length": 0,
                "error": "Empty HTML content"
            }
        
        try:
            # Clean HTML if requested
            if clean:
                html = self._clean_html(html)
            
            # Convert based on method
            if method == "html2text":
                markdown = self._convert_html2text(html)
            elif method == "markdownify":
                markdown = self._convert_markdownify(html)
            elif method == "auto":
                # Try html2text first, fallback to markdownify
                try:
                    markdown = self._convert_html2text(html)
                except Exception:
                    markdown = self._convert_markdownify(html)
            else:
                raise ValueError(f"Unknown conversion method: {method}")
            
            # Post-process markdown
            markdown = self._post_process(markdown)
            
            # Extract metadata
            metadata = self._extract_metadata(html)
            
            return {
                "markdown": markdown,
                "method": method,
                "length": len(markdown),
                "lines": len(markdown.split('\n')),
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            return {
                "markdown": "",
                "method": method,
                "length": 0,
                "error": str(e),
                "success": False
            }
    
    def _clean_html(self, html: str) -> str:
        """Clean and prepare HTML for conversion"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style tags
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()
        
        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
            comment.extract()
        
        # Remove hidden elements
        for tag in soup.find_all(style=re.compile(r'display:\s*none')):
            tag.decompose()
        
        # Remove common noise elements
        noise_classes = ['advertisement', 'ads', 'cookie-banner', 'popup', 'modal']
        for noise_class in noise_classes:
            for tag in soup.find_all(class_=re.compile(noise_class, re.I)):
                tag.decompose()
        
        return str(soup)
    
    def _convert_html2text(self, html: str) -> str:
        """Convert using html2text library"""
        return self.h2t.handle(html)
    
    def _convert_markdownify(self, html: str) -> str:
        """Convert using markdownify library"""
        return md(
            html,
            heading_style="ATX",  # Use # for headings
            bullets="-",  # Use - for lists
            strong_em_symbol="**",  # Use ** for bold
            strip=['script', 'style']
        )
    
    def _post_process(self, markdown: str) -> str:
        """Clean up and format the markdown output"""
        
        # Remove excessive blank lines (more than 2 consecutive)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Fix spacing around headings
        markdown = re.sub(r'\n(#{1,6}\s+.+)\n', r'\n\n\1\n\n', markdown)
        
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in markdown.split('\n')]
        markdown = '\n'.join(lines)
        
        # Ensure single trailing newline
        markdown = markdown.strip() + '\n'
        
        return markdown
    
    def _extract_metadata(self, html: str) -> Dict[str, Any]:
        """Extract metadata from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        metadata = {}
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Extract meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            metadata['description'] = desc_tag.get('content', '').strip()
        
        # Extract meta keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            metadata['keywords'] = keywords_tag.get('content', '').strip()
        
        # Extract Open Graph data
        og_title = soup.find('meta', property='og:title')
        if og_title:
            metadata['og_title'] = og_title.get('content', '').strip()
        
        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            metadata['og_description'] = og_desc.get('content', '').strip()
        
        # Count elements
        metadata['headings'] = len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        metadata['paragraphs'] = len(soup.find_all('p'))
        metadata['links'] = len(soup.find_all('a'))
        metadata['images'] = len(soup.find_all('img'))
        metadata['tables'] = len(soup.find_all('table'))
        metadata['lists'] = len(soup.find_all(['ul', 'ol']))
        
        return metadata
    
    def convert_with_options(
        self,
        html: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Convert HTML with custom options
        
        Options:
            - method: "html2text", "markdownify", or "auto"
            - clean: Clean HTML before conversion
            - body_width: Line wrap width (0 = no wrap)
            - ignore_links: Skip links
            - ignore_images: Skip images
            - skip_internal_links: Skip # links
            - inline_links: Use inline link format
            - heading_style: "ATX" (#) or "SETEXT" (underline)
        """
        options = options or {}
        
        # Configure html2text based on options
        if 'body_width' in options:
            self.h2t.body_width = options['body_width']
        if 'ignore_links' in options:
            self.h2t.ignore_links = options['ignore_links']
        if 'ignore_images' in options:
            self.h2t.ignore_images = options['ignore_images']
        if 'skip_internal_links' in options:
            self.h2t.skip_internal_links = options['skip_internal_links']
        if 'inline_links' in options:
            self.h2t.inline_links = options['inline_links']
        
        method = options.get('method', 'html2text')
        clean = options.get('clean', True)
        
        return self.convert(html, method=method, clean=clean)


# Global converter instance
markdown_converter = MarkdownConverter()
