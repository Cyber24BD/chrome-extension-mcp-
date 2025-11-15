/**
 * Content Extraction Module
 * Handles page content extraction with HTML and Markdown support
 */

export class ContentExtractor {
  
  async getContent(tabId, format = 'html') {
    try {
      // Always extract HTML, let Python handle markdown conversion
      const results = await chrome.scripting.executeScript({
        target: { tabId },
        func: this.extractPageContent
      });
      
      const content = results[0].result;
      content.requestedFormat = format; // Pass format to backend
      
      return {
        success: true,
        content: content
      };
    } catch (error) {
      throw new Error(`Failed to get content: ${error.message}`);
    }
  }
  
  async getPageMetadata(tabId) {
    try {
      const results = await chrome.scripting.executeScript({
        target: { tabId },
        func: this.extractMetadata
      });
      
      return {
        success: true,
        metadata: results[0].result
      };
    } catch (error) {
      throw new Error(`Failed to get metadata: ${error.message}`);
    }
  }
  
  // Injected function - runs in page context
  // Always extract HTML - Python will handle markdown conversion
  extractPageContent() {
    return {
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString(),
      html: document.documentElement.outerHTML,
      bodyHtml: document.body.innerHTML,
      text: document.body.innerText,
      format: 'html'
    };
  }
  
  // Extract metadata for markdown frontmatter
  extractMetadata() {
    const metadata = {
      url: window.location.href,
      title: document.title,
      description: '',
      keywords: [],
      author: '',
      timestamp: new Date().toISOString()
    };
    
    // Extract meta tags
    const metaTags = document.querySelectorAll('meta');
    metaTags.forEach(tag => {
      const name = tag.getAttribute('name') || tag.getAttribute('property');
      const content = tag.getAttribute('content');
      
      if (name && content) {
        if (name.includes('description')) {
          metadata.description = content;
        } else if (name.includes('keywords')) {
          metadata.keywords = content.split(',').map(k => k.trim());
        } else if (name.includes('author')) {
          metadata.author = content;
        }
      }
    });
    
    // Extract Open Graph tags
    const ogTitle = document.querySelector('meta[property="og:title"]');
    const ogDescription = document.querySelector('meta[property="og:description"]');
    
    if (ogTitle) metadata.ogTitle = ogTitle.getAttribute('content');
    if (ogDescription) metadata.ogDescription = ogDescription.getAttribute('content');
    
    return metadata;
  }
}
