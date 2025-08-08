import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def categorize_link(url):
    category_patterns = [
        (r'contact|reach.?us', 'Contact Us'),
        (r'about|our.?history', 'About Us'),
        (r'home|index|landing|start|crm', 'Home'),
        (r'service|our.?service|solution|offerings|consulting', 'Services'),
        (r'career|job|vacanc', 'Careers'),
        (r'portfolio|project|case.?stud', 'Portfolio and Projects'),
        (r'products|catalog|shop.?items|accessories|features|packages|menu', 'Products and Catalog'),
        (r'team|staff|member|our.?vision|our.?work|our.?people|our.?approach|our.?values|our.?mission|our.?process|leadership', 'Leadership'),
        (r'technology|digital|tools|systems|platform|software|apps|website|web|hardware', 'Technology and Digital-related'),
        (r'company|busines|industr|info', 'Business and Company-related'),
        (r'marketing', 'Marketing'),
        (r'location|find.?us|direction', 'Location and Directions'),
        (r'twitter|facebook|instagram|pinterest|linkedin|youtube|snapchat|tiktok|social', 'Social Media'),
        (r'blog|article', 'Blog and Articles'),
        (r'api|console|demo|dev|developers', 'Developer'),
        (r'gallery|image|video|exhibition|galleries', 'Gallery'),
        (r'shop|store|checkout|cart|basket', 'Shopping'),
        (r'faq|help|frequently.?asked', 'FAQ'),
        (r'testimonial|review', 'Testimonials and Reviews'),
        (r'term|legal|policy|privacy|cookie.?policy|data.?protection|compliance|gdpr|disclaimer|agreement|policies|copyright|intellectual.?property|term.?condition|cgv|condition', 'Legal and Terms'),
        (r'login|signin|account.?login|register|signup|create.?account|admin|auth|dashboard|panel', 'Login and Registration'),
        (r'donate|donation|give', 'Donation'),
        (r'pricing|plans|rates|price', 'Pricing'),
        (r'sitemap|navigation', 'Sitemap'),
        (r'resource|download|document|doc|forms', 'Resources'),
        (r'media|press|news|updates|announcement|newsletter', 'Media and Press'),
        (r'support|helpdesk|customer.?service', 'Help and Support'),
        (r'feedback|success.?stories', 'Customer Feedback'),
        (r'partner|affiliate', 'Partners'),
        (r'events|calendar', 'Events'),
        (r'membership|subscribe', 'Membership'),
        (r'booking|appointment|reservation|schedule', 'Booking and Reservations'),
        (r'offer|promotion|deals', 'Special Offers'),
        (r'(^en$|^us$|^ru$|^gb$|^fr$|^es$|^it$|^de$|^pt$|^cn$|^jp$|^kr$|^au$|^nz$|^ca$|^in$|^mx$|^br$|^za$|^nl$|^se$|^no$|^dk$|^fi$|^pl$|^ch$|^at$|^be$|^gr$|^cz$|^sk$|^hu$|^ie$|^tr$|^ar$|^cl$|^ve$|^co$|^pe$|^ae$|^sa$|^il$|^sg$|^th$|^my$|^id$|^ph$|^hk$|^tw$|^vn$)', 'Language and Region'),
        (r'user.?guide|manual|tutorial', 'User Guide and Tutorials'),
        (r'catering|restaurant', 'Catering and Restaurants'),
        (r'research|studies|papers', 'Research and Studies'),
        (r'education|training|course|workshop|certification|programs|learning|admission|student|academy', 'Education and Training-related'),
        (r'podcast|insight|publication|content', 'Communication-related'),
        (r'recruitment|join|hire|employees|workforce|talents|people', 'Human Resources and Recruitment-related'),
        (r'customer|client|account|billing', 'Customers'),
        (r'insurance|risk|policies|coverage|protection', 'Insurance and Risk-related'),
        (r'order|purchase|sale|deliver|shipping|return|exchange|e-commerce|discount|refund', 'E-commerce and Sales-related'),
        (r'user', 'User-related')
    ]
    url_lower = url.lower()
    for pattern, category in category_patterns:
        if re.search(pattern, url_lower):
            return category
    return 'Miscellaneous'

def fetch_page_metadata(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else "N/A"
            meta_tag = soup.find("meta", attrs={"name": "description"})
            metadata = meta_tag["content"].strip() if meta_tag and "content" in meta_tag.attrs else "N/A"
            return title, metadata
    except requests.RequestException:
        pass
    return "N/A", "N/A"

def fetch_links(input_file, output_file):
    df = pd.read_csv(input_file, low_memory=False)
    column_name = df.columns[0]
    domains = df.iloc[:, 0].dropna().astype(str).tolist()
    
    headers = {"User-Agent": "Mozilla/5.0"}
    prefixes = ["https://", "https://www.", "http://", "http://www."]
    
    results = []
    
    for domain in domains:
        domain = domain.strip()
        parsed = urlparse(domain)
        
        # If domain has no scheme, prepend one
        if not parsed.scheme:
            for prefix in prefixes:
                test_url = prefix + domain
                try:
                    response = requests.get(test_url, headers=headers, timeout=5)
                    if response.ok:
                        domain = test_url
                        break
                except requests.RequestException:
                    continue
        
        try:
            response = requests.get(domain, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            for link in soup.find_all("a", href=True):
                url = link["href"].strip()
                if url.startswith("/"):
                    url = domain + url  # Make relative links absolute
                links.append(url)
                
            unique_links = list(set(links))
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                metadata_results = list(executor.map(fetch_page_metadata, unique_links))
                
            for i, url in enumerate(unique_links):
                category = categorize_link(url)
                title, metadata = metadata_results[i]
                results.append({
                    "Input URL": domain,
                    "Extracted URL": url,
                    "Category": category,
                    "Title": title,
                    "Metadata": metadata
                })
        
        except requests.RequestException:
            results.append({"Input URL": domain, "Extracted URL": None, "Category": "Failed to fetch", "Title": "N/A", "Metadata": "N/A"})
    
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, index=False)

fetch_links("your_input_file.csv", "your_output_file.csv")